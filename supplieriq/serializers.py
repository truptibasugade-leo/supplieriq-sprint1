
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
from supplieriq.models import CompanyVendor,Company, CompanyItem, VendorAddress,Price, \
    FixedCost,VariableCost,ItemVendor,UserCompanyModel,PurchaseOrder,ItemReceipt

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
    company = serializers.SerializerMethodField('get_company_name')
    erp_vendor_code = serializers.CharField(read_only=True)
    address = serializers.SerializerMethodField('get_vendor_address')
    phone = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    class Meta(object):
        model = CompanyVendor
        fields = (
            'vendorid','name', 'erp_vendor_code','phone', 'email','company',
        )
    
    def get_vendor_id(self, obj):
        return obj.id;
    
    def get_company_name(self, obj):
        return obj.company.name;
    
    def get_vendor_address(self, obj):
        try:
            addrObj = VendorAddress.objects.get(vendor_id=obj.id)
            l1 = str(addrObj.address1) + ' ' + str(addrObj.address2)
            l1 = filter(None, l1)
            l2 = str(addrObj.city) + ' ' + str(addrObj.state) + ' ' + str(addrObj.zipcode)
            l2 = filter(None, l2)
            l3 = str(addrObj.country)
            l3 = filter(None, l3)
            
            xx = [l1,l2,l3]
            return '\n '.join(xx)
        except:
            return ''
    
    def get_item_fixed_cost(self, obj):
        price_details = {}
        for x in obj.item_set.all():
            ob = ItemVendor.objects.filter(companyitem_id=x.id,companyvendor_id=obj.id)
            for zz in ob:
                fc_objs = FixedCost.objects.filter(itemvendor=zz.id)
                q1 = {}
                for y in fc_objs:
                    q1[y.cost_type] = y.cost
                if q1:                 
                    price_details['fixed_cost_'+str(zz.id)] = q1
        return price_details; 
       
    def get_item_variable_cost(self, obj):
        price_details = {}
        for x in obj.itemvendor_set.values():
            vc_objs = VariableCost.objects.filter(itemvendor=x['id'])
            vc = []
            for z in vc_objs:
                q2 = {}
                q2['Quantity'] = z.quantity
                q2['Cost'] = z.cost
                vc.append(q2)
            if vc:
                price_details['variable_cost_'+str(x['id'])] = vc
        return price_details;   
        
class VendorAddressSerializer(serializers.Serializer):
    
    vendor = VendorSerializer(read_only=True, many=True)
 
    address1 = serializers.CharField(read_only=True)
 
    address2 = serializers.CharField(read_only=True)
 
    city = serializers.CharField(read_only=True)
 
    state = serializers.CharField(read_only=True)
 
    country = serializers.CharField(read_only=True)
 
    zipcode = serializers.CharField(read_only=True)
    
    class Meta(object):
        model = VendorAddress
        fields = (
            'address1','address2', 'city','state','country','zipcode',
        )        

class ItemSerializer(serializers.Serializer):

    """
    Used for indexing only.
    """
    itemid = serializers.SerializerMethodField('get_item_id')
    name = serializers.CharField(read_only=True)
    erp_item_code = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    vendor = serializers.SerializerMethodField('get_item_vendor_object')
    class Meta(object):
        model = CompanyVendor
        fields = (
            'itemid','name', 'erp_item_code','description','price','address'
        )
    
    def get_item_id(self, obj):
        return obj.id;        
    
    def get_item_vendor_object(self,obj):
        zz = []
        for y in obj.vendor.filter(company=obj.company):
            x = VendorSerializer(y)
            py_dict = x.data
            fixed_cost_item = self.get_item_fixed_cost(obj,y)            
            variable_cost_item = self.get_item_variable_cost(obj,y)
            py_dict.update({'price': [{'fixed_cost':fixed_cost_item},{'variable_cost':variable_cost_item}]})
            zz.append(py_dict)
        return zz
    def get_item_fixed_cost(self, obj,vendor_obj):
        
        price_details = []
        for x in obj.itemvendor_set.values():
            if x['companyvendor_id'] == vendor_obj.id:
                fc_objs = FixedCost.objects.filter(itemvendor=x['id'])
                q1 = {}
                for y in fc_objs:
                    q1[y.cost_type] = y.cost
                if q1:                 
                    price_details.append(q1)
        return price_details; 
       
    def get_item_variable_cost(self, obj,vendor_obj):
        price_details = []
        for x in obj.itemvendor_set.values():
            if x['companyvendor_id'] == vendor_obj.id:
                vc_objs = VariableCost.objects.filter(itemvendor=x['id'])
                vc = []
                for z in vc_objs:
                    q2 = {}
                    q2['Quantity'] = z.quantity
                    q2['Cost'] = z.cost
                    vc.append(q2)
                if vc:
                    price_details.append(vc)
        return price_details; 

class ItemVendorSerializer(serializers.Serializer):

    """
    Used for indexing only.
    """
    item_vendor = serializers.SerializerMethodField('get_item_vendor_object')
    vendor= serializers.SerializerMethodField('get_vendor_object')
    item = serializers.SerializerMethodField('get_item_object')
    class Meta(object):
        model = ItemVendor
        fields = (
            'companyitem','companyvendor',
        )
    def get_item_vendor_object(self, obj):        
        return {"itemvendor":obj.id} 
    
    def get_vendor_object(self, obj):        
        return {"vendor_name":obj.companyvendor.name,"vendor_id": obj.companyvendor.id} 
    
    def get_item_object(self, obj):        
        return {"item_name":obj.companyitem.name,"item_id": obj.companyitem.id} ; 

