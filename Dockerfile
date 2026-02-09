# استخدام نسخة بايثون رسمية وخفيفة
# سنستخدم نسخة كاملة بدلاً من slim لتجنب التحميل من الخارج
FROM python:3.10

# منع بايثون من إنشاء ملفات pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# لن نحتاج لـ apt-get update هنا لأن النسخة الكاملة تحتوي على المكتبات غالباً
# سنكتفي بتثبيت مكتبات بايثون مباشرة
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "app.py"]


# تثبيت مكتبات بايثون
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود بالكامل
COPY . .

# أمر التشغيل
CMD ["python", "app.py"]
