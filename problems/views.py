from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Problem, Submission
import subprocess
import sys
import json
from pathlib import Path
from tempfile import NamedTemporaryFile
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def problem_list(request):
    problems = Problem.objects.filter(is_public=True).order_by('-created_at')
    return render(request, 'problems/list.html', {'problems': problems})

# @login_required
# def problem_detail(request, problem_id):
#     problem = get_object_or_404(Problem, pk=problem_id, is_public=True)
#     output, error = "", ""

#     if request.method == 'POST':
#         code = request.POST.get('code', '')
#         language = request.POST.get('language', 'python')

#         submission = Submission.objects.create(
#             problem=problem,
#             user=request.user,
#             code=code,
#             language=language
#         )

#         # Load test cases
#         testcase_path = Path(settings.BASE_DIR) / 'problem_testcases' / f'problem_{problem.id}.json'
#         try:
#             testcases = json.loads(testcase_path.read_text())
#         except Exception as e:
#             error = f"Failed to load test cases: {str(e)}"
#             submission.verdict = "Error"
#             submission.save()
#             return render(request, 'problems/detail.html', {
#                 'problem': problem,
#                 'output': output,
#                 'error': error,
#                 'default_code': code
#             })

#         all_passed = True
#         combined_output = []
#         combined_error = []

#         try:
#             if language == 'cpp':
#                 with NamedTemporaryFile(suffix='.cpp', delete=False) as f:
#                     f.write(code.encode())
#                     cpp_file = Path(f.name)

#                 exec_file = cpp_file.with_suffix('.out')
#                 compile_result = subprocess.run(
#                     ['g++', str(cpp_file), '-o', str(exec_file)],
#                     stderr=subprocess.PIPE,
#                     text=True
#                 )
#                 if compile_result.returncode != 0:
#                     error = compile_result.stderr
#                     all_passed = False
#                 else:
#                     for case in testcases:
#                         result = subprocess.run(
#                             [str(exec_file)],
#                             input=case['input'],
#                             capture_output=True,
#                             text=True,
#                             timeout=problem.time_limit
#                         )
#                         out = result.stdout.strip()
#                         err = result.stderr.strip()
#                         combined_output.append(out)
#                         combined_error.append(err)
#                         if err or out != case['expected_output']:
#                             all_passed = False

#                 cpp_file.unlink(missing_ok=True)
#                 exec_file.unlink(missing_ok=True)

#             elif language == 'python':
#                 for case in testcases:
#                     result = subprocess.run(
#                         [sys.executable, '-c', code],
#                         input=case['input'],
#                         capture_output=True,
#                         text=True,
#                         timeout=problem.time_limit
#                     )
#                     out = result.stdout.strip()
#                     err = result.stderr.strip()
#                     combined_output.append(out)
#                     combined_error.append(err)
#                     if err or out != case['expected_output']:
#                         all_passed = False

#         except subprocess.TimeoutExpired:
#             error = f"Time Limit Exceeded ({problem.time_limit}s)"
#             submission.verdict = "Time Limit Exceeded"
#             submission.save()
#             return render(request, 'problems/detail.html', {
#                 'problem': problem,
#                 'output': '',
#                 'error': error,
#                 'default_code': code
#             })

#         output = "\n".join(combined_output)
#         error = "\n".join(filter(None, combined_error))
#         submission.verdict = "Accepted" if all_passed else "Wrong Answer"
#         submission.save()

#     context = {
#         'problem': problem,
#         'output': output,
#         'error': error,
#         'default_code': f"# Solve {problem.title}\n# Language: Python\n" if request.method != 'POST' else request.POST.get('code', ''),
#     }
#     return render(request, 'problems/detail.html', context)

