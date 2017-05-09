from django.contrib.auth.models import AnonymousUser
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import exceptions



class AuthenticatedUserMixin(object):
    """
    Purpose: Mixin for authenticating user based on token provided
    """

    def perform_authentication(self, request):
        if 'HTTP_AUTHORIZATION' in request.META:
            key = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]
            try:
                user = Token.objects.get(key=key).user
                request.user = user
            except Token.DoesNotExist:
                raise exceptions.AuthenticationFailed('Invalid token')            
        else:
            raise exceptions.AuthenticationFailed('Access Denied')