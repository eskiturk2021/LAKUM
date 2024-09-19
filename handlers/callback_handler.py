from telegram import Update
from telegram.ext import ContextTypes
from handlers.start_handler import start_order_process

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'start_order':
        await start_order_process(update, context)