from django.contrib import admin
from .models import Reventos,Person, AccessSEDE
# Register your models here.

admin.site.register(Reventos)




@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ['nac','dni', 'first_name', 'last_name', 'gender', 'created_at']
    list_filter = ['nac', 'dni']

@admin.register(AccessSEDE)
class AccessSEDEAdmin(admin.ModelAdmin):
    list_display = ['visitor', 'entry', 'hours', 'hoursEx',  'obs']
    list_filter = ['entry']
    date_hierarchy = 'entry'