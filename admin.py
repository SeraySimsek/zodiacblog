from django.contrib import admin

# Register your models here.

from .models import *


class FortuneTellingAdmin(admin.ModelAdmin):
    readonly_fields = ('date_added',)
    list_display = ('from_user', 'to_user', 'is_ok')
    date_hierarchy = 'date_added'
    ordering = ['date_created']
    search_fields = ['to_user']


admin.site.register(Customer)
admin.site.register(user_type)
admin.site.register(post)
admin.site.register(FortuneTelling)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Bank)
admin.site.register(Contact)

