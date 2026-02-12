import os
import logging
import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# --- КОНФИГУРАЦИЯ ---
TELEGRAM_TOKEN = "8331990342:AAE7xFJA8IaSc0pH_tRFREtqivVJnwBR0FM"
GOOGLE_API_KEY = "AIzaSyCAHtSq-5bzFOHF0nEtB4XrLDjMstv3v-M"

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
chat_sessions = {}

# --- ФУНКЦИИ БОТА ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_sessions[chat_id] = model.start_chat(history=[])
    await update.message.reply_text("Слава, я на Render и теперь всё настроено под Python 3.13! Пиши.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in chat_sessions:
        chat_sessions[chat_id] = model.start_chat(history=[])
    
    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
    try:
        response = chat_sessions[chat_id].send_message(update.message.text)
        await update.message.reply_text(response.text, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await update.message.reply_text("Ошибка в Gemini. Попробуй еще раз.")

# --- ИСПРАВЛЕННЫЙ ЗАПУСК ДЛЯ RENDER ---
def main():
    # Мы используем стандартный запуск, который лучше работает в облаке
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    
    print("Бот Слава запускает проверку...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
