from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Search)
class SearchAdmin(admin.ModelAdmin):
    list_display=['search_data']

@admin.register(SubObjectJSON)
class SubObjectJSONAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "sub_objects",
    ]
    search_fields = [
        "id",
        "sub_objects",
    ]
    list_per_page = 10