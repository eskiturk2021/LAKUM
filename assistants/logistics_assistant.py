import logging
from assistants.base_assistant import BaseAssistant
from config import LOGISTIC_ASSISTANT_ID, GOOGLE_MAPS_API_KEY, BAKERY_COORDINATES
import googlemaps
from datetime import datetime

logger = logging.getLogger(__name__)

class LogisticsAssistant(BaseAssistant):
    def __init__(self):
        super().__init__(LOGISTIC_ASSISTANT_ID)
        self.gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
        self.max_distance = 30000  # 30 км в метрах

    def process_address(self, thread, address):
        try:
            # Получаем координаты адреса клиента
            geocode_result = self.gmaps.geocode(address)
            if not geocode_result:
                return "Не удалось найти указанный адрес. Пожалуйста, уточните адрес доставки."

            client_location = geocode_result[0]['geometry']['location']

            # Вычисляем расстояние между пекарней и клиентом
            distance_result = self.gmaps.distance_matrix(
                f"{BAKERY_COORDINATES[0]},{BAKERY_COORDINATES[1]}",
                f"{client_location['lat']},{client_location['lng']}",
                mode="driving",
                units="metric"
            )

            if distance_result['status'] == 'OK':
                distance = distance_result['rows'][0]['elements'][0]['distance']['value']
                if distance <= self.max_distance:
                    response = self.process_message(thread, f"Адрес клиента: {address}")
                    logger.info(f"Ответ логиста: {response}")
                    return f"Адрес подтвержден. Расстояние: {distance / 1000:.2f} км. {response}"
                else:
                    return f"К сожалению, ваш адрес находится слишком далеко (расстояние: {distance / 1000:.2f} км). Максимальное расстояние доставки - 30 км."
            else:
                return "Не удалось рассчитать расстояние. Пожалуйста, проверьте правильность адреса."

        except Exception as e:
            logger.error(f"Ошибка при обработке адреса: {str(e)}")
            return "Произошла ошибка при обработке адреса. Пожалуйста, попробуйте еще раз или свяжитесь с поддержкой."