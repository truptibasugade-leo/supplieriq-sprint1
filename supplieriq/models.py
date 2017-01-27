from __future__ import unicode_literals

from django.db import models
# from django.contrib.auth.models import AbstractBaseUser
# 
# class User(AbstractBaseUser):
#     """
#     Custom user class.
#     """
#     email = models.EmailField('email address', unique=True, db_index=True)
#     company = models.ForeignKey('Company')


# Create your models here.

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
    address = models.CharField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    erp_vendor_code = models.CharField(max_length=256, null=True, blank=True)
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
    vendor = models.ManyToManyField(Vendor)
    def __unicode__(self):
        return self.name
    