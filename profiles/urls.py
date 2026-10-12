from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('manage/', views.manage, name='manage'),
    path('delete/<str:kind>/<int:pk>/', views.delete_item, name='delete_item'),
    path('u/<str:username>/', views.public_profile, name='public_profile'),
]
