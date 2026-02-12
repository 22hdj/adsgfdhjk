import os
import logging
import asyncio
import google.generativeai as genai
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# --- КОНФИГУРАЦИЯ ---
# Вставь сюда свои настоящие ключи, если они другие
TELEGRAM_TOKEN = "8331990342:AAE7xFJA8IaSc0pH_tRFREtqivVJnwBR0FM"
GOOGLE_API_KEY = "AIzaSyCAHtSq-5bzFOHF0nEtB4XrLDjMstv3v-M"

# Настройка логов
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Настройка Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
chat_sessions = {}

# --- ФУНКЦИИ БОТА ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    chat_sessions[chat_id] = model.start_chat(history=[])
    await update.message.reply_text("Слава, я успешно запустился на Render! Жду твоих команд.")

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
        await update.message.reply_text("Произошла ошибка при ответе. Попробуй позже.")

# --- ЗАПУСК ---
if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_text))
    
    print("Бот Слава запущен...")
    application.run_polling()
