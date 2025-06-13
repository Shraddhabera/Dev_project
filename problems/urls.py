# from django.urls import path
# from . import views

# app_name = 'problems'

# urlpatterns = [
#     path('', views.problem_list, name='problem_list'),
#     path('<int:problem_id>/', views.problem_detail, name='problem_detail'),
#     path('run_code/<int:problem_id>/', views.run_code_api, name='run_code_api'),
#     path('submit_code/<int:problem_id>/', views.submit_code_api, name='submit_code_api'),
#     path('ai-review/<int:problem_id>/', views.ai_code_review, name='ai_review_api'),  # <-- added AI review API
#     path('profile/', views.profile_view, name='profile'),
#     path('my-submissions/', views.user_submissions, name='user_submissions'),
#     path('leaderboard/', views.leaderboard, name='leaderboard'),
# ]


from django.urls import path
from . import views

app_name = 'problems'

urlpatterns = [
    path('', views.problem_list, name='problem_list'),
    path('<int:problem_id>/', views.problem_detail, name='problem_detail'),
    
    # API endpoints
    path('run/<int:problem_id>/', views.run_code, name='run_code'),
    path('run-all/<int:problem_id>/', views.run_all_testcases, name='run_all_testcases'),
    path('submit/<int:problem_id>/', views.submit_code, name='submit_code'),
    path('ai-review/<int:problem_id>/', views.ai_code_review, name='ai_review'),
    
    # User-related paths
    path('profile/', views.profile_view, name='profile'),
    path('submissions/', views.user_submissions, name='user_submissions'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('leaderboard/api/', views.leaderboard_api, name='leaderboard_api'),
]