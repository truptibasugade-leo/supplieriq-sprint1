from django.contrib import admin
from supplieriq.models import Vendor,Company,Account,Item
# Register your models here.
class CompanyAdmin(admin.ModelAdmin):    
    fields = ('name', )

# class UserAdmin(admin.ModelAdmin):    
#     fields = ('email','password','company' )
#     

class AccountAdmin(admin.ModelAdmin):
    fields = ('account_no', 'license_key','expiry_date','company')

class VendorAdmin(admin.ModelAdmin):
    fields = ('name','email','phone','address','company','erp_vendor_code')
    
class ItemAdmin(admin.ModelAdmin):
    fields = ('name','erp_item_code','description','vendor')


admin.site.register(Vendor, VendorAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Item, ItemAdmin)

