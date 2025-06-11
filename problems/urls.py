from django.urls import path
from . import views

app_name = 'problems'

urlpatterns = [
    path('', views.problem_list, name='problem_list'),
    path('<int:problem_id>/', views.problem_detail, name='problem_detail'),
    path('run_code/<int:problem_id>/', views.run_code_api, name='run_code_api'),
    path('submit_code/<int:problem_id>/', views.submit_code_api, name='submit_code_api'),
    path('ai-review/<int:problem_id>/', views.ai_code_review, name='ai_review_api'),  # <-- added AI review API
    path('profile/', views.profile_view, name='profile'),
    path('my-submissions/', views.user_submissions, name='user_submissions'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
