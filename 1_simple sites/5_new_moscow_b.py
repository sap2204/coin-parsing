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

        # Описание монеты
        description = coin.findAll('div', class_ = 'col')[1].find('p').text.replace(' ', '').replace(',', '.').replace('-', '')
        #print('Полное описание ----',description)
        # Получаем из описания только список цифр
        only_numb = re.findall(r'\d+', description)
        #logger.info('Получен список цифрового описания монеты')
        if only_numb[0] == '1': # Удалил лишний нулевой элемент  в монете 'Веселая карусель'
            del only_numb[0]
        #print(only_numb)

        # Для определения номинала и веса из списка цифр ищем числа из 1 и 2-х цифр (х и хх)
        # Создаем список для одно и двузначных чисел, чтобы из него забрать номинал и вес
        nom_weight_list = []
        number_3_list = [] # список для хранения пробы металла
        for i in only_numb:
            number1_2 = ((re.search(r'\b\d{1,2}\b', i))) # поиск 1 и 2-значных чисел

            # поиск 3-значных чисел для пробы металла
            number_3 = (re.search(r'\b\d{3}\b', i)) 
            if number_3:
                number_3 = (re.search(r'\b\d{3}\b', i)).group(0) + '-'
                #print('Проба ', number_3 )

                 # Металл монеты
                coin_me = re.search(me_pattern, description).group(0) + ' ' + number_3
                print(coin_me)
                
            if number1_2: # Если регулярное выражение нашло совпадение по шаблону
                nom_weight_list.append(number1_2.group(0))
        #print(nom_weight_list)
        #logger.info('Получен список, из которого берем номинал и вес монеты')

        # Масса монеты
        weight_coin = '{0}.{1}'.format(nom_weight_list[1], nom_weight_list[2])
        #logger.info('Полученна МАССА монеты {0} '.format(coin_name))

        # Металл монеты
        
        
        
        


        
        