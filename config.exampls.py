import os

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "++++")

# OpenAI API configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "++++++++")

# OpenAI model
OPENAI_MODEL = "gpt-4o"  # или другая подходящая модель

# Assistant IDs
LOGISTIC_ASSISTANT_ID = "++++++++++++"
CASHIER_ASSISTANT_ID = "asst_++++++++++"

# Paths to menu PDF files
MENU_PDF_1 = "menu1.pdf"
MENU_PDF_2 = "menu2.pdf"

# Delivery zones (example)
DELIVERY_ZONES = ["Зона1", "Зона2", "Зона3"]

# Conversation stages
STAGE_LOGISTICS = "logistics"
STAGE_MENU = "menu"
STAGE_CASHIER = "cashier"

GOOGLE_MAPS_API_KEY = "+++++++++++++++++++++"
BAKERY_COORDINATES = (55, 3710)