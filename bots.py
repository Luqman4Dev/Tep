import os
import subprocess
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

# 🔹 توكن بوت التنصيب ثابت هنا (لتشغيل البوت فقط)
BOT_TOKEN = "6729948368:AAGAWxKLIDDV7j6ciodsGwp6rV_as33GFEM"

# الحالات في ConversationHandler للفارات الخاصة بالسورس
API_HASH, STRING_SESSION, TG_BOT_TOKEN, APP_ID = range(4)

# نص الترحيب أثناء إدخال الفارات
START_TEXT = """
🎉 أهلاً بك في بوت تنصيب Tepthon! 🎉

هذا البوت سيقوم بجمع الفارات المطلوبة لتشغيل سورس Tepthon وتثبيت مكتبته تلقائيًا.

💡 التعليمات:
1. أدخل API_HASH للسورس.
2. أدخل STRING_SESSION للسورس.
3. أدخل TG_BOT_TOKEN للسورس.
4. أدخل APP_ID للسورس.

🔒 جميع البيانات تبقى سرية ولن يتم مشاركتها مع أي شخص.

لإلغاء العملية في أي وقت ارسل /cancel
"""

ENV_FILE = ".env"

# قراءة محتويات .env الحالية
def read_env():
    env_vars = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key] = value
    return env_vars

# كتابة القيم إلى .env
def write_env(env_vars):
    with open(ENV_FILE, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

# /start يعطي ترحيب عام
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 أهلاً بك! لاستخدام بوت تنصيب Tepthon أرسل /Tepthon"
    )

# بداية ConversationHandler عند /Tepthon
async def tepthon_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT)
    await update.message.reply_text("➡️ ارسل الآن API_HASH للسورس:")
    return API_HASH

# استلام API_HASH
async def get_api_hash(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["API_HASH"] = update.message.text.strip()
    await update.message.reply_text("✅ تم حفظ API_HASH.\n➡️ الآن ارسل STRING_SESSION للسورس:")
    return STRING_SESSION

# استلام STRING_SESSION
async def get_string_session(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["STRING_SESSION"] = update.message.text.strip()
    await update.message.reply_text("✅ تم حفظ STRING_SESSION.\n➡️ الآن ارسل TG_BOT_TOKEN للسورس:")
    return TG_BOT_TOKEN

# استلام TG_BOT_TOKEN
async def get_bot_token(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["TG_BOT_TOKEN"] = update.message.text.strip()
    await update.message.reply_text("✅ تم حفظ TG_BOT_TOKEN.\n➡️ الآن ارسل APP_ID للسورس:")
    return APP_ID

# استلام APP_ID وتنفيذ الإضافة وتشغيل Tepthon
async def get_app_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["APP_ID"] = update.message.text.strip()

    # قراءة env الحالي
    env_vars = read_env()

    # إزالة API_ID إذا وجد (لأن السورس لا يحتاجه)
    env_vars.pop("API_ID", None)

    # إضافة الفارات الخاصة بالسورس
    env_vars["API_HASH"] = context.user_data["API_HASH"]
    env_vars["STRING_SESSION"] = context.user_data["STRING_SESSION"]
    env_vars["TG_BOT_TOKEN"] = context.user_data["TG_BOT_TOKEN"]
    env_vars["APP_ID"] = context.user_data["APP_ID"]

    # كتابة env المحدث
    write_env(env_vars)

    await update.message.reply_text(
        "🎉 تم حفظ جميع بيانات السورس بنجاح!\n"
        "♻️ جاري تثبيت مكتبات سورس Tepthon وتشغيله ..."
    )

    # تثبيت مكتبات Tepthon
    subprocess.run(["pip3", "install", "-r", "requirements.txt"])

    # تشغيل Tepthon مباشرة
    subprocess.Popen(["python3", "-m", "Tepthon"])

    return ConversationHandler.END

# إلغاء العملية
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ تم إلغاء العملية. يمكنك البدء لاحقًا بإرسال /Tepthon")
    return ConversationHandler.END

# تشغيل البوت
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("Tepthon", tepthon_start)],
        states={
            API_HASH: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_api_hash)],
            STRING_SESSION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_string_session)],
            TG_BOT_TOKEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_bot_token)],
            APP_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_app_id)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    print("🤖 Installer Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
