# استخدام نسخة بايثون رسمية وخفيفة
FROM python:3.10-slim

# ضبط متغيرات البيئة لمنع تجميد بايثون
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# تثبيت مكتبات النظام اللازمة لمعالجة الصور
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# تثبيت مكتبات بايثون
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود بالكامل
COPY . .

# أمر التشغيل
CMD ["python", "app.py"]
