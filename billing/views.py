import base64
from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Meter, MeterReading, MeterReader
from .forms import MeterReadingForm

def tenant_list(request):
    from .models import Tenant
    tenants = Tenant.objects.prefetch_related('houses')
    return render(request, 'billing/tenant_list.html', {'tenants': tenants})

def scan_reading_page(request):
    # Screen that hosts QR scanner + camera + OCR. We'll include the JS libs from CDN in template.
    return render(request, 'billing/scan_reading.html')

@require_POST
def api_upload_reading(request):
    """
    Accepts multipart/form-data with:
      - meter_id (string) OR meter (pk)
      - reading_value
      - photo (file)
      - reader_id (optional)
      - ocr_text (optional)
    Saves MeterReading and returns JSON.
    """
    meter_id = request.POST.get('meter_id') or request.POST.get('meter')
    reading_value = request.POST.get('reading_value')
    reader_id = request.POST.get('reader_id')
    ocr_text = request.POST.get('ocr_text', '')

    if not meter_id or not reading_value:
        return HttpResponseBadRequest("meter_id and reading_value are required")

    # locate meter by meter_id field first, fallback to PK
    meter = Meter.objects.filter(meter_id=meter_id).first()
    if meter is None:
        try:
            meter = Meter.objects.get(pk=int(meter_id))
        except Exception:
            return HttpResponseBadRequest("Meter not found")

    reader = None
    if reader_id:
        reader = MeterReader.objects.filter(reader_id=reader_id).first()

    photo = request.FILES.get('photo')
    reading = MeterReading(meter=meter, reader=reader, reading_value=reading_value, ocr_text=ocr_text)
    if photo:
        reading.photo = photo
    reading.save()

    return JsonResponse({
        'id': reading.id,
        'meter': meter.meter_id,
        'reading_value': str(reading.reading_value),
        'captured_at': reading.captured_at.isoformat(),
    })