from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Problem, Submission, TestCase
import subprocess
import sys
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dotenv import load_dotenv
from openai import OpenAI
import os
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.contrib.auth import get_user_model

import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

# Helper functions


import subprocess
import sys
import shutil
from tempfile import NamedTemporaryFile
from pathlib import Path

def execute_code(code, language, input_data, time_limit):
    output, error = "", ""

    try:
        if language == 'cpp':
            with NamedTemporaryFile(suffix='.cpp', delete=False) as f:
                f.write(code.encode())
                cpp_file = Path(f.name)

            exec_file = cpp_file.with_suffix('.out')

            # Dynamically find g++ in system path
            gpp_path = shutil.which("g++")
            if not gpp_path:
                raise RuntimeError("g++ compiler not found. Ensure it is installed and in PATH.")

            # Compile the C++ code
            compile_result = subprocess.run(
                [gpp_path, str(cpp_file), '-o', str(exec_file)],
                stderr=subprocess.PIPE,
                text=True
            )

            if compile_result.returncode != 0:
                error = compile_result.stderr.strip()
            else:
                result = subprocess.run(
                    [str(exec_file)],
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=time_limit
                )
                output = result.stdout.strip()
                error = result.stderr.strip()

            # Cleanup
            cpp_file.unlink(missing_ok=True)
            exec_file.unlink(missing_ok=True)

        elif language == 'python':
            result = subprocess.run(
                [sys.executable, '-c', code],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=time_limit
            )
            output = result.stdout.strip()
            error = result.stderr.strip()

    except subprocess.TimeoutExpired:
        error = f"Time Limit Exceeded ({time_limit}s)"
    except Exception as e:
        error = str(e)

    return output, error



# Views
def problem_list(request):
    problems = Problem.objects.filter(is_public=True).order_by('-created_at')
    return render(request, 'problems/list.html', {'problems': problems})

@login_required
def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id, is_public=True)
    testcases = TestCase.objects.filter(problem=problem)
    sample_testcase = testcases.filter(is_sample=True).first()
    
    # Default code template
    default_code = f"""# {problem.title}
# Difficulty: {problem.difficulty}
# Time Limit: {problem.time_limit}s

def solve():
    # Your solution here
    pass

# Read input
input_data = input().strip()

# Process and output
result = solve()
print(result)
"""
    
    context = {
        'problem': problem,
        'sample_testcase': sample_testcase,
        'default_code': default_code,
    }
    return render(request, 'problems/detail.html', context)

