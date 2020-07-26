import logging
import function

from settings import Settings

# Подключение настроек.
s = Settings()

# Удаляет лишние файлы логов.
s.delete_logs()

# Запускает логирование.
s.start_logging()
logger = logging.getLogger(__name__)

logger.info("Старт программы")
while True:
    print("Чтобы выйти нажмите Ctrl+C")
    try:
        vacancy = input("Введите название вакансии: ")
        city = input("Введите название нужного города: ")
    except KeyboardInterrupt:
        logger.debug("Работа программы завершена пользователем.")
        s.stop_program()
        
    logging.debug("Полученная вакансия: " + vacancy)
    logging.debug("Полученный город: " + city)
    
    for site in s.sites:
        # Импортирование нужных функций.
        site = s.sites
        module_name = site + '_function'
        try:
            module = __import__(module_name)
            logger.debug("Модуль %s подключен" % (module_name))
        except:
            logger.critical("Ошибка подключения модуля " + module_name)
            print("!!!КРИТИЧЕСКАЯ ОШИБКА!!!")
            s.stop_program()
        
        logging.info("Старт поиска по сайту " + site)
        function.make_excel_file(site, city, vacancy,
            module.get_hrefs, module.extraction_information)
        logging.info("Поиск по сайту %s завершен" % (site))
        print('\a')
        
        # FIX ME.
        break
