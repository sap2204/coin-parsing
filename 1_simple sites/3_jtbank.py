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
logger.add("logs\jtbank.log", format = "{time} {level} {message}",
           level = 'INFO', rotation = '10MB', compression = 'zip')

# Создание фантомного юзер-агента
user = UserAgent().random
header = {'user-agent': user}
logger.info('Создан фейковый юзер агент')

# Исходные данные по банку
bank_name = 'J&T банк'
url = 'https://jtbank.ru/fizicheskim-litsam/monety/'

# Отправка запроса к странице сайта
responce = requests.get(url, headers = header)
logger.info('Получен ответ от сайта {0} - {1} - {2} '.format(bank_name, responce, url))

# Проверка статуса ответа сервера и начало сбора информации
if responce.ok == True:
    # Получение страницы с сайта и выделение тегов
    soup = BeautifulSoup(responce.text, 'lxml')
    logger.info('Получена страница сайта')
    
    # Создание пустого списка для записи спарсенных данных
    data = []

    # Парсинг списка всех монет
    coin_list = soup.findAll('div', class_ = 'info')
    logger.info('Получен список всех монет')
    
    # Цикл для перебора всех монет из полученного списка
    for coin in coin_list:
        # Название монеты
        coin_name = coin.find('span', class_ = 'name').text.strip()
        logger.info('Получено название монеты {0} '.format(coin_name))

        # Масса монеты
        weight = coin.find('div', class_ = 'weight').text.strip().replace(' ', '')
        weight_coin = re.search(weight_pattern, weight).group(0)
        logger.info('Масса монеты {0} '.format(coin_name))

        # Металл монеты
        me = coin.findAll('li')[0].text.strip().lower()
        #coin_me = re.search(me_pattern, me).group(0)  + ' ' + re.search(r'\d+', me).group(0) + '-' # добавление разделителя "-"
        logger.info('Металл монеты {0} '.format(me))