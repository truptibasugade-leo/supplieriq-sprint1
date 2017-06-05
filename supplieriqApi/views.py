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
from supplieriqApi.serializers import VendorApiSerializer,VendorAddressSerializer,ItemApiSerializer,ItemVendorApiSerializer,SignInAPISerializer
from supplieriqmatch.utils import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import\
    get_user_model, authenticate, login as auth_login, logout as auth_logout
from django.http import Http404
from django.core import serializers
# Create your views here.

class VendorsAPI(AuthenticatedUserMixin,APIView):
    """
    This API is used to render template having Vendor list or 
    if query parameter like 'id' is sent the it will render Vendor details
    """
    renderer_classes = (renderers.JSONRenderer,)
    
    def get_object(self, pk):
        try:
            return CompanyVendor.objects.get(pk=pk)
        except CompanyVendor.DoesNotExist:
            raise Http404
    
    def get_vendoradress_object(self, pk):
        try:
            return VendorAddress.objects.get(vendor_id=pk)
        except CompanyVendor.DoesNotExist:
            raise Http404
    
        
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
            data.update({'vendorid':obj.id})
            return Response(data)
        else:
            print serializer.errors
            return Response(serializer.errors)
    
    def validate_params(self,request,vendor_obj):
        if request.has_key('phone'):
            vendor_obj.phone = int(request['phone'])
        if request.has_key('name'):
            vendor_obj.name = request['name']
        if request.has_key('email'):
            vendor_obj.email = request['email']
        if request.has_key('erp_vendor_code'):
            vendor_obj.erp_vendor_code = int(request['erp_vendor_code'])
        vendor_obj.save()
        if request.has_key('address_set'):
            if vendor_obj.vendoraddress_set.count() == 0:
                try:
                    xx = VendorAddressSerializer(data= request['address_set'])
                    addr_obj = xx.create(request['address_set'],vendor_obj)
                except:
                    pass
            else:
                address = VendorAddress.objects.get(vendor_id=vendor_obj.id)
                addr_set = request['address_set'][0]
                if addr_set.has_key('address1'):
                    address.address1 = addr_set['address1']
                if addr_set.has_key('address2'):
                    address.address2 = addr_set['address2']
                if addr_set.has_key('city'):
                    address.city = addr_set['city']
                if addr_set.has_key('state'):
                    address.state = addr_set['state']
                if addr_set.has_key('country'):
                    address.country = addr_set['country']
                if addr_set.has_key('zipcode'):
                    address.zipcode = addr_set['zipcode']
                address.save()        
        return True
    
    def put(self, request,*args,**kwargs):
        try:
            vendor_id = request.query_params['id']
            vendor_obj = self.get_object(vendor_id)
            if request.data:
                obj = self.validate_params(request.data,vendor_obj)
                if obj:
                    serializer = VendorSerializer(vendor_obj)
                    return Response({"result":serializer.data})
        except:
            return Response({"result":"Invalid request"})
        return Response({"result":"Invalid request"})
    
    def delete(self,request,*args,**kwargs):
        try:
            vendor_id = request.query_params['id']
            addr_obj = self.get_vendoradress_object(vendor_id)
            addr_obj.delete()
            vendor_obj = self.get_object(vendor_id)
            vendor_obj.delete()
            return Response({"result":"Successfully Deleted..!!"})
        except:
            return Response({"result":"Invalid request"})
        
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
    
    def post(self,request,*args, **kwargs):
        serializer = ItemApiSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            obj = serializer.create(serializer.validated_data,request)
            xx = ItemVendorApiSerializer(data= request.data['vendor'])
            item_vendor = xx.create(request.data['vendor'],obj)
            print data
            return Response(data)
        else:
            print serializer.errors
            return Response(serializer.errors)

class SigninApi(APIView):
    
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = SignInAPISerializer 

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)       
        if serializer.is_valid():
            user = serializer.instance            
            token, created = Token.objects.get_or_create(user=user)  
#             new_user = authenticate(username=user.username, password=request.data.get('password'))
#             auth_login(request, new_user)
            vv =user.usercompanymodel_set.first()
            response = Response({'serializer':serializer.data,'token': token.key,
                                 'userid': user.id,'company':vv.company.name
            })
        else:
            response = Response({'errors':serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
        return response

class SignInOutApi(APIView):
    pass
    
class RunMatchAPI(AuthenticatedUserMixin,APIView):
    
    renderer_classes = (renderers.JSONRenderer,)
    def get(self, request,*args, **kwargs):   
        try:    
            cost = {}
            item_id = request.query_params['item']            
            qty = request.query_params['quantity']      
#             loc_id = request.query_params['company_address']      
#             loc = Location.objects.get(id = loc_id)  
#             lat1,long1 = get_lat_long(loc)    
            obj = ItemVendor.objects.filter(companyitem_id = item_id)
            qq = []
            for item in obj:   
                try:             
                    f_c = item.fixedcost_set.all()
                except:
                    f_c = ''
                try:
                    v_c = item.variablecost_set.all()
                except:
                    v_c= ''
                fixed_cost = 0
                variable_cost = 0
                if f_c:
                    fixed_cost = calculate_fixed_cost(f_c)
                if v_c:
                    variable_cost = calculate_variable_cost(qty,v_c)

                if variable_cost != 0 and fixed_cost != 0:
                    zzzz=request.user.usercompanymodel_set.all()
                    qqq =zzzz[0]
                    if qqq.company == item.companyvendor.company:
                        total= round(fixed_cost,2) + round(variable_cost,2)                
                        serializer = VendorSerializer(item.companyvendor)
                        
                        # find distance
                        v_addr = item.companyvendor.vendoraddress_set.first()
#                         lat2,long2 = get_lat_long(v_addr)                        
#                         if lat1 and long1 and lat2 and long2:
#                             dist = distance(lat1,long1,lat2,long2)
#                         else:
#                             if lat1=='' or long1=='':
#                                 dist = 'Incorrect Company Address..!!'
#                             else:
#                                 dist = 'Incorrect Vendor Address..!!'
                        
                        zz = serializer.data                    
                        zz.update({"total price":float(total)})
#                         zz.update({"distance":dist})

                        # find quality
#                         quality = calculate_quality(item)

                        #find delay
#                         delay = calculate_delay_time(item)
                        
#                         zz.update({"quality":quality})
#                         zz.update({"delivery delay":delay})
                        zz.update({"itemvendor":item.id})
                    
                        qq.append(zz)
            newlist = sorted(qq, key=lambda k: k['total price']) 
            return Response({'result':newlist})
        except:
            return Response({'result':'No Results Found'})

