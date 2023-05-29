# Импорт необходимых модулей
import requests 
from bs4 import BeautifulSoup 
from fake_useragent import UserAgent 
import pandas as pd 
import re 
import xlsxwriter 
from loguru import logger

# Паттерны регулярных выражений
weight_pattern = r'\d+[.,]\d+'
me_pattern = r'(серебро|золото)'
nominal_pattern = r'\d+'
price_pattern = r'\d+'

# Создание журнала логирования
logger.add("logs\log_dalena.txt", format = "{time} {level} {message}",
           level = 'INFO', rotation = '10 MB', compression = 'zip')

#Создание фантомного юзер агента
user = UserAgent().random
header = {'user-agent': user}
logger.info('Создан фейковый юзер-агент') 

# Исходные данные по банку
bank_name = 'Далена'
url = 'https://www.dalenabank.ru/chastnym-klientam/monety/'

# Отправка запроса к странице сайта
responce = requests.get(url, headers = header)
logger.info('Получен ответ от сайта {0} - {1} - {2}'.format(bank_name, responce, url))

# Проверка статуса ответа сервера и начало сбора информации
if responce.ok == True:
    # Получение страницы с сайта и выделение тегов
    soup = BeautifulSoup(responce.text, 'lxml')
    logger.info('Получили html-страницу сайта')

    # Создание пустого списка для записи спарсенных данных
    data = []

    # Парсинг списка всех монет
    coin_list = soup.findAll('div', class_ = 'bx-newslist-container col-sm-6 col-md-4')
    logger.info('Получен список всех монет')

    # Цикл для перебора данных монет из списка всех монет
    for coin in coin_list:
        # Название монеты
        coin_name = coin.find('h3', class_ = 'bx-newslist-title').text.strip()
        logger.info('Получено название монеты {0} '.format(coin_name))

        # Масса монеты
        weight = coin.findAll('div', class_ = 'bx-newslist-other')[0].text.strip().replace(' ', '')
        weight_coin = re.search(weight_pattern, weight).group(0)
        logger.info('Получен вес монеты {0} '.format(coin_name))

