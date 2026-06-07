import os
import secrets
import string
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن يتم جلبه من إعدادات Render بأمان
TOKEN = os.getenv('8557584212:AAFlYfgMjRh35UA2QtI_7fVeoEIOI1lrjZ8')

def check_password_strength(password):
    if len(password) < 8: return "ضعيف جداً ❌"
    if any(c.isdigit() for c in password) and any(c.isupper() for c in password):
        return "قوي جداً ✅"
    return "متوسط ⚠️"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🔐 توليد باسورد قوي", "🔍 فحص قوة باسورد"],
        ["🛡️ نصائح الحماية", "📞 تواصل مع المطور"],
        ["💻 أدوات تعليمية", "⚠️ تنبيهات أمنية"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text('أهلاً بك يا بطل! أنا بوتك الأمني، اختر ما تحتاجه:', reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🔐 توليد باسورد قوي":
        pwd = ''.join(secrets.choice(string.ascii_letters + string.digits + "!@#$%") for _ in range(16))
        await update.message.reply_text(f"الباسورد المقترح:\n`{pwd}`", parse_mode='Markdown')
    
    elif text == "🛡️ نصائح الحماية":
        await update.message.reply_text("نصيحة: لا تفتح روابط مجهولة، واستخدم المصادقة الثنائية (2FA) دائماً.")
        
    elif text == "📞 تواصل مع المطور":
        await update.message.reply_text("يمكنك التواصل مع المطور من هنا: @Mohamed018776")
        
    elif text == "💻 أدوات تعليمية":
        await update.message.reply_text("تعلم من منصات مثل: TryHackMe أو HackTheBox.")
        
    elif text == "🔍 فحص قوة باسورد":
        await update.message.reply_text("أرسل لي الباسورد الآن وسأخبرك بقوته.")
        context.user_data['waiting_for_password'] = True
        
    elif context.user_data.get('waiting_for_password'):
        strength = check_password_strength(text)
        await update.message.reply_text(f"حالة الباسورد الخاص بك: {strength}")
        context.user_data['waiting_for_password'] = False

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
