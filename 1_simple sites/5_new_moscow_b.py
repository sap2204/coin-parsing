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
logger.add("logs\mosc_new_b.txt", format = "{time} {level} {message}",
           level = 'INFO', rotation = '10 MB', compression = 'zip')

# Создание фантомного юзер агента
user = UserAgent().random
header = {'user-agent': user}
logger.info('Создан фейковый юзер агент')

# Исходные данные по банку
bank_name = 'Нов. мск. банк'
url = 'https://www.nmbank.ru/uslugi/chastnym-licam/monety-iz-dragocennyh-metallov/'

# Отправка запроса к странице сайта
responce = requests.get(url, headers = header)
logger.info('Получен ответ от сайта {0} {1} {2}'.format(bank_name, responce, url))

# Проверка статуса ответа и начало сбора информации
if responce.ok == True:
    # Получение страницы сайта и выделение тегов
    soup = BeautifulSoup(responce.content, 'lxml')
    logger.info('Получили html-страницу сайта {0} '.format(bank_name))

    # Создание пустого списка для записи спарсенных данных
    data = []

    # Получение списка всех монет
    coin_list = soup.findAll('div', class_ = 'row d-flex align-center')
    logger.info('Получен список всех монет')
    

    # Цикл для перебора данных всех монет из списка 
    for coin in coin_list:
        # Название монеты
        coin_name = coin.find('strong', class_ = 'title add-color').text.strip()
        logger.info('Получено название монеты {0} '.format(coin_name))

        # Масса монеты
        weight = coin.findAll('div', class_ = 'col')[1].find('p').text.replace(',', '.')
        #coin_weight = re.search(weight_pattern, weight).group(0)
        print(weight)