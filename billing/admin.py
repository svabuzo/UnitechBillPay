from django.contrib import admin
from .models import Tenant, House, MeterReader, Meter, MeterReading

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'phone')

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('house_number', 'street_name', 'tenant')

@admin.register(MeterReader)
class MeterReaderAdmin(admin.ModelAdmin):
    list_display = ('reader_id', 'user')

@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = ('meter_id', 'house', 'serial_number')

@admin.register(MeterReading)
class MeterReadingAdmin(admin.ModelAdmin):
    list_display = ('meter', 'reading_value', 'reader', 'captured_at')