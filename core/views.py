from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.middleware.csrf import get_token

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.http import JsonResponse
import json


def get_csrf(request):
    response = JsonResponse({'detail': 'CSRF cookie set'})
    response['X-CSRFToken'] = get_token(request)
    return response

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):

    permission_classes = (permissions.AllowAny, )

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        response = Response()

        response.set_cookie(get_token(request))
        # print(get_token(request))

        return Response({'csrfToken': get_token(request)})



@method_decorator(csrf_protect, name="dispatch")
class RegisterUserView(APIView):

    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        if self.request.data['email'] and self.request.data['username'] and self.request.data['password'] and self.request.data['password'] == self.request.data['confirmPass']:

            if User.objects.filter(username=self.request.data['username']).exists():
                return Response({'success': False, 'message': "User already exists"})
            else:
                user = User.objects.create_user(username=self.request.data['username'], email=self.request.data['email'], password=self.request.data['password'])
                user.save()
                return Response({'success': True, 'message': 'User successfully created'})

        return Response({'success': False, 'message': 'User already exist or password did not match'})


@method_decorator(csrf_protect, name="dispatch")
class LoginView(APIView):

    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        userData = request.data
        if userData and userData['username'] and userData['password'] and userData['email']:
            user = authenticate(request, username=userData['username'], password=userData['password'])
            if user is not None:
                login(request, user)
                return Response({'success': True, 'message': 'Success', 'usename': user.username, 'email': user.email})
            else:
                return Response({'success': False, 'message': 'Incorrect credentials'})

        return Response({'success': False, 'message': 'Incorrect credentials'})

@method_decorator(csrf_protect, name='dispatch')
class CheckAuthenticated(APIView):

    def get(self, request):
        try:
            isAuthenticated = request.user.is_authenticated
            if isAuthenticated:
                return Response({'username': request.user.username, 'isAuthenticated': True})
            else:
                return Response({'isAuthenticated': 'error'})
        except:
            return Response({'error': 'Something went wrong when checking authentication status'})

@method_decorator(csrf_protect, name='dispatch')
class LogoutView(APIView):
    def get(self, request, format=None):
        try:
            logout(request)
            return Response({ 'success': True })
        except:
            return Response({ 'error': 'Something went wrong when logging out' })


