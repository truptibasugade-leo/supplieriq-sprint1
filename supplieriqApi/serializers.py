from rest_framework import serializers
from supplieriq.models import CompanyVendor,Company, CompanyItem, VendorAddress,Price, \
    FixedCost,VariableCost,ItemVendor,UserCompanyModel,PurchaseOrder,ItemReceipt
from django.contrib.auth.models import User
from django.http import Http404


class CompanyApiSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    address = serializers.CharField(required=True)
    
    def validate(self, attrs):
        try:
            data = Company.objects.get(id=attrs)
        except:
            raise serializers.ValidationError("Company Id is required.")
        return data
        
    
    class Meta(object):
        model = Company
        fields = (
            'name', 'address',
        )
        
class VendorAddressSerializer(serializers.ModelSerializer):
     
    address1 = serializers.CharField(required=True)
 
    address2 = serializers.CharField()
 
    city = serializers.CharField(required=True)
 
    state = serializers.CharField(required=True)
 
    country = serializers.CharField(required=True)
 
    zipcode = serializers.CharField(required=True)
    
    def create(self, validated_data,obj):
        vv =validated_data[0]
        vv.update({"vendor":obj})
        ob = VendorAddress.objects.create(**vv)
        return ob
    
    class Meta(object):
        model = VendorAddress
        fields = (
            'address1','address2', 'city','state','country','zipcode',
        ) 
            
class VendorApiSerializer(serializers.ModelSerializer):

    """
    Used for indexing only.
    """
    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    erp_vendor_code = serializers.CharField(required=True)    
    address_set = VendorAddressSerializer(many=True)
    
    def create(self, validated_data,request):        
        validated_data.pop("address_set")
        ob = UserCompanyModel.objects.get(user=request.user)
        validated_data.update({"company":ob.company})
        obj = CompanyVendor.objects.create(**validated_data)        
        return obj        

    class Meta(object):
        model = CompanyVendor
        fields = (
            'name', 'erp_vendor_code','phone', 'email','address_set',
        )

class ItemVendorApiSerializer(serializers.ModelSerializer):
    
    companyitem = serializers.CharField(required=True)
    companyendor = serializers.CharField(required=True)
    
    def get_vendor_object(self, erp_vendor_code,company):
        try:
            return CompanyVendor.objects.get(erp_vendor_code=erp_vendor_code,company=company,is_deleted=False)
        except CompanyVendor.DoesNotExist:
            return ""
    
    def create(self, vendor,item):
    
        ob = self.get_vendor_object(vendor,item.company)
        if ob:       
            obj = ItemVendor.objects.create(companyitem=item,companyvendor=ob)
            return obj
        else:
            return ""
        
    class Meta(object):
        model = ItemVendor
        fields = (
            'companyitem', 'companyvendor'
        )
    
class ItemApiSerializer(serializers.ModelSerializer):

    """
    Used for indexing only.
    """
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    target_price = serializers.CharField(required=True)
    erp_item_code = serializers.CharField(required=True)           
    
    def create(self, validated_data,request):     
        
        ob = UserCompanyModel.objects.get(user=request.user)
        validated_data.update({"company":ob.company})
        obj = CompanyItem.objects.create(**validated_data)        
        return obj        
        
    class Meta(object):
        model = CompanyItem
        fields = (
            'name', 'description','target_price', 'erp_item_code',
        )
    
class SignInAPISerializer(serializers.ModelSerializer):

    """
    Purpose: To handle validations and populate sign in details.
    Methods Supported: Get & Post.
    """
    email = serializers.EmailField(
        required= True,
        style={'placeholder': 'Email', 'autofocus': True}
    )
    password = serializers.CharField(
        required= True,
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
    
    class Meta(object):
        model = User
        fields = (
            'email', 'password'
        )
        
class SupplierIQCompanyAPISerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    supplieriq_id = serializers.CharField(required=True)
    
    def validate(self, attrs):
        try:
            data = Company.objects.get(supplieriq_id=attrs.get('supplieriq_id'))
        except:
            data = attrs
        return data
        
    def create(self, validated_data,request):     
        
        obj = Company.objects.create(**validated_data)        
        return obj        
    
    class Meta(object):
        model = Company
        fields = (
            'name', 'supplieriq_id',
        )
        
class SupplierIQVendorAPISerializer(serializers.ModelSerializer):

    name = serializers.CharField(required=True)
    phone = serializers.CharField(required=True) 
    supplieriq_vendor_id = serializers.CharField(required=True)   
    address_set = VendorAddressSerializer(many=True)
    
    
    def validate(self, attrs):
        try:
            data = CompanyVendor.objects.filter(supplieriq_vendor_id=attrs.get('supplieriq_vendor_id'))
        except:
            data = attrs
        return data
    
    def create(self, validated_data,company):        
        validated_data.pop("address_set")
        try:
            ob = Company.objects.get(supplieriq_id=company)
            if ob.is_deleted == False:
                validated_data.update({"company":ob})
                obj = CompanyVendor.objects.create(**validated_data)        
                return obj
            else:
                return "Link the Company first with Purchase Smart."                        
        except:
            return "Link the Company first with Purchase Smart."
        

    class Meta(object):
        model = CompanyVendor
        fields = (
            'name', 'phone','supplieriq_vendor_id','address_set',
        )

class SupplierIQVendorAddressSerializer(serializers.ModelSerializer):
     
    address1 = serializers.CharField(required=True)
 
    address2 = serializers.CharField()
 
    city = serializers.CharField(required=True)
 
    state = serializers.CharField(required=True)
 
    country = serializers.CharField(required=True)
 
    zipcode = serializers.CharField(required=True)
    
    latitude = serializers.CharField(required=True)
    
    longitude = serializers.CharField(required=True)
    
    def create(self, validated_data,obj):
        vv =validated_data[0]
        vv.update({"vendor":obj})
        ob = VendorAddress.objects.create(**vv)
        return ob
    
    class Meta(object):
        model = VendorAddress
        fields = (
            'address1','address2', 'city','state','country','zipcode','latitude','longitude'
        ) 
