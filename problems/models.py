from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class Problem(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)  # Add this
    updated_at = models.DateTimeField(auto_now=True)     # Add this
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Add this
    time_limit = models.IntegerField(default=1)  # in seconds
    memory_limit = models.IntegerField(default=256)  # in MB
    input_description = models.TextField(help_text="Description of input format")
    output_description = models.TextField(help_text="Description of output format")
    sample_input = models.TextField(blank=True)
    sample_output = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)  # Add this

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    # problems/models.py (add this at the bottom)
# class Submission(models.Model):
#     LANGUAGE_CHOICES = [
#         ('python', 'Python'),
#         ('cpp', 'C++'),
#     ]
    
#     problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     code = models.TextField()
#     language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES)
#     verdict = models.CharField(max_length=50, default='Pending')
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.user.username}'s submission for {self.problem.title}"
class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    code = models.TextField()
    language = models.CharField(max_length=20)
    verdict = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {self.verdict}"
    
import os

class TestCase(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='testcases')
    input_data = models.TextField(help_text="Enter the input for the test case")
    expected_output = models.TextField(help_text="Enter the expected output")
    is_sample = models.BooleanField(default=False, help_text="Is this a sample test case?")

    def __str__(self):
        return f"TestCase for {self.problem.title} (Sample: {self.is_sample})"


