import os

import requests
import bs4
import openpyxl

# Запускает логирование.
import logging
import datetime

today = datetime.date.today()
log_name = 'logs\\' + today.strftime("%d-%m-%Y") +  '.log'

log_format  = ('%(filename)s[LINE:%(lineno)d] - [%(asctime)s] | ' +
    '#%(levelname)s:\t%message)s')
logging.basicConfig(
    filename=log_name,
    level=logging.INFO,
    format='[LINE:%(lineno)d][%(asctime)s] # %(levelname)s -- %(message)s'
    )
logging.disable(logging.DEBUG)

def main(vacancy):
    ''' Вызывает необходимые функции для обработки запроса
        на вакансию.
    '''
    logging.debug("Старт основной функции по запросу: " + vacancy)
    
    companies = []
    vacancy_names = []
    salaries =[]
    
    hrefs = get_href(vacancy, 50)
    for href in hrefs:
        logging.debug("Обработка ссылки " + href)
        res = requests.get(href)
        vacancy_page = bs4.BeautifulSoup(res.text)
        
        salary = get_info(vacancy_page, '.vacancy__salary')
        
        # Проверяет, указанна ли зарплата.
        if not salary:
            continue
            
        salary = (salary[0].getText().replace('\t', '').
            replace('\n', '').replace(' ', '').replace('руб.', '').
            replace('ивыше', '').replace('\xa0', ''))
            
        company = get_info(vacancy_page, '.org-info__item a')

        # Проверяет, указанна ли компания.
        if not company:
            continue
            
        company = (company[0].getText().replace('\t', '').
            replace('\n', ''))
        
        vacancy_name = get_info(vacancy_page, '.vacancy__title')

        # Проверяет, указанно ли название вакансии.
        if not vacancy_name:
            continue
        
        vacancy_name = (vacancy_name[0].getText().replace('\t', '').
            replace('\n', ''))
            
        companies.append(str(company))
        vacancy_names.append(str(vacancy_name))
        salaries.append(str(salary))
        logging.debug("Данные по ссылки %s добавлены в массивы" %
            (href))
    
    add_excel(vacancy, companies, vacancy_names, salaries)
    print('\a')
    logging.info("Все вакансии по запросу \"%s\" добавлены\n" % (vacancy))
    
def get_href(search, quantity = 1):
    ''' Возращает сслыки на первые quantity ответов, которые
        возращает сайт praca.by при поиске search.
    '''
    logging.debug(("Извлечение первых %d вакансий по запросу: "
        + search) %(quantity))
    hrefs = []
    page_num = 1 # номер страницы.
    add_vacancy = 0 # сколько вакансий добавленнл
    while True:
        logging.debug("Обработка страницы: " + str(page_num))
        res = requests.get('https://praca.by/search/vacancies/'+
            '?page='+ str(page_num) +'&search[query]=' + search +
            '&search[query-text-params][headline]=0&form-submit-btn=Найти')
        html_file = bs4.BeautifulSoup(res.text)        
        
        pages = html_file.select('.search-list .vac-small__title-link')
        
        if pages == []: # нет вакансий
            logging.debug("Больше нет доступных ссылок")
            logging.info("Ссылки на вакансии извлечены")
            return hrefs
        
        for page in pages:
            hrefs.append(page.get('href'))
            add_vacancy += 1
            logging.debug("Добавлена новая ссылка на вакансию №" +
                str(add_vacancy))
            
            if add_vacancy >= quantity:
                logging.info("Ссылки на вакансии извлечены")
                return hrefs
            
        page_num += 1
        
def get_info(page, tag):
    ''' Извлекает данные из страницы page, которые
        соотвествуют запоросу tag. Если таких данных нет, то
        возращает None.
        
        Аргументы:
            page -- информация о странице.
                type(page) == <class 'bs4.BeautifulSoup'>
            tag -- по каким css-селекторам искать?
                type(tag) == str
    '''
    info = page.select(tag)
    
    if info == []:
        logging.info("На странице нет данных по тегу " + tag)
        return None
    return info
    
def add_excel(vacancy, companies, vacancy_names, salaries):
    ''' Выводит информацию в файл excel. '''
    logging.info("Загрузка в файл salaries\\" + vacancy +
        ".xlsx началась")
    wb = openpyxl.load_workbook('template.xlsx')
    sheet = wb['Sheet']
    for row in range(len(vacancy_names)):
        try:
            sheet['F' + str(row+5)] = companies[row]
            sheet['B' + str(row+5)] = vacancy_names[row]
            sheet['C' + str(row+5)] = salaries[row]
        except:
            logging.error("Ошибка записи в строку " + str(row+5))
            break
    wb.save('salaries\\' + vacancy + '.xlsx')
    logging.info("Запись в файл salaries\\" + vacancy +
        ".xlsx завершена")

logging.info("Старт программы")
while True:
    print("Чтобы выйти нажмите Ctrl+C")
    vacancy = input("Введите название вакансии: ")
    logging.debug("Полученная вакансия: " + vacancy)
    main(vacancy)
