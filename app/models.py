from django.db import models
from django.contrib.auth.models import User
import sys
import os
from django.core.validators import RegexValidator
from django.core.validators import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS




class customerDetail(models.Model):
	FWInstanceValidator = RegexValidator(r'^[a-z]{3}[0-9]{7}$', 'Please enter the correct Instance ID. e.g format: jvf1234567 ')
	CustRefValidator = RegexValidator(r'^[CUS]{3}[-]{1}[A-Z]{2}[-]{1}[0-9]{8}$', 'Please enter the correct Reference ID. e.g format: "CUS-US-12345678" or "CUS-JP-12345678" ')
	CustSIDValidator = RegexValidator(r'^[SID]{3}[-]{1}[A-Z]{2}[-]{1}[0-9]{8}$', 'Please enter the correct Reference ID. e.g format: "CUS-US-12345678" or "SID-JP-12345678 ')
	user = models.OneToOneField(User)
	FW_Instance_ID = models.CharField(max_length=10, unique=True, validators=[FWInstanceValidator])
	Customer_Service_ID = models.CharField(max_length=15, unique=True, validators=[CustSIDValidator])
	Customer_Reference_ID = models.CharField(max_length=15, unique=True, validators=[CustRefValidator])
	IP_Address_1 = models.GenericIPAddressField(blank=False, unique=True, help_text= 'Please check the IP Address in the search field of Customer Detail page for any existing entries before entering here')
	IP_Address_2 = models.GenericIPAddressField(blank=False, unique=True, help_text= 'Please check the IP Address in the search field of Customer Detail page for any existing entries before entering here')

	def clean(self, *args, **kwargs):
		if (customerDetail.objects.filter(IP_Address_2=self.IP_Address_1).exists()):
			raise ValidationError('Customer details with the following "IP Address 1" value already exists. Please check the values before entering')
		elif (customerDetail.objects.filter(IP_Address_1=self.IP_Address_2).exists()):
			raise ValidationError('Customer details with the following "IP Address 2" value already exists. Please check the values before entering')
		else:
			super(customerDetail, self).clean(*args, **kwargs)
	def __unicode__(self):
		return self.user.username
