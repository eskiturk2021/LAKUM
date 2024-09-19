from telegram import Update
from telegram.ext import ContextTypes
from config import MENU_PDF_1, MENU_PDF_2

async def send_menu_pdfs(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    try:
        with open(MENU_PDF_1, 'rb') as menu1, open(MENU_PDF_2, 'rb') as menu2:
            await context.bot.send_document(chat_id=chat_id, document=menu1, filename='Меню 1.pdf')
            await context.bot.send_document(chat_id=chat_id, document=menu2, filename='Меню 2.pdf')
    except FileNotFoundError:
        await update.message.reply_text("Извините, не удалось найти файлы меню. Пожалуйста, свяжитесь с администратором.")