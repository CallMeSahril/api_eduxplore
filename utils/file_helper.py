import requests
import os
from datetime import datetime

def save_image_from_url(image_url):
    try:
        response = requests.get(image_url)
        response.raise_for_status()

        ext = image_url.split('.')[-1]
        if '?' in ext:
            ext = ext.split('?')[0]
        if ext.lower() not in ['jpg', 'jpeg', 'png']:
            ext = 'jpg'

        filename = f"soal_{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
        filepath = os.path.join("uploads", filename)

        os.makedirs("uploads", exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(response.content)

        return filepath  # contoh: uploads/soal_20250530103455.jpg
    except Exception as e:
        print(f"[ERROR] Gagal download gambar: {e}")
        return None
