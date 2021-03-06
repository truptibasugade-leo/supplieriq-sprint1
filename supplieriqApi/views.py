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
from supplieriqApi.serializers import VendorApiSerializer,VendorAddressSerializer,ItemApiSerializer,\
    ItemVendorApiSerializer,SignInAPISerializer,SupplierIQCompanyAPISerializer,SupplierIQVendorAPISerializer,\
    SupplierIQVendorAddressSerializer
from supplieriqmatch.utils import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import\
    get_user_model, authenticate, login as auth_login, logout as auth_logout
from django.http import Http404
from django.core import serializers
from django.http import HttpResponse
import json
# Create your views here.

class VendorsAPI(AuthenticatedUserMixin,APIView):
    """
    This API is used to render template having Vendor list or 
    if query parameter like 'id' is sent the it will render Vendor details
    """
    renderer_classes = (renderers.JSONRenderer,)
    
    def get_object(self, erp_vendor_code,company):
        try:
            obj = CompanyVendor.objects.get(erp_vendor_code=erp_vendor_code,company=company,is_deleted = False)
            return obj
        except CompanyVendor.DoesNotExist:
            raise Http404
    
    def get_vendoradress_object(self, pk):
        try:
            return VendorAddress.objects.get(vendor_id=pk)
        except CompanyVendor.DoesNotExist:
            raise Http404
    
    def get(self, request,*args, **kwargs):
        try:
            erp_vendor_code = request.query_params['erp_vendor_code']
            try:
                company= UserCompanyModel.objects.filter(user=request.user).first()
                obj = CompanyVendor.objects.get(erp_vendor_code=erp_vendor_code,company=company.company,is_deleted = False)
                serializer = VendorSerializer(obj)    
                return Response(serializer.data)
            except:
                return Response({"result":"Invalid request."})
        except:
            try:
                objs= UserCompanyModel.objects.filter(user=request.user).first()
                queryset = CompanyVendor.objects.filter(company_id = objs.company_id,is_deleted=False)
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
#             data.update({'vendorid':obj.id})
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
            erp_vendor_code = request.query_params['erp_vendor_code']
            company= UserCompanyModel.objects.filter(user=request.user).first()
            vendor_obj = self.get_object(erp_vendor_code,company.company)
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
            erp_vendor_code = request.query_params['erp_vendor_code']
            company= UserCompanyModel.objects.filter(user=request.user).first()
            vendor_obj = self.get_object(erp_vendor_code,company.company)
            try:
                addr_obj = self.get_vendoradress_object(vendor_obj.id)
                addr_obj.delete()
            except:
                pass
            vendor_obj.is_deleted = True
            vendor_obj.save()
            return Response({"result":"Successfully Deleted..!!"})
        except:
            return Response({"result":"Invalid request"})
        
class ItemsAPI(AuthenticatedUserMixin,APIView):
    """
    This API is used to render template having Vendor list or 
    if query parameter like 'id' is sent the it will render Vendor details
    """
    renderer_classes = (renderers.JSONRenderer,)
    
    def get_object(self, erp_item_code,company):
        try:
            return CompanyItem.objects.get(erp_item_code=erp_item_code,company=company,is_deleted=False)
        except CompanyItem.DoesNotExist:
            raise Http404
    
    def get_itemvendor_object(self, item_id):
        try:
            return ItemVendor.objects.filter(companyitem_id=item_id)
        except ItemVendor.DoesNotExist:
            raise Http404
        
    def get(self, request,*args, **kwargs):
        try:
            erp_item_code = request.query_params['erp_item_code']
            try:
                company= UserCompanyModel.objects.filter(user=request.user).first()
                obj = CompanyItem.objects.get(erp_item_code=erp_item_code,company=company.company)            
                serializer = ItemSerializer(obj)    
                return Response(serializer.data)
            except:
                return Response({"result":"Invalid Request."})
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
            try:
                for vendor in request.data['vendor']:
                    xx = ItemVendorApiSerializer(data={'companyitem':obj.id,'companyvendor':vendor})
                    xx.create(vendor,obj)
#                 data.update({'itemid':obj.id})
                return Response(data)
            except:
                return Response({"result":"Vendor Does not exists.."})
        else:
            print serializer.errors
            return Response(serializer.errors)
        
    def validate_params(self,request,item_obj):
        if request.has_key('target_price'):
            item_obj.target_price = int(request['target_price'])
        if request.has_key('name'):
            item_obj.name = request['name']
        if request.has_key('description'):
            item_obj.description = request['description']
        if request.has_key('erp_item_code'):
            item_obj.erp_item_code = int(request['erp_item_code'])
        item_obj.save()
        return True
    
    def put(self, request,*args,**kwargs):
        try:
            erp_item_code = request.query_params['erp_item_code']
            company= UserCompanyModel.objects.filter(user=request.user).first()
            item_obj = self.get_object(erp_item_code,company.company)
            if request.data:
                obj = self.validate_params(request.data,item_obj)
                if obj:
                    serializer = ItemApiSerializer(item_obj)
                    return Response({"result":serializer.data})
        except:
            return Response({"result":"Invalid request"})
        return Response({"result":"Invalid request"})
      
    def delete(self,request,*args,**kwargs):
        try:
            erp_item_code = request.query_params['erp_item_code']
            company= UserCompanyModel.objects.filter(user=request.user).first()
            item_obj = self.get_object(erp_item_code,company.company)
            item_obj.is_deleted = True
            item_obj.save()
            return Response({"result":"Successfully Deleted..!!"})
        except:
            return Response({"result":"Invalid request"})
        
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
            erp_item_code = request.query_params['erp_item_code']            
            qty = request.query_params['quantity']      
