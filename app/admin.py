from django.contrib import admin
from app.models import customerDetail
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django import forms



admin.site.site_header = 'Operator Portal'


class customerDetailAdmin(admin.ModelAdmin):
	list_display = ('user','FW_Instance_ID', 'IP_Address_1', 'IP_Address_2','Customer_Service_ID', 'Customer_Reference_ID')
	search_fields = ('user__username','FW_Instance_ID', 'IP_Address_1', 'IP_Address_2','Customer_Service_ID', 'Customer_Reference_ID',)


admin.site.register(customerDetail, customerDetailAdmin)


UserAdmin.list_display = ('username', 'last_login', 'date_joined','is_active', 'is_staff',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
