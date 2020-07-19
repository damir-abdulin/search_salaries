class Settings():
    """ Содержит настройки для приложения searc_salaries."""
    def __init__(self):
        """ Инициализирует настройки приложения. """
        # Настройки логирования.
        self.log_format = ('[LINE:%(lineno)d][%(asctime)s] # ' + 
            '%(levelname)s (%(name)s): %(message)s')
    
    def get_logs_filename(self):
        """ Вычисляет название для лог-файла. """
        import datetime
        
        today = datetime.date.today()
        log_name = 'logs\\' + today.strftime("%d-%m-%Y") +  '.log'
        return log_name
        
    def start_logging(self):
        """ Запускает логирование приложения. """
        import logging

        logging.basicConfig(
            filename=self.get_logs_filename(),
            level=logging.INFO,
            format=self.log_format)
