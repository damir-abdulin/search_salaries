import praca_function as praca
import function

from settings import Settings

# Подключение настроек.
s = Settings()

# Удаляет лишние файлы логов.
s.delete_logs()

# Запускает логирование.
import logging

s.start_logging()

logger = logging.getLogger(__name__)

logger.info("Старт программы")
while True:
    print("Чтобы выйти нажмите Ctrl+C")
    try:
        vacancy = input("Введите название вакансии: ")
    except KeyboardInterrupt:
        logger.debug("Работа программы завершена пользователем.")
        
        import sys
        sys.exit()
        
    logging.debug("Полученная вакансия: " + vacancy)
    praca.make_excel_file(vacancy)
