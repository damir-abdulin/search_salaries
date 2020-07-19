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
    logger.debug("Начало работы функции get_info")
    info = page.select(tag)
    logger.debug("Данные по тегу \"%s\" извлечены" %(tag))
    if info == []:
        return None
    return info
    
def add_excel(vacancy, companies, vacancy_names, salaries,
        vacancies_hrefs):
    ''' Выводит информацию в файл excel. '''
    logger.debug("Начало работы функции add_excel")
    try:
        wb = openpyxl.load_workbook('template.xlsx')
        logger.debug("Шаблон загружен")
    except:
        logger.critical("Ошибка загрузки шаблона")
        
        import sys
        sys.exit()
        
    sheet = wb['Sheet']
    for row in range(len(vacancy_names)):
        line = row+5
        try:
            sheet['B' + str(line)] = companies[row] # наименование нанимателя
            sheet['C' + str(line)] = salaries[row] # Бел. руб.
            sheet['F' + str(line)] = vacancy_names[row] # Специальность
            sheet['G' + str(line)] = vacancies_hrefs[row] # Ссылка
            logger.debug("Данные в строку %d загружены" %(line))
        except:
            logger.error("Ошибка записи в строку %d" % (line))
            break
    file_name = 'salaries\\' + vacancy + '.xlsx'
    try:
        wb.save(file_name)
        logger.info("Файл %s успешно создан" % (file_name))
    except:
        print("Что-то пошло не так.")
        logger.error("Ошибка создания файла %s" % (file_name))
        