class CostSerializer(serializers.Serializer):
    fixed_cost_item = serializers.SerializerMethodField('get_item_fixed_cost')
    variable_cost_item = serializers.SerializerMethodField('get_item_variable_cost') 
    
    class Meta(object):
        model = ItemVendor
        fields = (
            'item','vendor','fixed_cost_item','variable_cost_item',
        )
    def get_item_fixed_cost(self, obj):
        
        price_details = []

        fc_objs = FixedCost.objects.filter(itemvendor=obj.id)
        fc=[]
        for y in fc_objs:
            q1 = {}
            q1['fixedcost_id'] = y.id
            q1[y.cost_type] = y.cost
            fc.append(q1)
        if fc:                 
            price_details.append(fc)
        return price_details; 
    
    def get_item_variable_cost(self, obj):  
        price_details = []
        vc_objs = VariableCost.objects.filter(itemvendor=obj.id)
        vc = []
        for z in vc_objs:
            q2 = {}          
            q2['variablecost_id'] = z.id  
            q2['Cost'] = z.cost
            q2['Quantity'] = z.quantity

            
            vc.append(q2)
        if vc:
            price_details.append(vc)
        return price_details;      
    
class FixedCostSerializer(serializers.Serializer):

    """
    Purpose: To handle validations and populate sign in details.
    Methods Supported: Get & Post.
    """
    itemvendor = ItemVendorSerializer(read_only=True, many=True)
    price_type = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=6)

    def validate(self, attrs):
        """
        Purpose: To validate FixedCost serializers.
        :param self: Context Object
        :param attrs: Dictionary containing the key as field name & it's value
        :param source: Field name
        Constraints:
        User account should be present and should be active.
        :returns: attrs in case of valid inputs else error message
        """
        
        price_type = attrs.get('price_type')
        price = attrs.get('price')   
        if price_type.isdigit():
            error = "Invalid data.Price Type cannot be a number."
            raise serializers.ValidationError(error)        
        return attrs

class VariableCostSerializer(serializers.Serializer):

    """
    Purpose: To handle validations and populate sign in details.
    Methods Supported: Get & Post.
    """
    itemvendor = ItemVendorSerializer(read_only=True, many=True)
    quantity = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=6)

    def validate(self, attrs):
        """
        Purpose: To validate VariableCost serializers.
        :param self: Context Object
        :param attrs: Dictionary containing the key as field name & it's value
        :param source: Field name
        Constraints:
        User account should be present and should be active.
        :returns: attrs in case of valid inputs else error message
        """
        
        quantity = attrs.get('quantity')
        price = attrs.get('price')   
        if not quantity.isdigit():
            error = "Invalid data.Quantity has to be a number."
            raise serializers.ValidationError(error) 
        else:
            try:       
                queryset= VariableCost.objects.filter(itemvendor=self.initial_data['itemvendor'],quantity=attrs.get('quantity'))                
            except:
                queryset = ''                   
            if queryset:
                vv = queryset.first()
                if str(vv.id) != str(self.initial_data['variablecost_id']):
                    error = "Price for this Quantity already exists."
                    raise serializers.ValidationError(error) 
        return attrs
    

class PurchaseOrderSerializer(serializers.Serializer):

    """
    Used for indexing only.
    """
    po_id = serializers.SerializerMethodField('get_po_object')
    PO_date = serializers.DateTimeField(read_only=True)
    recieve_by_date = serializers.DateTimeField(read_only=True)
    vendor = serializers.SerializerMethodField('get_vendor_object')
    erp_po_code = serializers.CharField(read_only=True)
    total = serializers.CharField(read_only=True)
    poitem = serializers.SerializerMethodField('get_poitem_object')
    
    
    
    class Meta(object):
        model = PurchaseOrder
        fields = (
            'PO_date', 'recieve_by_date','total_amount','erp_po_code','total'
        )
    
    def get_poitem_object(self, obj): 
        items = obj.poitem_set.all()  
        
        y =[]
        for x in items:
            q={}
            q['item_name'] =  x.item.name
            q['item_id'] = x.item.id
            q['quantity'] = x.quantity
            q['unit_price'] = x.unit_price
            q['total_amount'] = x.total_amount
            y.append(q)
        return y 
    
    def get_vendor_object(self, obj):    
        vendor =  obj.vendor
        return {"vendor_name":vendor.name, "vendor_id": vendor.id } 
    
    def get_po_object(self, obj):    
        return obj.id 
    
class ItemReceiptSerializer(serializers.Serializer):

    """
    Used for indexing only.
    """
    vendor = serializers.SerializerMethodField('get_vendor_object')
    item = serializers.SerializerMethodField('get_item_object')
    created_from = serializers.SerializerMethodField('get_po_object')
    rating = serializers.CharField(read_only=True)
    date = serializers.DateTimeField(read_only=True)
    to_location = serializers.CharField(read_only=True)    
    item_receipt = serializers.SerializerMethodField('get_ir_object')
    
    class Meta(object):
        model = PurchaseOrder  
        fields = (
            'item','date', 'rating','quantity','created_from','to_location'
        )
    
    def get_item_object(self, obj):    
        items = obj.created_from.poitem_set.all() 
        y =[]
        for x in items:
            q={}
            q['item_name'] =  x.item.name
            q['item_id'] = x.item.id
            q['quantity'] = x.quantity
            q['unit_price'] = x.unit_price
           
            y.append(q)
        
        return y 
    
    def get_vendor_object(self, obj):    
        vendor =  obj.created_from.vendor
        return {"vendor_name":vendor.name, "vendor_id": vendor.id } 
    
    def get_po_object(self, obj):    
        return obj.created_from.id 
    
    def get_ir_object(self, obj):    
        return obj.id 
    