from django.contrib import admin
from .models import Harvest


@admin.register(Harvest)
class HarvestAdmin(admin.ModelAdmin):

    list_display = (
        "crop_name",
        "farmer",
        "quantity",
        "harvest_date",
        "status",
        "soil_moisture",
        "temperature",
        "humidity",
    )

    list_filter = (
        "crop_name",
        "status",
        "harvest_date",
    )

    search_fields = (
        "crop_name",
        "farmer__username",
        "location",
    )

    ordering = (
        "-harvest_date",
    )