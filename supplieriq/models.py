from __future__ import unicode_literals

from django.db import models
import uuid
from datetime import datetime 
from decimal import Decimal   
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django_countries import countries
from supplieriq.countries import COUNTRIES
from django.core.validators import MaxValueValidator, MinValueValidator

class Company(models.Model):

    """
    Purpose: Describes the schema required to maintain Company details
    """
    # Common Information
    name = models.CharField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    supplieriq_id = models.CharField(max_length=256,null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Account(models.Model):

    """
    Purpose: Describes the schema required to maintain Account for the Company
    """
    # Common Information
    account_no = models.CharField(max_length=12, null=True, blank=True)
    license_key = models.CharField(max_length=256, null=True, blank=True)
    company = models.ForeignKey('Company')
    expiry_date = models.DateField(null=True, blank=True)
    
    
class CompanyVendor(models.Model):

    """
    Purpose: Describes the schema required to maintain Vendor details
    """
    # Common Information
    name = models.CharField(max_length=256, null=True, blank=True)
    company = models.ForeignKey('Company')    
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    erp_vendor_code = models.CharField(max_length=256, null=True, blank=True)
    supplieriq_vendor_id = models.CharField(max_length=256,null=True, blank=True)
    send_quote_id = models.CharField(max_length=100, blank=True, default=uuid.uuid4)
    link_expiration_date = models.DateTimeField(default=datetime.now)
    is_deleted = models.BooleanField(default=False)
    
    
    def __unicode__(self):
        return "Company : "+self.company.name+", Vendor : "+self.name
    
class CompanyItem(models.Model):

    """
    Purpose: Describes the schema required to maintain Item details
    """
    # Common Information
    name = models.CharField(max_length=256, null=True, blank=True)
    erp_item_code = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=20, null=True, blank=True)
    company = models.ForeignKey('Company', null=True, blank=True)  
    target_price = models.DecimalField(max_digits=10, decimal_places=2,default=Decimal('0.00'))
    vendor = models.ManyToManyField('CompanyVendor')
    is_deleted = models.BooleanField(default=False)
    def __unicode__(self):
        return "Company : "+self.company.name+", Item : " +self.name
 
class VendorAddress(models.Model):
    """
    Purpose: Model for VendorAddress.
    """
    vendor = models.ForeignKey('CompanyVendor', null=True, blank=True)
 
    address1 = models.CharField(max_length=255, null=True, blank=True)
 
    address2 = models.CharField(max_length=255, null=True, blank=True)
 
    city = models.CharField(max_length=255, null=True, blank=True)
 
    state = models.CharField(max_length=255, null=True, blank=True)
    
    county_choice = COUNTRIES
    
    country = models.CharField(max_length=2,choices=county_choice,default='AD')
 
    zipcode = models.CharField(max_length=6, null=True, blank=True)
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6,default=Decimal('0.00'))

    longitude = models.DecimalField(max_digits=9, decimal_places=6,default=Decimal('0.00'))

 
    def get_address(self):
        """
        Purpose: To return string representation of address.
        :returns: returns verbose string for the address values.
        """
        address_list = [self.address1, self.address2, self.city, self.state,
                        self.country, self.zipcode]
        address_list = filter(None, address_list)
        return ', '.join(address_list)
 
    def __unicode__(self):
        return "Vendor : " +self.vendor.name +' - '+ self.get_address()


class ItemVendor(models.Model):
    companyitem = models.ForeignKey('CompanyItem') 
    companyvendor = models.ForeignKey('CompanyVendor') 
    
    def __unicode__(self):
        return 'Item : ' + self.companyitem.name + ' Vendor : ' +self.companyvendor.name 

    class Meta:
        managed = False
        db_table = 'supplieriq_companyitem_vendor'
        

class FixedCost(models.Model):
    itemvendor = models.ForeignKey('ItemVendor')
    cost_type = models.CharField(max_length=256, null=True, blank=True)
    cost = models.CharField(max_length=256, null=True, blank=True)
    def __unicode__(self):
        return "ItemVendor : " + str(self.itemvendor.companyitem.name)+ \
            ' ' + str(self.itemvendor.companyvendor.name) +', Cost Type : ' +str(self.cost_type)

    