@csrf_exempt
@login_required
def run_code_api(request, problem_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        code = data.get('code', '')
        custom_input = data.get('custom_input', '')
        language = data.get('language', 'python')
        output, error = "", ""

        try:
            if language == 'cpp':
                with NamedTemporaryFile(suffix='.cpp', delete=False) as f:
                    f.write(code.encode())
                    cpp_file = Path(f.name)

                exec_file = cpp_file.with_suffix('.out')
                compile_result = subprocess.run(['g++', str(cpp_file), '-o', str(exec_file)],
                                                stderr=subprocess.PIPE, text=True)
                if compile_result.returncode != 0:
                    error = compile_result.stderr
                else:
                    result = subprocess.run([str(exec_file)], input=custom_input,
                                            capture_output=True, text=True)
                    output = result.stdout.strip()
                    error = result.stderr.strip()

                cpp_file.unlink(missing_ok=True)
                exec_file.unlink(missing_ok=True)

            elif language == 'python':
                result = subprocess.run([sys.executable, '-c', code],
                                        input=custom_input, capture_output=True,
                                        text=True)
                output = result.stdout.strip()
                error = result.stderr.strip()

        except subprocess.TimeoutExpired:
            error = "Time Limit Exceeded"

        return JsonResponse({'output': output, 'error': error})

# @csrf_exempt
# @login_required
# def submit_code_api(request, problem_id):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         code = data.get('code', '')
#         language = data.get('language', 'python')
#         problem = get_object_or_404(Problem, pk=problem_id)
#         testcase_path = Path(settings.BASE_DIR) / 'problem_testcases' / f'problem_{problem.id}.json'

#         try:
#             testcases = json.loads(testcase_path.read_text())
#         except Exception as e:
#             return JsonResponse({'error': f"Failed to load test cases: {str(e)}"})

#         verdicts = []
#         passed = 0

#         try:
#             if language == 'cpp':
#                 with NamedTemporaryFile(suffix='.cpp', delete=False) as f:
#                     f.write(code.encode())
#                     cpp_file = Path(f.name)
#                 exec_file = cpp_file.with_suffix('.out')
#                 compile_result = subprocess.run(['g++', str(cpp_file), '-o', str(exec_file)],
#                                                 stderr=subprocess.PIPE, text=True)
#                 if compile_result.returncode != 0:
#                     return JsonResponse({'error': compile_result.stderr})

#                 for i, case in enumerate(testcases):
#                     result = subprocess.run([str(exec_file)], input=case['input'],
#                                             capture_output=True, text=True, timeout=problem.time_limit)
#                     out = result.stdout.strip()
#                     verdict = "Passed" if out == case['expected_output'].strip() else "Failed"
#                     verdicts.append({'case': i + 1, 'verdict': verdict, 'output': out})
#                     if verdict == "Passed":
#                         passed += 1

#                 cpp_file.unlink(missing_ok=True)
#                 exec_file.unlink(missing_ok=True)

#             elif language == 'python':
#                 for i, case in enumerate(testcases):
#                     result = subprocess.run([sys.executable, '-c', code],
#                                             input=case['input'], capture_output=True,
#                                             text=True, timeout=problem.time_limit)
#                     out = result.stdout.strip()
#                     verdict = "Passed" if out == case['expected_output'].strip() else "Failed"
#                     verdicts.append({'case': i + 1, 'verdict': verdict, 'output': out})
#                     if verdict == "Passed":
#                         passed += 1

#         except subprocess.TimeoutExpired:
#             return JsonResponse({'error': "Time Limit Exceeded"})

#         return JsonResponse({
#             'verdicts': verdicts,
#             'score': f"{passed}/{len(testcases)}"
#         })
    


# @login_required
# def user_submissions(request):
#     submissions = Submission.objects.filter(user=request.user).order_by('-created_at')
#     return render(request, 'problems/user_submissions.html', {'submissions': submissions})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Submission
from django.core.paginator import Paginator

@login_required
def user_submissions(request):
    # Get all submissions for the current user, newest first
    submissions_list = Submission.objects.filter(user=request.user).order_by('-created_at')
    
    # Count accepted submissions
    accepted_count = submissions_list.filter(verdict='Accepted').count()
    
    # Pagination (10 per page)
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
    easy = Problem.objects.filter(id__in=solved, difficulty='easy').count()
    medium = Problem.objects.filter(id__in=solved, difficulty='medium').count()
    hard = Problem.objects.filter(id__in=solved, difficulty='hard').count()
    
    return render(request, 'problems/profile.html', {
        'easy': easy,
        'medium': medium,
        'hard': hard,
        'total': easy + medium + hard,
    })

# views.py
from django.db.models import Count, Q
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
        .order_by('-problems_solved')[:50]  # top 50
    )
    return render(request, 'problems/leaderboard.html', {'user_scores': user_scores})


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from problems.models import Problem
from openai import OpenAI
import os

