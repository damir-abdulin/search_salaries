# Содержит общие функции для search_salaries.
import openpyxl

# Запускает логирование.
import logging

logger = logging.getLogger(__name__)

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
    logger.info("All good")
    info = page.select(tag)
    
    if info == []:
        return None
    return info
    
def add_excel(vacancy, companies, vacancy_names, salaries,
        vacancies_hrefs):
    ''' Выводит информацию в файл excel. '''
    wb = openpyxl.load_workbook('template.xlsx')
    sheet = wb['Sheet']
    for row in range(len(vacancy_names)):
        try:
            sheet['B' + str(row+5)] = companies[row] # наименование нанимателя
            sheet['C' + str(row+5)] = salaries[row] # Бел. руб.
            sheet['F' + str(row+5)] = vacancy_names[row] # Специальность
            sheet['G' + str(row+5)] = vacancies_hrefs[row] # Ссылка
        except:
            break
    wb.save('salaries\\' + vacancy + '.xlsx')
