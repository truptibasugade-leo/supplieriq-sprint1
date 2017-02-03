from django.contrib import admin
from django.db import models
from supplieriq.models import Vendor,Company,Account,Item, Address,FixedCost,VariableCost
# Register your models here.
class CompanyAdmin(admin.ModelAdmin):    
    fields = ('name', )

# class UserAdmin(admin.ModelAdmin):    
#     fields = ('email','password','company' )
#     

class AccountAdmin(admin.ModelAdmin):
    fields = ('account_no', 'license_key','expiry_date','company')

class VendorAdmin(admin.ModelAdmin):
    fields = ('name','email','phone','company','erp_vendor_code')
    
class ItemAdmin(admin.ModelAdmin):
    fields = ('name','erp_item_code','company','description','vendor')

class AddressAdmin(admin.ModelAdmin):
    fields = ('address1','address2','vendor','city','state','country','zipcode')

class FixedCostAdmin(admin.ModelAdmin):
    fields = ('itemvendor','cost_type','cost')

class VariableCostAdmin(admin.ModelAdmin):
    fields = ('itemvendor','quantity','cost')

# class PriceAdmin(admin.ModelAdmin):
#     fields = ('itemvendor','fixedCost','variableCost')


admin.site.register(Vendor, VendorAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(FixedCost, FixedCostAdmin)
admin.site.register(VariableCost, VariableCostAdmin)
# admin.site.register(Price, PriceAdmin)