#             loc_id = request.query_params['company_address']      
#             loc = Location.objects.get(id = loc_id)  
#             lat1,long1 = get_lat_long(loc) 
            company= UserCompanyModel.objects.filter(user=request.user).first()
            itemobj = CompanyItem.objects.filter(erp_item_code=erp_item_code,is_deleted=False,company=company.company).first()  
            item_id = itemobj.id
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
                    v_c = ''
                fixed_cost = 0
                variable_cost = 0
                if f_c:
                    fixed_cost = calculate_fixed_cost(f_c)
                if v_c:
                    variable_cost = calculate_variable_cost(qty,v_c)

                if variable_cost != 0 and fixed_cost != 0 and item.companyvendor.is_deleted == False:
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


class SupplierIQCompanyApi(APIView):
    
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = SupplierIQCompanyAPISerializer 
    
    def get(self, request, *args, **kwargs):
        if request.data["call"] == "get":
            serializer = self.serializer_class(data=request.data)       
            if serializer.is_valid():
                try:
                    if serializer.validated_data.id:
                        if serializer.validated_data.is_deleted == False:
                            
                            response = Response(json.dumps({"result":"Added"}))
                        else:
                            
                            response = Response(json.dumps({"result":"Deleted"}))
                except:
                    
                    response = Response(json.dumps({"result":"DoesNotExists"}))
            else:
                response = Response({"errors":serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
            return response

        else:
            serializer = self.serializer_class(data=request.data)       
            if serializer.is_valid():
                try:
                    if serializer.validated_data.id:
                        if serializer.validated_data.is_deleted == False:
                            serializer.validated_data.is_deleted = True
                            response = Response(json.dumps({"result":"Deleted"}))
                        else:
                            serializer.validated_data.is_deleted = False
                            response = Response(json.dumps({"result":"Added"}))
                        serializer.validated_data.save()
                except:
                    obj = serializer.create(serializer.validated_data,request)
                    response = Response(json.dumps({"result":"Created"}))
            else:
                response = Response({"errors":serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
            return response

class SupplierIQVendorApi(APIView):
    
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = SupplierIQVendorAPISerializer 
    
    def check_if_obj_exists(self,obj,company):
        aa = []
        try:
            for x in obj:
                if x.company.supplieriq_id == company:
                    aa.append(x)
                
            return aa[0]
        except:
            return "NA"
    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)       
        if serializer.is_valid():
            try:
                result = self.check_if_obj_exists(serializer.validated_data,request.data['company_id'])
                if result.id:
                    if result.is_deleted == False and result.company.supplieriq_id == request.data['company_id']:                        
                        response = Response(json.dumps({"result":"Added"}))
                    else:                        
                        response = Response(json.dumps({"result":"Deleted"}))
            except:                
                response = Response(json.dumps({"result":"DoesNotExists"}))
        else:
            response = Response({"errors":serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
        return response

    def post(self,request,*args, **kwargs):
        query_data = dict(request.data)
        company = query_data.pop('company_id')
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():  
            try:
                result = self.check_if_obj_exists(serializer.validated_data,company[0])
                if result.id:
                    if result.is_deleted == False and result.company.supplieriq_id == company[0]:
                        result.is_deleted = True
                        response = Response(json.dumps({"result":"Deleted"}))
                    else:
                        result.is_deleted = False
                        response = Response(json.dumps({"result":"Added"}))
                    result.save()
            except:          
                data = serializer.data
                obj = serializer.create(serializer.validated_data,company[0])
                if obj == "Link the Company first with Purchase Smart.":
                    response = Response(json.dumps({"result":"Link the Company first with Purchase Smart."}))
                else:
                    address_set = [{"address1":query_data["address1"][0],"address2":query_data["address2"][0],\
                                    "city":query_data["city"][0],"state":query_data["state"][0],\
                                    "country":query_data["country"][0],"zipcode":query_data["zipcode"][0],\
                                   "longitude":query_data["longitude"][0],"latitude":query_data["latitude"][0],}]
                    xx = SupplierIQVendorAddressSerializer(data= address_set)
                    addr_obj = xx.create(address_set,obj)
                    response = Response(json.dumps({"result":"Created"}))
#             data.update({'vendorid':obj.id})
            
        else:
            response = Response({"errors":serializer.errors, 'status':status.HTTP_400_BAD_REQUEST})
        return response