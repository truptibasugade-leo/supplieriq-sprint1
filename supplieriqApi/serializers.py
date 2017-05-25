from rest_framework import serializers
from supplieriq.models import CompanyVendor,Company, CompanyItem, VendorAddress,Price, \
    FixedCost,VariableCost,ItemVendor,UserCompanyModel,PurchaseOrder,ItemReceipt

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
    
    class Meta(object):
        model = CompanyItem
        fields = (
            'name', 'description','target_price', 'erp_item_code',
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
        
        return ''
    
    class Meta(object):
        model = CompanyItem
        fields = (
            'name', 'description','target_price', 'erp_item_code',
        )
    
    
     