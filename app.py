import os
import io
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from flask import Flask
from threading import Thread

# 1. إعداد سيرفر الويب الصغير لـ Render
app_web = Flask('')
@app_web.route('/')
def home():
    return "AI Bot is Live and linked to Hugging Face!"

def run_flask():
    port = int(os.environ.get('PORT', 10000))
    app_web.run(host='0.0.0.0', port=port)

Thread(target=run_flask).start()

# 2. إعدادات الربط مع Hugging Face (المصنع)
# تأكد أنك أضفت HF_TOKEN في إعدادات Render
API_URL = "https://api-inference.huggingface.co/models/ZhengPeng7/BiRefNet"
HF_TOKEN = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query_hugging_face(image_bytes):
    response = requests.post(API_URL, headers=headers, data=image_bytes)
    return response.content

async def process_and_remove_bg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status_msg = await update.message.reply_text("⏳ جاري المعالجة في مختبر الهجين...")
    try:
        # تحميل الصورة من تليجرام
        photo_file = await update.message.photo[-1].get_file()
        photo_bytes = await photo_file.download_as_bytearray()
        
        # إرسال الصورة لهجين وقص الخلفية هناك
        processed_image_bytes = query_hugging_face(photo_bytes)
        
        # إرسال النتيجة للمستخدم
        out_io = io.BytesIO(processed_image_bytes)
        out_io.name = "no_bg.png"
        await update.message.reply_document(document=out_io, caption="✨ تمت المعالجة بواسطة Hugging Face!")
        
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("❌ حدث تأخير في الاستجابة، حاول مرة أخرى.")
    finally:
        await status_msg.delete()

if __name__ == '__main__':
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if BOT_TOKEN:
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        app.add_handler(MessageHandler(filters.PHOTO, process_and_remove_bg))
        print("🚀 البوت يعمل الآن بالربط الهجين...")
        app.run_polling()
