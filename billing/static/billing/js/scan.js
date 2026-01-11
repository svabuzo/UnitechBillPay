// scan.js - vanilla JS to run QR scanner, camera capture, OCR (Tesseract.js) and submit reading
document.addEventListener('DOMContentLoaded', function () {
  const meterInput = document.getElementById('meter-id');
  const video = document.getElementById('camera-stream');
  const canvas = document.getElementById('capture-canvas');
  const btnCapture = document.getElementById('btn-capture');
  const btnOCR = document.getElementById('btn-ocr');
  const ocrTextEl = document.getElementById('ocr-text');
  const readingEl = document.getElementById('reading-value');
  const btnSubmit = document.getElementById('btn-submit');

  let lastBlob = null;

  // 1) Start html5-qrcode scanner
  if (window.Html5Qrcode) {
    const html5QrCode = new Html5Qrcode("qr-reader");
    const qrConfig = { fps: 10, qrbox: 250 };
    Html5Qrcode.getCameras().then(cameras => {
      const cameraId = cameras && cameras.length ? cameras[0].id : null;
      if (cameraId) {
        html5QrCode.start(
          cameraId,
          qrConfig,
          (decodedText, decodedResult) => {
            // decodedText typically contains the meter id
            meterInput.value = decodedText.replace(/^meter[:\s]*/i, '').trim();
          },
          (errorMessage) => {
            // ignore decode errors
          }
        ).catch(err => console.error('QR start error', err));
      }
    }).catch(err => console.warn('No camera for QR', err));
  } else {
    console.warn('Html5Qrcode not available');
  }

  // 2) Start camera stream for capture
  navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false })
    .then(stream => {
      video.srcObject = stream;
    })
    .catch(err => {
      console.error('Camera error', err);
      alert('Camera not available: ' + err.message);
    });

  // Capture image to canvas and prepare blob
  btnCapture.addEventListener('click', function () {
    const width = video.videoWidth;
    const height = video.videoHeight;
    if (!width || !height) {
      alert('Video not ready - try again in a moment');
      return;
    }
    canvas.width = width;
    canvas.height = height;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, width, height);
    canvas.toBlob(blob => {
      lastBlob = blob;
      // Show a preview by opening in new tab (optional)
      // window.open(URL.createObjectURL(blob));
      alert('Photo captured. Now run OCR or edit reading manually.');
    }, 'image/jpeg', 0.9);
  });

  // 3) Run OCR using Tesseract.js on the captured blob
  btnOCR.addEventListener('click', function () {
    if (!lastBlob) {
      alert('Capture a photo first');
      return;
    }
    ocrTextEl.value = 'Running OCR...';
    Tesseract.recognize(lastBlob, 'eng', { logger: m => {
      // progress logs if needed
      console.log(m);
    }})
    .then(({ data }) => {
      ocrTextEl.value = data.text;
      // attempt to find a number (simple heuristic)
      const match = data.text.replace(/,/g, '.').match(/(\d{1,9}(?:[\.\,]\d{1,3})?)/);
      if (match) readingEl.value = match[1].replace(',', '.');
    })
    .catch(err => {
      ocrTextEl.value = 'OCR error: ' + err.message;
      console.error(err);
    });
  });

  // Helper to get CSRF token cookie
  function getCookie(name) {
    const v = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return v ? v.pop() : '';
  }

  // 4) Submit reading to server
  btnSubmit.addEventListener('click', function () {
    const meterId = meterInput.value && meterInput.value.trim();
    const readingValue = readingEl.value && readingEl.value.trim();
    if (!meterId || !readingValue) {
      alert('Meter ID and reading value are required');
      return;
    }
    const form = new FormData();
    form.append('meter_id', meterId);
    form.append('reading_value', readingValue);
    form.append('ocr_text', ocrTextEl.value || '');
    // append photo blob if we have it
    if (lastBlob) {
      form.append('photo', lastBlob, 'photo.jpg');
    }

    fetch('/billing/api/upload-reading/', {
      method: 'POST',
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
      },
      body: form
    })
    .then(resp => {
      if (!resp.ok) throw new Error('Upload failed: ' + resp.statusText);
      return resp.json();
    })
    .then(data => {
      alert('Saved reading: ' + data.reading_value + ' for meter ' + data.meter);
      // reset
      ocrTextEl.value = '';
      readingEl.value = '';
      lastBlob = null;
    })
    .catch(err => {
      console.error(err);
      alert('Failed to save: ' + err.message);
    });
  });
});