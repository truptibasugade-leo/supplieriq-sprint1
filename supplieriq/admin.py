from django.contrib import admin
from supplieriq.models import Vendor,Company,Account,Item #Cost
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

# class CostAdmin(admin.ModelAdmin):
#     fields = ('item_vendor','fixed_price','variable_price')


admin.site.register(Vendor, VendorAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Item, ItemAdmin)
# admin.site.register(Cost, CostAdmin)

