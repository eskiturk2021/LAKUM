import logging
from telegram import Update
from telegram.ext import ContextTypes
from config import STAGE_LOGISTICS, STAGE_MENU, STAGE_CASHIER
from assistants.logistics_assistant import LogisticsAssistant
from assistants.cashier_assistant import CashierAssistant
from utils.telegram_utils import send_menu_pdfs

logger = logging.getLogger(__name__)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text

    if 'thread' not in context.user_data:
        await update.message.reply_text('Пожалуйста, нажмите кнопку "Сделать заказ 🍽️" для начала.')
        return

    thread = context.user_data['thread']
    current_stage = context.user_data.get('stage', STAGE_LOGISTICS)

    logger.info(f"Текущая стадия: {current_stage}")

    if current_stage == STAGE_LOGISTICS:
        logistics_assistant = LogisticsAssistant()
        response = logistics_assistant.process_address(thread, user_input)
        logger.info(f"Ответ логиста: {response}")

        message = await update.message.reply_text("Обрабатываю ваш адрес...")

        for i in range(len(response)):
            if i % 20 == 0 and i != 0:
                await message.edit_text(response[:i])

        await message.edit_text(response)

        if "Адрес подтвержден" in response:
            context.user_data['stage'] = STAGE_MENU
            await update.message.reply_text("Отлично! Сейчас я отправлю вам наше меню.")
            await send_menu_pdfs(update, context)
            await update.message.reply_text("Что бы вы хотели заказать?")

    elif current_stage == STAGE_MENU:
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
        await update.message.reply_text(
            "Извините, произошла ошибка. Пожалуйста, нажмите кнопку 'Сделать заказ 🍽️' для начала.")

    logger.info(f"Новая стадия: {context.user_data.get('stage')}")