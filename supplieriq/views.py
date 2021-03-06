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
from supplieriq.serializers import SignInSerializer,VendorSerializer,ItemSerializer, \
    ItemVendorSerializer,CostSerializer,FixedCostSerializer,VariableCostSerializer, \
    PurchaseOrderSerializer,ItemReceiptSerializer
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework.renderers import TemplateHTMLRenderer
from supplieriq.models import CompanyVendor,Company, CompanyItem, VendorAddress,Price, \
    FixedCost,VariableCost,ItemVendor,UserCompanyModel,PurchaseOrder,ItemReceipt
from django.shortcuts import render_to_response
import uuid 
from django.conf import settings
from django.core.mail.message import EmailMessage
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect

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
    serializer_class = SignInSerializer 
    model = Token
    template_name = 'login.html'
    
    def get(self, request):
        serializer = self.serializer_class()
        if request.user.is_authenticated():
            token, created = Token.objects.get_or_create(user=request.user)  
            vv =request.user.usercompanymodel_set.first()
            return Response({'serializer': serializer,'token': token.key,'userid': request.user.id,'company':vv.company.name}, template_name='home.html')
        
        return Response({'serializer': serializer})
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)       
        if serializer.is_valid():
            user = serializer.instance            
            token, created = Token.objects.get_or_create(user=user)  
            new_user = authenticate(username=user.username, password=request.data.get('password'))
            auth_login(request, new_user)
            vv =request.user.usercompanymodel_set.first()
            response = Response({'serializer':serializer.data,'token': token.key,
                                 'userid': user.id,'company':vv.company.name
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
            obj = CompanyVendor.objects.get(id=vendor_id,is_deleted=False)
            serializer = VendorSerializer(obj)    
            return Response({'serializer':serializer.data},template_name="vendor/vendor_details.html")
        except:
            try:
                objs= UserCompanyModel.objects.filter(user=request.user).first()
                queryset = CompanyVendor.objects.filter(company_id = objs.company_id,is_deleted=False)
            except:
                queryset = CompanyVendor.objects.all()            
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
            obj = CompanyItem.objects.get(id=item_id,is_deleted=False)            
            serializer = ItemSerializer(obj)  
            return Response({'serializer':serializer.data},template_name="item/item_details.html")
        except:
            try:
                objs= UserCompanyModel.objects.filter(user=request.user).first()
                queryset = CompanyItem.objects.filter(company_id = objs.company_id,is_deleted=False)
            except:
                queryset = CompanyItem.objects.all()
            renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
            serializer = ItemSerializer(queryset, many=True)     
            return Response({'serializer':serializer.data},template_name="item/item_list.html")
        
    
class CostAPI(APIView):
    renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
    def post(self, request,*args, **kwargs):
        v_id = request.data.get('vendor_id')
        i_id = request.data.get('item_id')
        if v_id:
            # To add new fixed cost and variable cost
            price = request.data.get('price')
            objs=ItemVendor.objects.filter(companyvendor_id = v_id , companyitem_id = i_id)     
            price_type = request.data.get('price_type')
            d = request.data.copy()            
            if price_type:
                for x in objs:
                   
                    o = FixedCostSerializer(data=request.data)
                    if o.is_valid():
                        f_c_obj = FixedCost(itemvendor=x,cost_type=price_type,cost=price)
                        f_c_obj.save()
                    else:
                        err = o.errors
                        err.update({"status":"error"})
                        return Response(json.dumps(err))

            else:
                quantity = request.data.get('quantity')
                for x in objs:
                    d.update({"itemvendor":x})
                    o = VariableCostSerializer(data=d)
                    if o.is_valid():
                        v_c_obj = VariableCost(itemvendor=x,quantity=quantity,cost=price)
                        v_c_obj.save()
                    else:
                        err = o.errors
                        err.update({"status":"error"})
                        return Response(json.dumps(err))
                    
            return Response(json.dumps(request.data))
        else:    
            # To update existing fixed cost and variable cost       
            price_type = request.data.get('price_type')
            quantity = request.data.get('quantity')
            price = request.data.get('price')
            
            if price_type:
                id = request.data.get('fixedcost_id')      
                o = FixedCostSerializer(data=request.data)      
                if o.is_valid():
                    f_c_obj = FixedCost.objects.get(id=id)
                    f_c_obj.cost_type = price_type
                    f_c_obj.cost = price
                    f_c_obj.save()
                else:
                    err = o.errors
                    err.update({"status":"error"})
                    return Response(json.dumps(err))
            else:
                d = request.data.copy()    
                id = request.data.get('variablecost_id')     
                v_c_obj = VariableCost.objects.get(id=id)
                d.update({"itemvendor":v_c_obj.itemvendor})
                o = VariableCostSerializer(data=d)
                if o.is_valid():                    
                    v_c_obj.quantity = quantity
                    v_c_obj.cost = price
                    v_c_obj.save()
                else:
                    err = o.errors
                    err.update({"status":"error"})
                    return Response(json.dumps(err))
            return Response(json.dumps(request.data))
        
    def delete(self,request):
        v_id = request.data.get('variablecost_id')
        f_id = request.data.get('fixedcost_id')
        if f_id:
            ob = FixedCost.objects.get(id = f_id)
            ob.delete()
        else:
            ob =VariableCost.objects.get(id = v_id)
            ob.delete()
        return Response({'serializer':'Data has been deleted successfully.'})
    
class RunMatchAPI(APIView):
    
    renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
    def get(self, request,*args, **kwargs):   
        try:    
            cost = {}
            itemvendor = request.query_params['itemvendor']            
            qty = request.query_params['quantity']            
            obj = ItemVendor.objects.get(id = itemvendor)
            f_c = obj.fixedcost_set.all()
            v_c = obj.variablecost_set.all()
            fixed_cost = 0
            variable_cost = 0
            if f_c:
                for x in f_c:
                    fixed_cost += float(x.cost)
                    cost[str(x.cost_type)] = float(x.cost)
            if v_c:
                try:
                    val = v_c.values_list('quantity','cost')
                    cc =filter(lambda x: float(x[0]) <= float(qty),val)
                    m = max( [ float(x[0]) for x in cc])
                    closest =[b for b in cc if float(b[0]) == m]
                    variable_cost = float(closest[0][1]) * float(qty)
                except:
                    val = v_c.values_list('quantity','cost')
                    cc =filter(lambda x: float(x[0]) >= float(qty),val)
                    m = min( [ float(x[0]) for x in cc])
                    closest =[b for b in cc if float(b[0]) == m]
                    variable_cost = float(closest[0][1]) * float(qty)
                cost['Price (per unit)'] = closest[0][1]
            total= round(fixed_cost,2) + round(variable_cost,2)
            cost['Quantity'] = qty            
            cost['Fixed Price'] = round(fixed_cost,2)
            cost['Variable Price'] =round(variable_cost,2)
            cost[ 'Total']=float(total)
            return Response(json.dumps(cost))
        except:
            try:
                zzzz=request.user.usercompanymodel_set.all()
                company_address = zzzz[0].company.location_set.all()
                qqq =zzzz[0]
                queryset = CompanyItem.objects.filter(company=qqq.company)
                return Response({'serializer':queryset,'company_address':company_address},template_name="run_match.html")
            except:
                return HttpResponseRedirect("/")
class QuoteAPI(APIView):
    renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
    
    def get(self, request,*args, **kwargs):        
        try:
            v_id = request.query_params['vendorid']
            i_id = request.query_params['itemid']
            action = request.query_params['action']
            i_obj = CompanyItem.objects.get(id= i_id)
            v_obj = CompanyVendor.objects.get(id= v_id)
            v_i_id = ItemVendor.objects.get(companyvendor=v_id,companyitem=i_id)
            v_obj.send_quote_id = uuid.uuid4()
            v_obj.link_expiration_date = datetime.datetime.now()
            v_obj.save()
            domain = request.META['HTTP_HOST']
            if action == 'open modal':
                if domain == '172.16.0.109:8000':
                    link = 'http://'+str(domain)+'/quote/?vendoritem='+str(v_i_id.id)+'&send_quote_id='+str(v_obj.send_quote_id)
                else:
                    link = 'https://'+str(domain)+'/quote/?vendoritem='+str(v_i_id.id)+'&send_quote_id='+str(v_obj.send_quote_id)
                return Response({'serializer':link})
            else:
                if domain == '172.16.0.109:8000':
                    text_content = 'To Update the price for Item - '+str(i_obj.name)+'<br/><a href="http://'+str(domain)+'/quote/?vendoritem='+str(v_i_id.id)+'&send_quote_id='+str(v_obj.send_quote_id)+'">Please Click this link. </a>'
                else:
                    text_content = 'To Update the price for Item - '+str(i_obj.name)+'<br/><a href="https://'+str(domain)+'/quote/?vendoritem='+str(v_i_id.id)+'&send_quote_id='+str(v_obj.send_quote_id)+'">Please Click this link. </a>'
                email = EmailMessage(subject='Quote Request',body=text_content,from_email=settings.DEFAULT_FROM_EMAIL,to=[str(v_obj.email)])
                email.content_subtype = "html"
                email.send()
                return Response({'serializer':'Link has been sent to the email address.'})
        except: 
            v_i_id = request.query_params['vendoritem']
            send_quote_id = request.query_params['send_quote_id']
            obj=ItemVendor.objects.get(id =v_i_id)  
            try:
                v_ob = CompanyVendor.objects.get(id=obj.companyvendor.id,send_quote_id=send_quote_id)
                if (datetime.datetime.now(timezone.utc) - v_ob.link_expiration_date) > datetime.timedelta(1): 
                    return Response({'serializer':'This link has been expired. Please send the Quote request again.','status':'expired'},template_name="update_cost.html")
            except:
                return Response({'serializer':'Unauthorized..!! You cannot access this link.','status':'unauthorized'},template_name="update_cost.html")
            serializer = CostSerializer(obj)
            return Response({'serializer':serializer.data,'vendor_name':obj.companyvendor.name,\
                             'vendor_id':obj.companyvendor.id,'item_name':obj.companyitem.name,\
                             'item_id':obj.companyitem.id,},template_name="update_cost.html")

class PurchaseOrderAPI(APIView):
    """
    This API is used to render template having Purchase Order list or 
    if query parameter like 'id' is sent the it will render Purchase Order details
    """
    
    renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
    def get(self, request,*args, **kwargs):
        try:            
            po_id = request.query_params['id']
            obj = PurchaseOrder.objects.get(id=po_id)            
            serializer = PurchaseOrderSerializer(obj)                                
            return Response({'serializer':serializer.data},template_name="purchase_order/purchase_order_details.html")
        except:
            try:
                objs = UserCompanyModel.objects.filter(user=request.user).first()
                queryset = PurchaseOrder.objects.filter(company=objs.company)
            except:
                queryset = PurchaseOrder.objects.all()
            serializer = PurchaseOrderSerializer(queryset, many=True)     
            return Response({'serializer':serializer.data},template_name="purchase_order/purchase_order_list.html")
        
class ItemReceiptAPI(APIView):
    """
    This API is used to render template having Item Receipt list or 
    if query parameter like 'id' is sent the it will render Item Receipt details
    """
    renderer_classes = (renderers.JSONRenderer,TemplateHTMLRenderer)
    def get(self, request,*args, **kwargs):
        try:            
            po_id = request.query_params['id']
            obj = ItemReceipt.objects.get(id=po_id)            
            serializer = ItemReceiptSerializer(obj)                                
            return Response({'serializer':serializer.data},template_name="item_receipt/item_receipt_details.html")
        except:
            try:
                objs = UserCompanyModel.objects.filter(user=request.user).first()
                po_queryset = PurchaseOrder.objects.filter(company_id = objs.company_id)
                queryset = ItemReceipt.objects.filter(created_from__in =po_queryset)
            except:
                queryset = ItemReceipt.objects.all()
            serializer = ItemReceiptSerializer(queryset, many=True)     
            return Response({'serializer':serializer.data},template_name="item_receipt/item_receipt_list.html")
        