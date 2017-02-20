from .labels import LBL_USER, PLACEHOLDER_USER, DOB_HELP_TEXT, WORK_TITLE, \
    EDUCATION_TITLE, WORK_ENTRY, EDUCATION_ENTRY, FORGOT_LINK, ACTIVATION_LINK, \
    WORK_IS_PRESENT, EDUCATION_IS_PRESENT, TITLE_PLACEHOLDER, \
    USER_ENTRY_PLACEHOLDER, CONTACT_NAME, PERSON_MANAGING_ACC, EMAIL_ADDRESS, \
    SEARCH_LOCAL_OR_NATIONAL, INVITE_EMAIL, WORKING_LABEL, CONTACT_PHONE, CONTACT_NUMBER, SITE_NAME, \
    REVIEWS_SETTING_DETAILS, REVIEWS_ANONYMOUS_DETAILS
from captcha.fields import CaptchaField, CaptchaTextInput
from crispy_forms.layout import Layout, HTML, Div, Fieldset
from django import forms
from django.contrib.auth import get_user_model
from django.forms import widgets
from django.forms.widgets import TextInput
from django.utils.translation import ugettext as _
from supplieriq.constants import (GENDERS, ATTRS_DICT_FIRST_NAME,
                                     ATTRS_DICT_LAST_NAME, ATTRS_DICT_EMAIL, ATTRS_DICT_EMAIL2, ATTRS_DICT_PASSWORD1,
                                     PASSWORD_MIN_LENGTH, ATTRS_DICT_PASSWORD2, ATTRS_DICT_CAPTCHA, ATTRS_DICT_DOB,
                                     ATTRS_DICT, ZIPCODE_MIN_LENGTH, ZIPCODE_MAX_LENGTH, ATTRS_DICT_ZIPCODE, USER_ZIPCODE_MAX_LENGTH,
                                     ATTRS_DICT_IDENTIFICATION, MIN_YEAR, MAX_YEAR, COUNTRIES,
                                     )
from reviews.forms import GenericForm, GenericModelForm

from reviews.models import UserEntries
from reviews.business.labels import LBL_COUNTRY
from reviews.users.operations import get_privacy_settings, get_username_choices
from datetime import datetime
from crispy_forms.helper import FormHelper
from .messages import ERROR_TOS
from .widgets import NgModelCheckboxSelectMultiple as NgmodelMultipleCheckBoxWidget
from reviews.users.labels import CONNECTIONS_ADD
User = get_user_model()
PASSWORD_MAX_LENGTH = User._meta.get_field('password').max_length

class LoginForm(GenericForm):

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
    