class VariableCost(models.Model):
    itemvendor = models.ForeignKey('ItemVendor')
    quantity = models.CharField(max_length=256, null=True, blank=True)
    cost = models.CharField(max_length=256, null=True, blank=True)
    def __unicode__(self):
        return "ItemVendor : " + str(self.itemvendor.companyitem.name)+ \
            ' ' + str(self.itemvendor.companyvendor.name) +', Quantity : ' +self.quantity + ', Cost : '+self.cost


class Price(models.Model):    
    itemvendor = models.ForeignKey('ItemVendor')
    fixedCost = models.ForeignKey('FixedCost')
    variableCost = models.ForeignKey('VariableCost')
    def __unicode__(self):
        return 'Vendor: ' + self.itemvendor.vendor.name + \
            ', Item:'+self.itemvendor.item.name + \
            ', FixedCost: '+ self.fixedCost.cost_type +'- ' +self.fixedCost.cost 

    
class UserCompanyModel(models.Model):
    """ Model to relate User and Company """
    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)

    class Meta:
        unique_together = ("user","company")

    def __unicode__(self):
        return 'User : ' + str(self.user.username) + ', Company : ' + str(self.company.name)
    
class Location(models.Model):
    """
    Purpose: Model for Company Address.
    """
    company = models.ForeignKey('Company', null=True, blank=True)
 
    phone = models.CharField(max_length=20, null=True, blank=True)
    
    address1 = models.CharField(max_length=255, null=True, blank=True)
 
    address2 = models.CharField(max_length=255, null=True, blank=True)
    
    address3 = models.CharField(max_length=255, null=True, blank=True)
 
    city = models.CharField(max_length=255, null=True, blank=True)
 
    state = models.CharField(max_length=255, null=True, blank=True)
    
    county_choice = COUNTRIES
    
    country = models.CharField(max_length=2,choices=county_choice,default='AD')
 
    zipcode = models.CharField(max_length=6, null=True, blank=True)
    
    latitude = models.DecimalField(max_digits=9, decimal_places=6,default=Decimal('0.00'))

    longitude = models.DecimalField(max_digits=9, decimal_places=6,default=Decimal('0.00'))

 
    def get_address(self):
        """
        Purpose: To return string representation of address.
        :returns: returns verbose string for the address values.
        """
        address_list = [self.address1, self.address2, self.city, self.state,
                        self.country, self.zipcode]
        address_list = filter(None, address_list)
        return "Company : " + self.company.name + ", Address : " + ', '.join(address_list)
 
    def __unicode__(self):
        return self.get_address()

class PurchaseOrder(models.Model):
     
    vendor = models.ForeignKey('CompanyVendor', null=True, blank=True)
  
    PO_date = models.DateTimeField(default=datetime.now)
     
    recieve_by_date = models.DateTimeField(default=datetime.now)
    
    total = models.DecimalField(max_digits=10, decimal_places=2,default=Decimal('0.00'))
    
    company = models.ForeignKey('Company', null=True, blank=True)
  
    erp_po_code = models.CharField(max_length=255, null=True, blank=True)
    
    def __unicode__(self):
        return 'PO Date : ' + str(self.PO_date.date()) + ', Recieve By Date : ' + str(self.recieve_by_date.date())
    
class POItem(models.Model):
    
    purchaseorder = models.ForeignKey(PurchaseOrder,null=True, blank=True)
    
    item = models.ForeignKey('CompanyItem')
    
    quantity = models.CharField(max_length=255, null=True, blank=True)
    
    unit_price = models.CharField(max_length=255, null=True, blank=True)
    
    total_amount = models.CharField(max_length=255, null=True, blank=True)
    
    def __unicode__(self):
        return 'PO : '+str(self.purchaseorder.id)+', Item : ' + self.item.name 

     
class ItemReceipt(models.Model):
     
    date = models.DateTimeField(default=datetime.now)
  
    rating = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(1)])
    
    to_location = models.CharField(max_length=255, null=True, blank=True)
    
    created_from = models.ForeignKey('PurchaseOrder')
    
    def __unicode__(self):
        return 'PO ID : ' + str(self.created_from.id) + ', Rating : ' +str(self.rating)

    
     