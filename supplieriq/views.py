import json
import datetime
from django.utils import timezone
from django.contrib.auth import\
    get_user_model, authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.core.urlresolvers import reverse
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import parsers, renderers, status, viewsets,generics
from rest_framework.authentication import get_authorization_header
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from django.middleware.csrf import rotate_token
from django.contrib import messages
import time
from django.utils.http import cookie_date
from django.core.cache import cache
from django.contrib.auth.models import Group
from supplieriq.serializers import SignInSerializer,VendorSerializer,ItemSerializer
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework.renderers import TemplateHTMLRenderer
from supplieriq.models import Vendor,Company, Item
from django.shortcuts import render_to_response


class ObtainAuthToken(APIView):

    """
    This API is used to authenticated the user with provided credentials.
    """

    throttle_classes = ()
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (AllowAny,)
    parser_classes = (
        parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
    serializer_class = SignInSerializer  # AuthTokenSerializer
    model = Token
    template_name = 'login.html'
    
    def get(self, request):
        serializer = self.serializer_class()
        if request.user.is_authenticated():
            token, created = Token.objects.get_or_create(user=request.user)  
            return Response({'serializer': serializer,'token': token.key,'userid': request.user.id,}, template_name='home.html')
        
        return Response({'serializer': serializer})
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)       
        if serializer.is_valid():
            user = serializer.instance            
            token, created = Token.objects.get_or_create(user=user)  
            new_user = authenticate(username=user.username, password=request.data.get('password'))
            auth_login(request, new_user)
            response = Response({'serializer':serializer.data,'token': token.key,
                                 'userid': user.id,
            }, template_name='home.html')
#             response.set_cookie('authorization', token.key, max_age=MAX_AGE, expires=EXPIRES)
#             response.set_cookie('authenticate', token.key, max_age=MAX_AGE, expires=EXPIRES)        
        else:
            try:
                #for website
                x = request.data['csrfmiddlewaretoken'] 
                response = Response({'serializer':serializer,'errors':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
            except:
                # for API
                response = Response({'errors':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
        return response

class SignoutUser(APIView):

    """
    This API is used to logout the authenticatde user.
    """

    throttle_classes = ()
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (AllowAny,)
    parser_classes = (
        parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
    serializer_class = SignInSerializer  # AuthTokenSerializer
    model = Token
    template_name = 'login.html'
    
    def get(self, request):
        serializer = self.serializer_class()
        if request.user.is_authenticated():
            auth_logout(request)
        
        return Response({'serializer': serializer})
        
# class VendorsAPI(viewsets.ModelViewSet):
class VendorsAPI(APIView):
    """
    This API is used to render template having Vendor list or 
    if query parameter like 'id' is sent the it will render Vendor details
    """
    
#     serializer_class = VendorSerializer  # AuthTokenSerializer
#     template_name = 'vendor_list.html'
    renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
    def get(self, request,*args, **kwargs):
        try:
            vendor_id = request.query_params['id']
            obj = Vendor.objects.get(id=vendor_id)
            serializer = VendorSerializer(obj)    
            return Response({'serializer':serializer.data},template_name="vendor/vendor_details.html")
        except:
            queryset = Vendor.objects.all()
            renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
            serializer = VendorSerializer(queryset, many=True)     
            return Response({'serializer':serializer.data},template_name="vendor/vendor_list.html")
     
    
    '''
    model = Vendor
    serializer_class = VendorSerializer
    template_name = 'vendor_list.html'
    queryset =  Vendor.objects.all()

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(self.object_list, many=True)
        return Response(serializer.data)
    
    '''        
        
class ItemsAPI(APIView):
    """
    This API is used to render template having Item list or 
    if query parameter like 'id' is sent the it will render Item details
    """
    
    renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
    def get(self, request,*args, **kwargs):
        try:
            item_id = request.query_params['id']
            obj = Item.objects.get(id=item_id)
            serializer = ItemSerializer(obj)    
            return Response({'serializer':serializer.data},template_name="item/item_details.html")
        except:
            queryset = Item.objects.all()
            renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
#             import ipdb;ipdb.set_trace()
            serializer = ItemSerializer(queryset, many=True)     
            return Response({'serializer':serializer.data},template_name="item/item_list.html")
     