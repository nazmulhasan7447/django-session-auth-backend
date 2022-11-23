from django.contrib import admin
from django.urls import path, include
from .views import GetCSRFToken, RegisterUserView, LoginView, CheckAuthenticated, LogoutView
from . import views


urlpatterns = [
    path('get-csrf-token/', GetCSRFToken.as_view(), name='getCsrfToken'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login-user/', LoginView.as_view(), name='login'),
    path('logout-user/', LogoutView.as_view(), name='logout'),
    path('check-authenticated/', CheckAuthenticated.as_view(), name='checkAuthenticated'),
    # path('check-authenticated/', views.CheckAuthenticated, name='checkAuthenticated'),

    path('api/csrf/', views.get_csrf, name='get_csrf'),
]
