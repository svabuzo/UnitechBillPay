```markdown
# UnitechBillPay - Django starter

This is a starter Django app to manage tenants, houses, meters and to capture meter readings via QR + photo + client-side OCR.

Getting started (local):

1. Create and activate a Python virtualenv:
   python -m venv venv
   source venv/bin/activate

2. Install:
   pip install -r requirements.txt

3. Create the Django project and app if not present (this sample assumes 'unitech_billpay' project and 'billing' app).

4. Add settings for MEDIA_ROOT and MEDIA_URL (see provided settings snippet). Add 'billing' to INSTALLED_APPS.

5. Run migrations:
   python manage.py makemigrations
   python manage.py migrate

6. Create a superuser:
   python manage.py createsuperuser

7. Collect static (if needed) and run server:
   python manage.py runserver

8. Open:
   - Admin: http://127.0.0.1:8000/admin/
   - Tenant list: http://127.0.0.1:8000/billing/tenants/
   - Scan page: http://127.0.0.1:8000/billing/scan/

Notes:
- This starter uses client-side OCR (Tesseract.js). No Tesseract binary is required on the server.
- For production, secure endpoints, require login, protect who can submit readings, and validate input.
- If you prefer server-side OCR, replace the client-side Tesseract usage with an upload-only flow and run pytesseract on the server (requires installation of tesseract-ocr package).
```