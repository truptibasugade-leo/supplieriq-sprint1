from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import parsers, renderers, status, viewsets,generics
from rest_framework.renderers import TemplateHTMLRenderer
from supplieriq.models import CompanyVendor,Company, CompanyItem, VendorAddress,Price,FixedCost,VariableCost,\
    ItemVendor,Location,UserCompanyModel,PurchaseOrder,ItemReceipt
from supplieriq.serializers import SignInSerializer,VendorSerializer,ItemSerializer,\
    ItemVendorSerializer,CostSerializer,FixedCostSerializer,VariableCostSerializer
from rest_framework.response import Response
from supplieriqApi.utils import AuthenticatedUserMixin
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from supplieriqApi.serializers import VendorApiSerializer,VendorAddressSerializer,ItemApiSerializer
# Create your views here.

class VendorsAPI(AuthenticatedUserMixin,APIView):
    """
    This API is used to render template having Vendor list or 
    if query parameter like 'id' is sent the it will render Vendor details
    """
    renderer_classes = (renderers.JSONRenderer,)
    def get(self, request,*args, **kwargs):
        try:
            vendor_id = request.query_params['id']
            obj = CompanyVendor.objects.get(id=vendor_id)
            serializer = VendorSerializer(obj)    
            return Response(serializer.data)
        except:
            try:
                objs= UserCompanyModel.objects.filter(user=request.user).first()
                queryset = CompanyVendor.objects.filter(company_id = objs.company_id)
            except:
                queryset = CompanyVendor.objects.all()            
            renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
            serializer = VendorSerializer(queryset, many=True)     
            return Response(serializer.data)
    
    def post(self,request,*args, **kwargs):
        serializer = VendorApiSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            obj = serializer.create(serializer.validated_data,request)
            xx = VendorAddressSerializer(data= request.data['address_set'])
            addr_obj = xx.create(request.data['address_set'],obj)
            print data
            return Response(data)
        else:
            print serializer.errors
            return Response(serializer.errors)

class ItemsAPI(AuthenticatedUserMixin,APIView):
    """
    This API is used to render template having Vendor list or 
    if query parameter like 'id' is sent the it will render Vendor details
    """
    renderer_classes = (renderers.JSONRenderer,)
    def get(self, request,*args, **kwargs):
        try:
            item_id = request.query_params['id']
            obj = CompanyItem.objects.get(id=item_id)            
            serializer = ItemSerializer(obj)    
            return Response(serializer.data)
        except:
            try:
                objs= UserCompanyModel.objects.filter(user=request.user).first()
                queryset = CompanyItem.objects.filter(company_id = objs.company_id)
            except:
                queryset = CompanyItem.objects.all()           
            renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
            serializer = ItemSerializer(queryset, many=True)         
            return Response(serializer.data)
    
    