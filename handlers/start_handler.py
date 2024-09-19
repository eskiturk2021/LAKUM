from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import STAGE_LOGISTICS
from assistants.logistics_assistant import LogisticsAssistant


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton("Сделать заказ 🍽️", callback_data='start_order')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Добро пожаловать в пекарню "ЛАКУМ"! Нажмите кнопку ниже, чтобы сделать заказ.',
                                    reply_markup=reply_markup)


async def start_order_process(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data.clear()
    context.user_data['stage'] = STAGE_LOGISTICS
    logistics_assistant = LogisticsAssistant()
    thread = logistics_assistant.create_thread()
    context.user_data['thread'] = thread

    message = await update.effective_message.reply_text('Отлично! Давайте начнем оформление заказа.')
    await message.edit_text(message.text + '\nДля начала давайте уточним детали доставки.')
    await message.edit_text(message.text + '\nПожалуйста, укажите ваш адрес.')