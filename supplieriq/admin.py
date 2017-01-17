from django.contrib import admin
from supplieriq.models import Vendors,Company
# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    fields = ('name', )

class VendorsAdmin(admin.ModelAdmin):
    fields = ('name','email','phone','company')
    

admin.site.register(Vendors, VendorsAdmin)
admin.site.register(Company, CompanyAdmin)
