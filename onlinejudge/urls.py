from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views
from problems import views as problem_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', account_views.register, name='register'),
    path('login/', account_views.login_view, name='login'),
    path('logout/', account_views.logout_view, name='logout'),
    path('problems/', include('problems.urls')),  # All problem-related URLs
    path('', problem_views.home, name='home'),  # Main homepage
]