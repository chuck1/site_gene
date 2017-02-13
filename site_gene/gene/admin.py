from django.contrib import admin

# Register your models here.

from .models import *

class PersonAdmin(admin.ModelAdmin):
    ordering = ('name',)

admin.site.register(Person, PersonAdmin)
admin.site.register(Location)

