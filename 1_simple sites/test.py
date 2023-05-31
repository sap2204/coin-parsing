# Проверка сайтов как сайт отдает страницы

# Импорт необходимых модулей
import requests 
from bs4 import BeautifulSoup 
from fake_useragent import UserAgent 
import pandas as pd 
import re 
import xlsxwriter 
from loguru import logger 


# Создание фантомного юзер агента
user = UserAgent().random
header = {'user-agent': user}


# Сайт банка
url = 'https://www.invb.ru/person/prodazha-monet/'

# Отправка запроса к странице сайта
responce = requests.get(url, headers = header)

# Проверка статуса ответа и начало сбора информации
if responce.ok == True:
    # Получение страницы сайта и выделение тегов
    soup = BeautifulSoup(responce.content, 'lxml')
    print(soup)

    
    