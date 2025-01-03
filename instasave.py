from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import instaloader
import requests
import os

# Instagram videoni yuklab olish funksiyasi
def download_instagram_video(link):
    try:
        loader = instaloader.Instaloader()
        # Havoladan shortcode'ni ajratib olish
        if "/reel/" in link or "/p/" in link:
            shortcode = link.split("/")[-2]
        else:
            return "Xato: Instagram havolasi noto'g'ri."

        # Post ma'lumotlarini olish
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # Video URL'ni olish
        if post.is_video:
            video_url = post.video_url
            file_name = "instagram_video.mp4"

            # requests kutubxonasi orqali video yuklash
            response = requests.get(video_url)
            if response.status_code == 200:
                with open(file_name, 'wb') as f:
                    f.write(response.content)
                return file_name
            else:
                return f"Xato: Video yuklanmadi, HTTP status: {response.status_code}"
        else:
            return "Xato: Bu havola video uchun emas."
    except Exception as e:
        return f"Xato: {str(e)}"

# /start komandasi
async def start(update: Update, context) -> None:
    await update.message.reply_text("Salom! Instagramdan video yuklash uchun link yuboring.")

# Instagram linkini qayta ishlash
async def handle_instagram_link(update: Update, context) -> None:
    link = update.message.text

    if "instagram.com" in link:
        await update.message.reply_text("Video yuklanmoqda, kuting...")
        file_name = download_instagram_video(link)

        # Faylni foydalanuvchiga yuborish
        if os.path.exists(file_name):
            await context.bot.send_video(chat_id=update.effective_chat.id, video=open(file_name, "rb"))
            os.remove(file_name)  # Yuklab olingan faylni o'chirish
        else:
            await update.message.reply_text(file_name)
    else:
        await update.message.reply_text("Iltimos, to'g'ri Instagram linkini yuboring!")

# Botni ishga tushirish
def main():
    TOKEN = "7626491002:AAHVI9QxB30ejGhqYFr_ZRcbMGIUa3eh9Ighttps://www.instagram.com/reel/DEVKywpimJv/?igsh=Y2xzMHppaGtqeXFl"  # O'z tokeningizni bu yerga kiriting
    application = Application.builder().token(TOKEN).build()

    # Handlerlarni qo'shish
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_link))

    # Botni ishga tushirish
    application.run_polling()

if __name__ == "__main__":
    main()
