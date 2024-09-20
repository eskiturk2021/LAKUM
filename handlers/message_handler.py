import json
import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import STAGE_LOGISTICS, STAGE_MENU, STAGE_CASHIER
from assistants.logistics_assistant import LogisticsAssistant
from assistants.cashier_assistant import CashierAssistant
from utils.telegram_utils import send_menu_pdfs

logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.web_app_data:
        data = json.loads(update.message.web_app_data.data)
        address = data['address']
        distance = data['distance']
        
        if "км" in distance:
            distance_km = float(distance.split()[0].replace(',', '.'))
            if distance_km > 30:
                await update.message.reply_text(f"К сожалению, ваш адрес находится слишком далеко (расстояние: {distance}). Максимальное расстояние доставки - 30 км.")
                return

        context.user_data['address'] = address
        context.user_data['stage'] = STAGE_MENU
        await update.message.reply_text(f"Адрес подтвержден: {address}. Расстояние: {distance}")
        await send_menu_pdfs(update, context)
        await update.message.reply_text("Что бы вы хотели заказать?")
        return

    user_input = update.message.text

    if 'thread' not in context.user_data:
        await update.message.reply_text('Пожалуйста, нажмите кнопку "Сделать заказ 🍽️" для начала.')
        return

    thread = context.user_data['thread']
    current_stage = context.user_data.get('stage', STAGE_LOGISTICS)

    logger.info(f"Текущая стадия: {current_stage}")

    if current_stage == STAGE_MENU:
        context.user_data['stage'] = STAGE_CASHIER
        cashier_assistant = CashierAssistant()
        response = cashier_assistant.process_order(thread, f"Новый заказ: {user_input}")
        
        message = await update.message.reply_text("Обрабатываю ваш заказ...")
        
        for i in range(len(response)):
            if i % 20 == 0 and i != 0:
                await message.edit_text(response[:i])

        await message.edit_text(response)

    elif current_stage == STAGE_CASHIER:
        cashier_assistant = CashierAssistant()
        response = cashier_assistant.process_order(thread, user_input)
        
        message = await update.message.reply_text("Обрабатываю вашу информацию...")
        
        for i in range(len(response)):
            if i % 20 == 0 and i != 0:
                await message.edit_text(response[:i])

        await message.edit_text(response)

    else:
        await update.message.reply_text("Извините, произошла ошибка. Пожалуйста, нажмите кнопку 'Сделать заказ 🍽️' для начала.")

    logger.info(f"Новая стадия: {context.user_data.get('stage')}")