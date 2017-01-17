from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Company(models.Model):

    """
    Purpose: Describes the schema required to maintain Products, Business and Movies
    """
    # Common Information
    name = models.CharField(max_length=256, null=True, blank=True)
    address = models.CharField(max_length=256, null=True, blank=True)
    
class Vendors(models.Model):

    """
    Purpose: Describes the schema required to maintain Products, Business and Movies
    """
    # Common Information
    name = models.CharField(max_length=256, null=True, blank=True)
    company = models.ForeignKey('Company')
    
    address = models.CharField(max_length=256, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    