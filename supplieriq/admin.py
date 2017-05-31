from django.contrib import admin
from django.db import models
from supplieriq.models import CompanyVendor,Company,Account,CompanyItem,\
     VendorAddress,FixedCost,VariableCost,UserCompanyModel,Location,PurchaseOrder,ItemReceipt,\
     ItemVendor,POItem
# Register your models here.
class CompanyAdmin(admin.ModelAdmin):    
    fields = ('name', )

# class UserAdmin(admin.ModelAdmin):    
#     fields = ('email','password','company' )
#     

class AccountAdmin(admin.ModelAdmin):
    fields = ('account_no', 'license_key','expiry_date','company')

class CompanyVendorAdmin(admin.ModelAdmin):
    fields = ('name','email','phone','company','erp_vendor_code',)
    
class CompanyItemAdmin(admin.ModelAdmin):
    
    fields = ('name','erp_item_code','company','description','vendor','target_price')

class VendorAddressAdmin(admin.ModelAdmin):
    fields = ('address1','address2','vendor','city','state','country','zipcode','latitude','longitude')

class FixedCostAdmin(admin.ModelAdmin):
    fields = ('itemvendor','cost_type','cost')


class VariableCostAdmin(admin.ModelAdmin):
    fields = ('itemvendor','quantity','cost')

class UserCompanyAdmin(admin.ModelAdmin):
    fields = ('user','company')

class LocationAdmin(admin.ModelAdmin):
    fields = ('address1','address2','company','city','state','country','zipcode','latitude','longitude','phone')

class PurchaseOrderAdmin(admin.ModelAdmin):
    fields = ('vendor','company','PO_date','recieve_by_date','total','erp_po_code')

class ItemReceiptAdmin(admin.ModelAdmin):
    fields = ('date','rating','to_location','created_from')

class POItemAdmin(admin.ModelAdmin):
    fields = ('purchaseorder','item','quantity','unit_price','total_amount')


class ItemVendorAdmin(admin.ModelAdmin):
    fields = ('companyitem','companyvendor')

admin.site.register(CompanyVendor, CompanyVendorAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(CompanyItem, CompanyItemAdmin)
admin.site.register(VendorAddress, VendorAddressAdmin)
admin.site.register(FixedCost, FixedCostAdmin)
admin.site.register(VariableCost, VariableCostAdmin)
admin.site.register(UserCompanyModel, UserCompanyAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(ItemReceipt, ItemReceiptAdmin)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(POItem, POItemAdmin)
admin.site.register(ItemVendor, ItemVendorAdmin)




