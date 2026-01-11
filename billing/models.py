from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Tenant(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class House(models.Model):
    house_number = models.CharField(max_length=50)
    street_name = models.CharField(max_length=200)
    suburb = models.CharField(max_length=200, blank=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.SET_NULL, null=True, blank=True, related_name='houses')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.house_number} {self.street_name}"

class MeterReader(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    reader_id = models.CharField(max_length=80, unique=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.reader_id} ({self.user})"

class Meter(models.Model):
    meter_id = models.CharField(max_length=120, unique=True)  # value encoded in QR
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='meters')
    serial_number = models.CharField(max_length=120, blank=True)
    installation_date = models.DateField(null=True, blank=True)
    last_verified = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.meter_id} - {self.house}"

class MeterReading(models.Model):
    meter = models.ForeignKey(Meter, on_delete=models.CASCADE, related_name='readings')
    reader = models.ForeignKey(MeterReader, on_delete=models.SET_NULL, null=True, blank=True)
    reading_value = models.DecimalField(max_digits=12, decimal_places=2)
    captured_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='meter_photos/', blank=True, null=True)
    ocr_text = models.TextField(blank=True)

    class Meta:
        ordering = ['-captured_at']

    def __str__(self):
        return f"{self.meter} - {self.reading_value} @ {self.captured_at}"