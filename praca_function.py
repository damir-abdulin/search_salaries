# Функции для сбора информации с сайта praca.by
import requests
import bs4

import function

def get_hrefs(vacancy, quantity=10):
    """ Находит ссылки, с которых будет собираться информация.
        
        Выводит первые quantity ссылок, которые возращаются
        через поисковой запрос на сайте praca.by по слову vacancy.
    """
    hrefs = []
    page_num = 1 # номер страницы.
    add_vacancy = 0 # сколько вакансий добавленно.
    
    while True:
        res = requests.get('https://praca.by/search/vacancies/'+
            '?page='+ str(page_num) +'&search[query]=' + vacancy +
            '&search[query-text-params][headline]=0&form-submit-btn=' +
            'Найти')
        html_file = bs4.BeautifulSoup(res.text)        
        
        pages = html_file.select('.search-list .vac-small__title-link')
        
        if pages == []: # нет вакансий
            return hrefs
        
        for page in pages:
            hrefs.append(page.get('href'))
            add_vacancy += 1
            
            if add_vacancy >= quantity:
                return hrefs
            
        page_num += 1

def extraction_information(href):
    """ Извлекает необходимую информацию с ссылки href. """
    res = requests.get(href)
    vacancy_page = bs4.BeautifulSoup(res.text)
    
    salary = function.get_info(vacancy_page, '.vacancy__salary')
    
    if not salary:
        return None

    salary = (salary[0].getText().replace('\t', '').
        replace('\n', '').replace(' ', '').replace('руб.', '').
        replace('ивыше', '').replace('\xa0', ''))
        
    company = function.get_info(vacancy_page, '.org-info__item a')
    
    if not company:
        return None
        
    company = (company[0].getText().replace('\t', '').
        replace('\n', ''))
    
    vacancy_name = function.get_info(vacancy_page, '.vacancy__title')
    
    if not vacancy_name:
        return None
    
    vacancy_name = (vacancy_name[0].getText().replace('\t', '').
        replace('\n', ''))
        
    return company, vacancy_name, salary

def make_excel_file(vacancy):
    """ Создает файл excel по вакансиям с сайта praca.by """
    companies = []
    vacancy_names = []
    salaries =[]
    vacancies_hrefs = []
    
    hrefs = get_hrefs(vacancy, 50)
    for href in hrefs:
        try:
            company, vacancy_name, salary = extraction_information(href)
        except:
            continue
        
        companies.append(str(company))
        vacancy_names.append(str(vacancy_name))
        salaries.append(str(salary))
        vacancies_hrefs.append(href)
        
    function.add_excel(vacancy, companies, vacancy_names, salaries,
        vacancies_hrefs)
        
