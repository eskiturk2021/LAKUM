from assistants.base_assistant import BaseAssistant
from config import CASHIER_ASSISTANT_ID

class CashierAssistant(BaseAssistant):
    def __init__(self):
        super().__init__(CASHIER_ASSISTANT_ID)

    def process_order(self, thread, order):
        return self.process_message(thread, f"Заказ клиента: {order}")