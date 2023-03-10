from django.contrib import admin
from.models import Catagory

# Register your models here.

class CatagoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('catagory_name',)}
    list_display = ('catagory_name', 'slug')
admin.site.register(Catagory, CatagoryAdmin)

