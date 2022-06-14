from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Countries)
admin.site.register(Regions)
admin.site.register(SubRegions)