@csrf_exempt
@login_required
def run_code(request, problem_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            language = data.get('language', 'python')
            custom_input = data.get('custom_input', '').strip()  # Clean whitespace
            problem = get_object_or_404(Problem, pk=problem_id)

            # Fallback to sample input if custom input is empty
            if not custom_input:
                testcase = TestCase.objects.filter(problem=problem, is_sample=True).first()
                if testcase:
                    custom_input = testcase.input_data
                else:
                    return JsonResponse({'error': 'No sample input available and custom input was empty.'}, status=400)

            output, error = execute_code(code, language, custom_input, problem.time_limit)

            return JsonResponse({
                'output': output,
                'error': error,
                'input_used': custom_input
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@login_required
def run_all_testcases(request, problem_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            language = data.get('language', 'python')
            problem = get_object_or_404(Problem, pk=problem_id)
            testcases = TestCase.objects.filter(problem=problem)
            
            results = []
            passed = 0
            
            for testcase in testcases:
                output, error = execute_code(code, language, testcase.input_data, problem.time_limit)
                
                if error:
                    verdict = "Error"
                elif output == testcase.expected_output:
                    verdict = "Passed"
                    passed += 1
                else:
                    verdict = "Failed"
                
                if testcase.is_sample:
                    results.append({
                    'input': testcase.input_data,
                    'expected_output': testcase.expected_output,
                    'output': output,
                    'error': error,
                    'verdict': verdict,
                    'is_sample': True
                })
            else:
                results.append({
                    'verdict': verdict,
                    'is_sample': False
                })

            
            return JsonResponse({
                'results': results,
                'passed': passed,
                'total': len(testcases),
                'score': f"{passed}/{len(testcases)}"
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@login_required
def submit_code(request, problem_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            language = data.get('language', 'python')
            problem = get_object_or_404(Problem, pk=problem_id)
            testcases = TestCase.objects.filter(problem=problem)

            passed = 0
            total = len(testcases)
            sample_results = []

            for testcase in testcases:
                output, error = execute_code(code, language, testcase.input_data, problem.time_limit)

                if error:
                    verdict = "Error"
                elif output == testcase.expected_output:
                    verdict = "Passed"
                    passed += 1
                else:
                    verdict = "Failed"

                # Collect detailed result only for sample test cases
                if testcase.is_sample:
                    sample_results.append({
                        'input': testcase.input_data,
                        'expected_output': testcase.expected_output,
                        'output': output,
                        'error': error,
                        'verdict': verdict,
                        'is_sample': True
                    })

            # Determine overall verdict
            if passed == total:
                overall_verdict = "Accepted"
            elif passed > 0:
                overall_verdict = "Partial Answer"
            else:
                overall_verdict = "Wrong Answer"

            # Save submission
            submission = Submission.objects.create(
                user=request.user,
                problem=problem,
                code=code,
                language=language,
                verdict=overall_verdict
            )

            return JsonResponse({
                'submission_id': submission.id,
                'verdict': overall_verdict,
                'score': f"{passed}/{total}",
                'results': sample_results,
                'timestamp': submission.created_at.isoformat()
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


import requests
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from problems.models import Problem
import json

import json
import requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from problems.models import Problem

@csrf_exempt
@login_required
def ai_code_review(request, problem_id):
    if request.method == 'POST':
        try:
            # Parse request data
            data = json.loads(request.body)
            code = data.get('code', '')
            language = data.get('language', 'python')

            # Fetch problem details
            problem = get_object_or_404(Problem, pk=problem_id)

            # Optional language-specific guidelines
            language_guidelines = {
                'python': [
                    "Check PEP 8 compliance",
                    "Use Pythonic idioms (e.g., list comprehensions)",
                    "Analyze exception handling"
                ],
                'cpp': [
                    "Check for memory management issues",
                    "Use of STL (Standard Template Library)",
                    "Proper pointer/reference usage",
                    "Check const-correctness"
                ]
            }

            # Create prompt for Gemini
            prompt = f"""
Please review the following {language} code solution to a competitive programming problem.

Focus on these areas:
- Code quality and readability
- Efficiency (time and space)
- Handling of edge cases
- Bug risks or logic flaws
- Best practices in {language}
- Specific points: {', '.join(language_guidelines.get(language, []))}

### Problem:
**{problem.title}**

{problem.description}

### User Code:

### Provide feedback in this format:
1. **Code Quality Assessment**
2. **Efficiency Analysis**
3. **Improvement Suggestions**
4. **Potential Bugs**
5. **Final Grade** (A-F)
"""

            # Call Gemini API
            response = requests.post(
                url="https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
                headers={"Content-Type": "application/json"},
                params={"key": settings.GEMINI_API_KEY},
                json={
                    "contents": [{
                        "parts": [{"text": prompt}],
                        "role": "user"
                    }]
                }
            )

            # Handle Gemini response
            if response.status_code == 200:
                result = response.json()
                review_text = result['candidates'][0]['content']['parts'][0]['text']
                return JsonResponse({
                    'review': review_text,
                    'language': language,
                    'problem': problem.title
                })
            else:
                return JsonResponse({
                    'error': f"Gemini API returned status {response.status_code}",
                    'details': response.text
                }, status=500)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



@login_required
def user_submissions(request):
    submissions_list = Submission.objects.filter(user=request.user).order_by('-created_at')
    accepted_count = submissions_list.filter(verdict='Accepted').count()
    
    paginator = Paginator(submissions_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'submissions': page_obj,
        'accepted_count': accepted_count,
    }
    return render(request, 'problems/user_submissions.html', context)

@login_required
def profile_view(request):
    solved = Submission.objects.filter(user=request.user, verdict='Accepted').values_list('problem', flat=True).distinct()
    easy = Problem.objects.filter(id__in=solved, difficulty='Easy').count()
    medium = Problem.objects.filter(id__in=solved, difficulty='Medium').count()
    hard = Problem.objects.filter(id__in=solved, difficulty='Hard').count()
    
    return render(request, 'problems/profile.html', {
        'easy': easy,
        'medium': medium,
        'hard': hard,
        'total': easy + medium + hard,
    })

from django.contrib.auth import get_user_model
User = get_user_model()

def leaderboard(request):
    user_scores = (
        User.objects.annotate(
            problems_solved=Count(
                'submission__problem',
                filter=Q(submission__verdict="Accepted"),
                distinct=True
            )
        )
        .order_by('-problems_solved')[:50]
    )
    return render(request, 'problems/leaderboard.html', {'user_scores': user_scores})

from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Submission, Problem

def leaderboard_api(request):
    users = User.objects.all()
    user_scores = []

    for user in users:
        solved = Submission.objects.filter(user=user, verdict="Accepted").values('problem').distinct().count()
        if solved > 0:
            user_scores.append({
                "username": user.username,
                "problems_solved": solved
            })

    # Sort descending by problems_solved
    user_scores.sort(key=lambda x: x["problems_solved"], reverse=True)
    return JsonResponse(user_scores, safe=False)

from django.shortcuts import redirect, render

from django.shortcuts import render, redirect

def home(request):
    """Landing page view for non-authenticated users"""
    if request.user.is_authenticated:
        return redirect('problems:problem_list')
    return render(request, 'problems/home.html')