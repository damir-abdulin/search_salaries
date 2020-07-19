# Функции для сбора информации с сайта praca.by
import requests
import bs4

import function

from settings import Settings

# Подключение настроек.
s = Settings()

# Запускает логирование.
import logging

logger = logging.getLogger(__name__)

def get_hrefs(vacancy, quantity=10):
    """ Находит ссылки, с которых будет собираться информация.
        
        Выводит первые quantity ссылок, которые возращаются
        через поисковой запрос на сайте praca.by по слову vacancy.
    """
    logger.debug("Начало работы функции get_hrefs")
    hrefs = []
    page_num = 1 # номер страницы.
    add_vacancy = 0 # сколько вакансий добавленно.
    
    while True:
        res = requests.get('https://praca.by/search/vacancies/'+
            '?page='+ str(page_num) +'&search[query]=' + vacancy +
            '&search[query-text-params][headline]=0&form-submit-btn=' +
            'Найти')
        if res.status_code == 200:
            logger.debug("Страница %s успешно получена" % (res.url))
        else:
            logger.debug("Ошибка получения страницы %s" % (res.url))
        
        html_file = bs4.BeautifulSoup(res.text, "html.parser")        
        
        pages = html_file.select('.search-list .vac-small__title-link')
        
        if pages == []: # нет вакансий
            logger.debug("Нет вакансий по адресу " + res.url)
            logger.debug("Завершение работы функции get_hrefs")
            return hrefs
        
        for page in pages:
            hrefs.append(page.get('href'))
            add_vacancy += 1
            logger.debug("Ссылка(%d из %d) добавлена" %
                (add_vacancy, quantity))
            
            if add_vacancy >= quantity:
                logger.debug("Массив ссылок создан")
                logger.debug("Завершение работы функции get_hrefs")
                return hrefs
            
        page_num += 1

def extraction_information(href):
    """ Извлекает необходимую информацию с ссылки href. """
    logger.debug("Начало работы функции extraction_information")
    res = requests.get(href)
    
    if res.status_code == 200:
        logger.debug("Страница %s успешно получена" % (res.url))
    else:
        logger.debug("Ошибка получения страницы %s" % (res.url))
        
    vacancy_page = bs4.BeautifulSoup(res.text, "html.parser")
    
    salary = function.get_info(vacancy_page, '.vacancy__salary')
    
    if not salary:
        logger.debug("Нет информации об зарплате (%s)" % (res.urls))
        logger.debug("Завершение работы функции extraction_information")
        return None

    salary = (salary[0].getText().replace('\t', '').
        replace('\n', '').replace(' ', '').replace('руб.', '').
        replace('ивыше', '').replace('\xa0', ''))
        
    company = function.get_info(vacancy_page, '.org-info__item a')
    
    if not company:
        logger.warning("Нет информации об компании (%s)" % (res.urls))
        logger.debug("Завершение работы функции extraction_information")
        return None
        
    company = (company[0].getText().replace('\t', '').
        replace('\n', ''))
    
    vacancy_name = function.get_info(vacancy_page, '.vacancy__title')
    
    if not vacancy_name:
        logger.warning("Нет информации об вакансии (%s)" % (res.urls))
        logger.debug("Завершение работы функции extraction_information")
        return None
    
    vacancy_name = (vacancy_name[0].getText().replace('\t', '').
        replace('\n', ''))
    
    logger.debug("Завершение работы функции extraction_information")
    return company, vacancy_name, salary

def make_excel_file(vacancy):
    """ Создает файл excel по вакансиям с сайта praca.by """
    logger.debug("Начало работы функции make_excel_file")
    companies = []
    vacancy_names = []
    salaries =[]
    vacancies_hrefs = []
    
    hrefs = get_hrefs(vacancy, 50)
    for href in hrefs:
        logger.debug("Обработка ссылки " + href)
        try:
            company, vacancy_name, salary = extraction_information(href)
        except:
            continue
        
        companies.append(str(company))
        vacancy_names.append(str(vacancy_name))
        salaries.append(str(salary))
        vacancies_hrefs.append(href)
        logger.debug("Информация добавлена")
    
    logger.info("Вся нужная информация с сайта praca.by собрана")
    function.add_excel(vacancy, companies, vacancy_names, salaries,
        vacancies_hrefs)
    logger.debug("Завершение работы функции make_excel_file")
        
