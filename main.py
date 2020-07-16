import os

import requests
import bs4

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
    file_vacancies = open('salaries/'+vacancy+'.txt', 'w')
    hrefs = get_href(vacancy, 10)
    for href in hrefs:
        res = requests.get(href)
        vacancy_page = bs4.BeautifulSoup(res.text)
        os.system('cls')
        
        salary = vacancy_page.select('.vacancy__salary')
        
        # Проверяет, указанна ли зарплата.
        if salary == []:
            # З/п не указанна, значит вакансия пропускается.
            
            continue
            
        salary = (salary[0].getText().replace('\t', '').
            replace('\n', '').replace(' ', '').replace('руб.', '').
            replace('ивыше', '').replace('\xa0', ''))
            
        company = vacancy_page.select('.org-info__item a')

        # Проверяет, указанна ли компания.
        if company == []:
            # Компания не указанна, значит вакансия пропускается.
            print('company')
            continue
            
        company = company[0].getText().replace('\t', '').replace('\n', '')
        
        vacancy_name = vacancy_page.select('.vacancy__title')

        # Проверяет, указанно ли название вакансии.
        if vacancy_name == []:
            # Вакансия не указанна, значит вакансия пропускается.
            print(href)
            continue
        
        vacancy_name = vacancy_name[0].getText().replace('\t', '').replace('\n', '')
        
        full_string = (str(company) + ' - ' + str(vacancy_name) + ' - '
            + str(salary) + '\n' )
            
                    
        file_vacancies.write(full_string)
    print('\a')
    file_vacancies.close()
    
def get_href(search, quantity = 1):
    ''' Возращает сслыки на первые quantity ответов, которые
        возращает сайт praca.by при поиске search.
    '''
    hrefs = []
    page_num = 1 # номер страницы.
    add_vacancy = 0 # сколько вакансий добавленнл
    while page_num < 4:
        res = requests.get('https://praca.by/search/vacancies/'+
            '?page='+ str(page_num) +'&search[query]=' + search +
            '&search[query-text-params][headline]=0&form-submit-btn=Найти')
        html_file = bs4.BeautifulSoup(res.text)
        os.system('cls')
        
        
        pages = html_file.select('.search-list .vac-small__title-link')
        for page in pages:
            hrefs.append(page.get('href'))
            add_vacancy += 1
            
            if add_vacancy >= quantity:
                return hrefs
            
        page_num += 1
    return hrefs

while True:
    print("Чтобы выйти нажмите Ctrl+C")
    vacancy = input("Введите название вакансии: ")
    main(vacancy)
    
