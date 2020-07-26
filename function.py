# Содержит общие функции для search_salaries.
import openpyxl
import logging

from settings import Settings

# Подключает настройки
s = Settings()

# Запускает логирование.
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
    
def add_excel(site, city, vacancy, companies, vacancy_names, salaries,
        vacancies_hrefs):
    ''' Выводит информацию в файл excel. 
        
        Аргументы:
            service -- название сервиса откуда берется информация.
            city -- название города.
            vacancy -- название вакансии.
            companies -- масив названий компаний.
            vacancy_names -- масив названий вакансий.
            salaries -- массив зарплат.
            vacancies_hrefs -- массив ссылок на зарплаты.
    '''
    logger.debug("Начало работы функции add_excel")
    try:
        wb = openpyxl.load_workbook('template.xlsx')
        logger.debug("Шаблон загружен")
    except:
        logger.critical("Ошибка загрузки шаблона")
        s.stop_program()
        
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
    try:
        file_name = ('salaries\\' + site + '_' + city + '_' + vacancy + 
            '.xlsx')
        wb.save(file_name)
        logger.info("Файл %s успешно создан" % (file_name))
    except:
        print("Что-то пошло не так.")
        logger.error("Ошибка создания файла %s" % (file_name))

def make_excel_file(site, city, vacancy,
    get_hrefs, extraction_information):
    """ Создает файл excel по вакансиям с сайта service.
        
        Аргументы:
            vacancy -- название вакансии.
            city -- название города.
            service -- название сервиса, где ищется вакансия.
            get_hrefs -- функция, которая получает ссылки.
            extraction_information -- функция, которая извлекает данные.
    """
    logger.debug("Начало работы функции make_excel_file")
    companies = []
    vacancy_names = []
    salaries =[]
    vacancies_hrefs = []
    
    hrefs = get_hrefs(city, vacancy, 50)
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
    add_excel(site, city, vacancy, companies, vacancy_names,
        salaries, vacancies_hrefs)
    logger.debug("Завершение работы функции make_excel_file")
