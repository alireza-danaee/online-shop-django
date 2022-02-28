from django.contrib import admin
from .models import Coupons
# Register your models here.





class CouponsAdmin(admin.ModelAdmin):
    list_display = ["code" , "valid_from" , "valid_to" , "discount" , "active"]
    list_filter = ["active" , "valid_to" , "valid_from"]
    search_field = ["code"]

admin.site.register(Coupons , CouponsAdmin)
