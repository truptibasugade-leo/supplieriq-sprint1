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
from supplieriqApi.serializers import VendorApiSerializer,VendorAddressSerializer,ItemApiSerializer,ItemVendorApiSerializer
from supplieriqmatch.utils import *
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
            import ipdb;ipdb.set_trace()
            data = serializer.data
            obj = serializer.create(serializer.validated_data,request)
            xx = VendorAddressSerializer(data= request.data['address_set'])
            addr_obj = xx.create(request.data['address_set'],obj)
            data.update({'vendorid':obj.id})
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

