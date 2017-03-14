from .labels import LBL_USER
from django import forms
from django.contrib.auth import get_user_model
from django.forms import widgets
from django.forms.widgets import TextInput
from django.utils.translation import ugettext as _
from supplieriq.constants import (ATTRS_DICT_PASSWORD1,PASSWORD_MIN_LENGTH,ATTRS_DICT_IDENTIFICATION
from django.forms import ModelForm, Form                           )
from reviews.forms import GenericForm, GenericModelForm

from datetime import datetime
User = get_user_model()
PASSWORD_MAX_LENGTH = User._meta.get_field('password').max_length

class LoginForm(Form):

    """
    Purpose: Login form for user.
    Methods Supported: Get & Post.
    """
    email = forms.EmailField(
        label=LBL_USER['EMAIL'],
        max_length=User._meta.get_field('email').max_length,
        widget=forms.TextInput(attrs=ATTRS_DICT_IDENTIFICATION),
    )
    password = forms.CharField(
        label=LBL_USER['PASSWORD'],
        widget=widgets.PasswordInput(attrs=ATTRS_DICT_PASSWORD1),
        min_length=PASSWORD_MIN_LENGTH,
        max_length=PASSWORD_MAX_LENGTH,
    )
    
