from django.contrib import admin
# from .models import related models
from .models import CarModel, CarMake

# Register your models here.

# CarModelInline class
class CarModelInLine(admin.StackedInline):
    model = CarModel
    

# CarModelAdmin class
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'make','version','year','id') # what fields to display
    list_filter = ['make'] # you can filter by make
    search_fields = ['name', 'version'] # you can search by name and desc
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInLine]
    list_display = ('name', 'description') # what fields to display
    list_filter = ['name'] # you can filter by date
    search_fields = ['name'] # you can search by name and desc
# Register models here
admin.site.register(CarModel, CarModelAdmin)
admin.site.register(CarMake, CarMakeAdmin)