from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class BasicBackend:
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

class EmailAuthBackEnd(ModelBackend):
    def authenticate(self, email=None, password=None,**kwargs):
        try:
            user = User.objects.get(email=email)  

            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None