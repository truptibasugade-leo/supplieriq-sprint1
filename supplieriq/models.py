from __future__ import unicode_literals

from django.db import models
import uuid
from datetime import datetime    

class Company(models.Model):

    """
    Purpose: Describes the schema required to maintain Company details
    """
    # Common Information
    name = models.CharField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
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
    
    
class Vendor(models.Model):

    """
    Purpose: Describes the schema required to maintain Vendor details
    """
    # Common Information
    name = models.CharField(max_length=256, null=True, blank=True)
    company = models.ForeignKey('Company')    
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    erp_vendor_code = models.CharField(max_length=256, null=True, blank=True)
    send_quote_id = models.CharField(max_length=100, blank=True, default=uuid.uuid4)
    link_expiration_date = models.DateTimeField(default=datetime.now)
    
    def __unicode__(self):
        return self.name
    
class Item(models.Model):

    """
    Purpose: Describes the schema required to maintain Item details
    """
    # Common Information
    name = models.CharField(max_length=256, null=True, blank=True)
    erp_item_code = models.CharField(max_length=256, null=True, blank=True)
    description = models.CharField(max_length=20, null=True, blank=True)
    company = models.ForeignKey('Company', null=True, blank=True)  
    vendor = models.ManyToManyField('Vendor')
    def __unicode__(self):
        return self.name
 
class Address(models.Model):
    """
    Purpose: Model for Address.
    """
    vendor = models.ForeignKey('Vendor', null=True, blank=True)
 
    address1 = models.CharField(max_length=255, null=True, blank=True)
 
    address2 = models.CharField(max_length=255, null=True, blank=True)
 
    city = models.CharField(max_length=255, null=True, blank=True)
 
    state = models.CharField(max_length=255, null=True, blank=True)
 
    country = models.CharField(max_length=255, null=True, blank=True)
 
    zipcode = models.CharField(max_length=6, null=True, blank=True)
 
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
        return self.get_address()


class ItemVendor(models.Model):
    item = models.ForeignKey('Item') 
    vendor = models.ForeignKey('Vendor') 
    
    def __unicode__(self):
        return 'Item: ' + self.item.name + ' Vendor: ' +self.vendor.name

    class Meta:
        managed = False
        db_table = 'supplieriq_item_vendor'
        

class FixedCost(models.Model):
    itemvendor = models.ForeignKey('ItemVendor')
    cost_type = models.CharField(max_length=256, null=True, blank=True)
    cost = models.CharField(max_length=256, null=True, blank=True)
    def __unicode__(self):
        return self.cost_type

    
class VariableCost(models.Model):
    itemvendor = models.ForeignKey('ItemVendor')
    quantity = models.CharField(max_length=256, null=True, blank=True)
    cost = models.CharField(max_length=256, null=True, blank=True)
    def __unicode__(self):
        return 'Quantity: ' +self.quantity + ', Cost:'+self.cost


class Price(models.Model):    
    itemvendor = models.ForeignKey('ItemVendor')
    fixedCost = models.ForeignKey('FixedCost')
    variableCost = models.ForeignKey('VariableCost')
    def __unicode__(self):
        return 'Vendor: ' + self.itemvendor.vendor.name + \
            ', Item:'+self.itemvendor.item.name + \
            ', FixedCost: '+ self.fixedCost.cost_type +'- ' +self.fixedCost.cost 

    
    
