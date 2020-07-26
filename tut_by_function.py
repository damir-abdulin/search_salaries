# Функции для сбора информации с сайта jobs.tut.by
import requests
import bs4

import function

from settings import Settings

# Подключение настроек.
s = Settings()

# Запускает логирование.
import logging

logger = logging.getLogger(__name__)

def get_hrefs(city, vacancy, quantity=10):
    """ Находит ссылки, с которых будет собираться информация.
        
        Выводит первые quantity ссылок, которые возращаются
        через поисковой запрос на сайте jobs.tut.by по слову vacancy.
    """
    logger.debug("Начало работы функции get_hrefs")
    
def extraction_information(href):
    """ Извлекает необходимую информацию с ссылки href. """
    logger.debug("Начало работы функции extraction_information")
