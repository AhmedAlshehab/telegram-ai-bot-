# استخدام نسخة بايثون رسمية وخفيفة
# تغيير النسخة لنسخة أكثر استقراراً
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# إضافة خيارات لإعادة المحاولة في حال فشل الشبكة
RUN apt-get update --fix-missing && apt-get install -y \
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
