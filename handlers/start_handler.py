from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import ContextTypes
from config import STAGE_LOGISTICS, WEB_APP_URL
from assistants.logistics_assistant import LogisticsAssistant

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Сделать заказ 🍽️", callback_data='start_order')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Добро пожаловать в пекарню "ЛАКУМ"! Нажмите кнопку ниже, чтобы сделать заказ.', reply_markup=reply_markup)

async def start_order_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.clear()
    context.user_data['stage'] = STAGE_LOGISTICS
    logistics_assistant = LogisticsAssistant()
    thread = logistics_assistant.create_thread()
    context.user_data['thread'] = thread
    
    keyboard = [[InlineKeyboardButton("Ввести адрес", web_app=WebAppInfo(url=WEB_APP_URL))]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text('Пожалуйста, введите ваш адрес:', reply_markup=reply_markup)