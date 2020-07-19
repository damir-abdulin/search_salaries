import os

import requests
import bs4
import openpyxl

import function

import praca_function as praca

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

logging.info("Старт программы")
while True:
    print("Чтобы выйти нажмите Ctrl+C")
    vacancy = input("Введите название вакансии: ")
    logging.debug("Полученная вакансия: " + vacancy)
    praca.make_excel_file(vacancy)
