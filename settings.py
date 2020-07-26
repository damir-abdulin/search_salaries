import os

class Settings():
    """ Содержит настройки для приложения searc_salaries."""
    def __init__(self):
        """ Инициализирует настройки приложения. """
        # Настройки логирования.
        self.log_format = ('[LINE:%(lineno)d][%(asctime)s] # ' + 
            '%(levelname)s (%(name)s): %(message)s')
        self.log_dir = 'logs'
        
        # Настройки запросов.
        self.headers = {'user-agent':
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) ' +
            'AppleWebKit/537.36 (KHTML, like Gecko) ' + 
            'Chrome/53.0.2785.143 ' + 
            'Safari/537.36'}
            
        # Настройки сайтов.
        self.sites = 'praca'
        
    def get_logs_filename(self):
        """ Вычисляет название для лог-файла. """
        import datetime
        
        today = datetime.date.today()
        log_name = (self.log_dir + '\\' + today.strftime("%d-%m-%Y") + 
            '.log')
        return log_name
        
    def start_logging(self):
        """ Запускает логирование приложения. """
        import logging

        logging.basicConfig(
            filename=self.get_logs_filename(),
            level=logging.DEBUG,
            format=self.log_format)
    
    def delete_logs(self):
        """ Удаляет файлы логов по условию.
            
            Условие удаления логов:
                Если вес папки logs превышает 1Мб,
                то удаляются старые файлы, пока лимит будет превышен.
        """
        dir_size = self.get_size(self.log_dir)
        while dir_size > 1024*1024:
            elder_file = self.get_elder_file(self.log_dir)
            os.remove(elder_file)
            
    def get_size(self, directory):
        """ Ищет размер папки directory. """
        os.chdir(directory)
        dir_size = 0
        files = os.listdir()
        for filename in files:
            dir_size += os.stat(filename).st_size
        os.chdir('..')
        return dir_size
        
    def get_elder_file(self, directory):
        """ Ищет файл, который был создан раньше всех. """
        os.chdir(directory)
        files = os.listdir()
        try:
            elder_file = files[0]
        except:
            return
        elder_ctime = os.stat(elder_file).st_ctime
        for filename in files:
            ctime = os.stat(filename).st_ctime
            if ctime < elder_ctime:
                elder_file = filename
                elder_ctime = os.stat(elder_file).st_ctime
        elder_file = directory + '\\' + elder_file
        os.chdir('..')
        return elder_file
    
    def stop_program(self):
        """ Завершает работу программы. """
        import sys
        sys.exit()
