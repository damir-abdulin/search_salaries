import praca_function as praca
import function

from settings import Settings

# Подключение настроек.
s = Settings()

# Запускает логирование.
import logging

s.start_logging()

logger = logging.getLogger(__name__)
logging.disable(logging.DEBUG)

logger.info("Старт программы")
while True:
    print("Чтобы выйти нажмите Ctrl+C")
    vacancy = input("Введите название вакансии: ")
    logging.debug("Полученная вакансия: " + vacancy)
    praca.make_excel_file(vacancy)
