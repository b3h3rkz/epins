from django.contrib import admin

from .models import BusinessUnit


class BusinessUnitAdmin(admin.ModelAdmin):
    model = BusinessUnit
    list_display = ['__str__', 'website_url']


admin.site.register(BusinessUnit, BusinessUnitAdmin)