# Load OpenAI API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@csrf_exempt
@login_required
def ai_code_review(request, problem_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            language = data.get('language', 'python')
            problem = get_object_or_404(Problem, pk=problem_id)

            # Prompt construction
            prompt = f"""
Please review this {language} code solution for the following programming problem.
Provide constructive feedback on code quality, efficiency, style, and potential improvements.

Problem Title: {problem.title}
Problem Description: {problem.description}

The code to review:
{code}

Please provide:
1. A brief summary of what the code does well
2. Specific areas for improvement
3. Suggestions for better practices
4. Any potential bugs or edge cases not handled
5. A letter grade (A-F) for code quality

Format your response in clear, markdown-formatted sections.
"""

            # Use the updated OpenAI SDK call
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful programming code reviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            review = response.choices[0].message.content
            return JsonResponse({'review': review})

        except Exception as e:
            return JsonResponse({'error': f"Failed to generate AI review: {str(e)}"})
        
@login_required
def problem_detail(request, problem_id):
    problem = get_object_or_404(Problem, pk=problem_id, is_public=True)
    output, error = "", ""
    latest_submission = None

    # Default code template based on problem details
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

    if request.method == 'POST':
        code = request.POST.get('code', '')
        language = request.POST.get('language', 'python')

        # Create submission before running tests
        submission = Submission.objects.create(
            problem=problem,
            user=request.user,
            code=code,
            language=language,
            verdict='Running'  # Initial status
        )

        # Load test cases
        testcase_path = Path(settings.BASE_DIR) / 'problem_testcases' / f'problem_{problem.id}.json'
        try:
            testcases = json.loads(testcase_path.read_text())
        except Exception as e:
            error = f"Failed to load test cases: {str(e)}"
            submission.verdict = "Error"
            submission.save()
            return render(request, 'problems/detail.html', {
                'problem': problem,
                'output': output,
                'error': error,
                'default_code': code,
                'latest_submission': submission
            })

        all_passed = True
        combined_output = []
        combined_error = []

        try:
            if language == 'cpp':
                with NamedTemporaryFile(suffix='.cpp', delete=False) as f:
                    f.write(code.encode())
                    cpp_file = Path(f.name)

                exec_file = cpp_file.with_suffix('.out')
                compile_result = subprocess.run(
                    ['g++', str(cpp_file), '-o', str(exec_file)],
                    stderr=subprocess.PIPE,
                    text=True
                )
                if compile_result.returncode != 0:
                    error = compile_result.stderr
                    all_passed = False
                else:
                    for case in testcases:
                        result = subprocess.run(
                            [str(exec_file)],
                            input=case['input'],
                            capture_output=True,
                            text=True,
                            timeout=problem.time_limit
                        )
                        out = result.stdout.strip()
                        err = result.stderr.strip()
                        combined_output.append(f"Test Case Input:\n{case['input']}\nExpected Output:\n{case['expected_output']}\nYour Output:\n{out}")
                        combined_error.append(err)
                        if err or out != case['expected_output']:
                            all_passed = False

                cpp_file.unlink(missing_ok=True)
                exec_file.unlink(missing_ok=True)

            elif language == 'python':
                for case in testcases:
                    result = subprocess.run(
                        [sys.executable, '-c', code],
                        input=case['input'],
                        capture_output=True,
                        text=True,
                        timeout=problem.time_limit
                    )
                    out = result.stdout.strip()
                    err = result.stderr.strip()
                    combined_output.append(f"Test Case Input:\n{case['input']}\nExpected Output:\n{case['expected_output']}\nYour Output:\n{out}")
                    combined_error.append(err)
                    if err or out != case['expected_output']:
                        all_passed = False

        except subprocess.TimeoutExpired:
            error = f"Time Limit Exceeded ({problem.time_limit}s)"
            submission.verdict = "Time Limit Exceeded"
            submission.save()
            return render(request, 'problems/detail.html', {
                'problem': problem,
                'output': '',
                'error': error,
                'default_code': code,
                'latest_submission': submission
            })

        output = "\n\n".join(combined_output)
        error = "\n".join(filter(None, combined_error))
        submission.verdict = "Accepted" if all_passed else "Wrong Answer"
        submission.save()
        latest_submission = submission
        default_code = code  # Preserve the submitted code

    # Get user's recent submissions for this problem
    recent_submissions = Submission.objects.filter(
        problem=problem,
        user=request.user
    ).order_by('-created_at')[:5]

    context = {
        'problem': problem,
        'output': output,
        'error': error,
        'default_code': default_code,
        'latest_submission': latest_submission,
        'recent_submissions': recent_submissions,
    }
    return render(request, 'problems/detail.html', context)

import json
from pathlib import Path
from tempfile import NamedTemporaryFile
import subprocess
import sys
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Submission, Problem

@csrf_exempt
@login_required
@require_POST
def submit_code_api(request, problem_id):
    try:
        data = json.loads(request.body)
        code = data.get('code', '')
        language = data.get('language', 'python').lower()
        problem = get_object_or_404(Problem, pk=problem_id)
        
        # Initialize default verdict
        overall_verdict = "Wrong Answer"
        passed = 0
        verdict_details = []

        # Load test cases
        testcase_path = Path(settings.BASE_DIR) / 'problem_testcases' / f'problem_{problem.id}.json'
        try:
            with open(testcase_path, 'r') as f:
                testcases = json.load(f)
        except Exception as e:
            return JsonResponse({'error': f"Failed to load test cases: {str(e)}"}, status=500)

        # Process submission
        try:
            if language == 'cpp':
                # Compile C++ code
                with NamedTemporaryFile(suffix='.cpp', delete=False) as src_file:
                    src_file.write(code.encode())
                    src_file_path = Path(src_file.name)
                
                exec_file = src_file_path.with_suffix('.out')
                compile_result = subprocess.run(
                    ['g++', str(src_file_path), '-o', str(exec_file)],
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                if compile_result.returncode != 0:
                    overall_verdict = "Compilation Error"
                    raise Exception(compile_result.stderr)

                # Run test cases
                for case in testcases:
                    try:
                        result = subprocess.run(
                            [str(exec_file)],
                            input=case['input'],
                            capture_output=True,
                            text=True,
                            timeout=problem.time_limit
                        )
                        output = result.stdout.strip()
                        verdict = "Passed" if output == case['expected_output'].strip() else "Failed"
                        verdict_details.append({
                            'input': case['input'],
                            'expected': case['expected_output'],
                            'output': output,
                            'verdict': verdict
                        })
                        if verdict == "Passed":
                            passed += 1
                    except subprocess.TimeoutExpired:
                        verdict_details.append({
                            'input': case['input'],
                            'error': "Time Limit Exceeded"
                        })

            elif language == 'python':
                # Run Python code
                for case in testcases:
                    try:
                        result = subprocess.run(
                            [sys.executable, '-c', code],
                            input=case['input'],
                            capture_output=True,
                            text=True,
                            timeout=problem.time_limit
                        )
                        output = result.stdout.strip()
                        verdict = "Passed" if output == case['expected_output'].strip() else "Failed"
                        verdict_details.append({
                            'input': case['input'],
                            'expected': case['expected_output'],
                            'output': output,
                            'verdict': verdict
                        })
                        if verdict == "Passed":
                            passed += 1
                    except subprocess.TimeoutExpired:
                        verdict_details.append({
                            'input': case['input'],
                            'error': "Time Limit Exceeded"
                        })

            # Determine overall verdict
            if any('error' in detail for detail in verdict_details):
                overall_verdict = "Time Limit Exceeded"
            elif passed == len(testcases):
                overall_verdict = "Accepted"
            elif passed > 0:
                overall_verdict = "Partial Answer"
            else:
                overall_verdict = "Wrong Answer"

        except Exception as e:
            if overall_verdict == "Wrong Answer":
                overall_verdict = f"Runtime Error: {str(e)}"

        finally:
            # Clean up temporary files for C++
            if language == 'cpp':
                src_file_path.unlink(missing_ok=True)
                exec_file.unlink(missing_ok=True)

        # Save submission to database
        submission = Submission.objects.create(
            user=request.user,
            problem=problem,
            code=code,
            language=language,
            verdict=overall_verdict,
            # You might want to add more fields like execution_time, memory_usage, etc.
        )

        return JsonResponse({
            'submission_id': submission.id,
            'verdict': overall_verdict,
            'score': f"{passed}/{len(testcases)}",
            'details': verdict_details,
            'timestamp': submission.created_at.isoformat()
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)