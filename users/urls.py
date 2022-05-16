from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('edit_profile/<str:pk>/', views.edit_profile, name='edit-profile'),
    path('logout/', views.user_logout, name='logout'),
    path('search_result_profiles/', views.search_results_profiles, name='search-result-profiles'),
    path('follow/<str:pk>/', views.follow, name='follow'),
    path('followers/<str:pk>/', views.view_followers, name='followers'),
    path('following/<str:pk>/', views.view_following, name='following'),
    path('delete_profile/<str:pk>/', views.delete_profile, name='delete-profile'),
]