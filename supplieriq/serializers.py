
import random
from django.utils import timezone
try:
    from hashlib import sha1 as sha_constructor
except ImportError:
    from django.utils.hashcompat import sha_constructor
from django.db.models import Q
from django.contrib.auth.models import User

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate, get_user_model, login
from django.forms import widgets
from django.contrib.auth.models import Group
from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator
from django.core.paginator import Page
from django.core.serializers.json import DjangoJSONEncoder
import logging
from supplieriq.models import Vendor,Company

logger = logging.getLogger('file_debug_log')

User = get_user_model()
PASSWORD_MAX_LENGTH = User._meta.get_field('password').max_length
EMAIL_MAX_LENGTH = User._meta.get_field('email').max_length

from datetime import datetime

class SignInSerializer(serializers.Serializer):

    """
    Purpose: To handle validations and populate sign in details.
    Methods Supported: Get & Post.
    """
    email = serializers.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        style={'placeholder': 'Email', 'autofocus': True}
    )
    password = serializers.CharField(
        max_length=PASSWORD_MAX_LENGTH,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
#     email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)
# # 
#     password = serializers.CharField(max_length=PASSWORD_MAX_LENGTH)

    def validate(self, attrs):
        """
        Purpose: To validate signin serializers.
        :param self: Context Object
        :param attrs: Dictionary containing the key as field name & it's value
        :param source: Field name
        Constraints:
        User account should be present and should be active.
        :returns: attrs in case of valid inputs else error message
        """
        
        try:
            user = User.objects.get(email=attrs.get('email'))  

            if user.check_password(attrs.get('password')):
                self.instance = user
            else:
                error = "Invalid credentials. Note that both fields are case-sensitive."
                raise serializers.ValidationError(error)                           
        except:
            error = "Invalid credentials. Note that both fields are case-sensitive."
            raise serializers.ValidationError(error)
            
#         user = authenticate(email=attrs.get('email'),password=attrs.get('password'))
#         if user is not None and user.is_active:
#             self.instance = user
#         else:
#             error = "Invalid credentials. Note that both fields are case-sensitive."
#             raise serializers.ValidationError(error)
#             

        return attrs

class VendorSerializer(serializers.Serializer):

    """
    Used for indexing only.
    """
    vendorid = serializers.SerializerMethodField('get_vendor_id')
    name = serializers.CharField(read_only=True)
#     company = serializers.PrimaryKeyRelatedField(read_only=True)
    erp_vendor_code = serializers.CharField(read_only=True)
    address = serializers.CharField(read_only=True)
    phone = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    
    class Meta(object):
        model = Vendor
        fields = (
            'vendorid','name', 'erp_vendor_code','phone','address', 'email',
        )
    
    def get_vendor_id(self, obj):
        return obj.id;
    
class ItemSerializer(serializers.Serializer):

    """
    Used for indexing only.
    """
    itemid = serializers.SerializerMethodField('get_item_id')
    name = serializers.CharField(read_only=True)
    erp_item_code = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    vendor = VendorSerializer(read_only=True, many=True)
    
    class Meta(object):
        model = Vendor
        fields = (
            'itemid','name', 'erp_item_code','description',
        )
    
    def get_item_id(self, obj):
        return obj.id;
    
