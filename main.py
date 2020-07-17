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

def main(vacancy):
    ''' Печатает информацию о вакансии в файл по следующему образцу:
        название компании - название вакансии - з/п
        
        Принцип работы:
            1) Производит поиск подходящей вакансии.
            2) Собирает сслыки на 50 первых вакансий.
            3) Циклом проходит каждую вакансию и собирает
               необходимую информацию (если чего-то нет, то
               пропускает вакансию).
            4) Записывает необходимую информацию в файл.
    '''
    logging.debug("Старт основной функции по запросу: " + vacancy)
    
    companies = []
    vacancy_names = []
    salaries =[]
    hrefs = get_href(vacancy, 50)
    for href in hrefs:
        res = requests.get(href)
        vacancy_page = bs4.BeautifulSoup(res.text)
        
        salary = vacancy_page.select('.vacancy__salary')
        
        # Проверяет, указанна ли зарплата.
        if salary == []:
            # З/п не указанна, значит вакансия пропускается.
            logging.warning("Нет информации о зарплате. Вакансия:\n\t" +
                href)
            continue
            
        salary = (salary[0].getText().replace('\t', '').
            replace('\n', '').replace(' ', '').replace('руб.', '').
            replace('ивыше', '').replace('\xa0', ''))
            
        company = vacancy_page.select('.org-info__item a')

        # Проверяет, указанна ли компания.
        if company == []:
            # Компания не указанна, значит вакансия пропускается.
            logging.warning("Нет информации о компании. Вакансия:\n\t" +
                href)
            continue
            
        company = company[0].getText().replace('\t', '').replace('\n', '')
        
        vacancy_name = vacancy_page.select('.vacancy__title')

        # Проверяет, указанно ли название вакансии.
        if vacancy_name == []:
            # Вакансия не указанна, значит вакансия пропускается.
            logging.warning("Нет информации об имени вакансии." +
                "Вакансия:\n\t" + href)
            continue
        
        vacancy_name = vacancy_name[0].getText().replace('\t', '').replace('\n', '')
        companies.append(str(company))
        vacancy_names.append(str(vacancy_name))
        salaries.append(str(salary))
    
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
            logging.debug("Ссылка на вакансии извлечены")
            return hrefs
        
        for page in pages:
            hrefs.append(page.get('href'))
            add_vacancy += 1
            logging.debug("Добавлена новая ссылка на вакансию №" +
                str(add_vacancy))
            
            if add_vacancy >= quantity:
                logging.debug("Ссылки на вакансии извлечены")
                return hrefs
            
        page_num += 1
    
def add_excel(vacancy, companies, vacancy_names, salaries):
    ''' Выводит информацию в файл excel. '''
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
    logging.debug("Запись в файл salaries\\" + vacancy +
        ".xlsx завершена")

logging.debug("Старт программы")
while True:
    print("Чтобы выйти нажмите Ctrl+C")
    vacancy = input("Введите название вакансии: ")
    main(vacancy)
