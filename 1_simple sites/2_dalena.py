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
logger.add("logs\dalena.log", format = "{time} {level} {message}",
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
        weight = coin.findAll('div', class_ = 'bx-newslist-other')[0].text.strip().replace(' ', '').replace(',', '.')
        weight_coin = re.search(weight_pattern, weight).group(0)
        logger.info('Получен вес монеты {0} '.format(coin_name))

        # Металл монеты
        me = coin.findAll('div', class_ = 'bx-newslist-other')[1].text.strip().lower()
        coin_me = re.search(me_pattern, me).group(0)  + ' ' + re.search(r'\d+', me).group(0) + '-' # добавление разделителя "-"
        logger.info('Получен металл монеты {0} '.format(coin_name))

        # Номинал монеты
        nominal = coin.findAll('div', class_ = 'bx-newslist-other')[2].text.strip()
        coin_nominal = re.search(nominal_pattern, nominal).group(0) + '-' # добавление разделителя '-'
        logger.info('Получение номинала {0} '.format(coin_name))

        # Цена монеты
        price = coin.findAll('div', class_ = 'bx-newslist-other')[3].text.strip().replace(' ', '')
        coin_price = re.search(price_pattern, price).group(0)
        logger.info('Получение цены {0} '.format(coin_name)) 

        # Добавление элементов в список
        data.append([coin_name, '', coin_price, weight_coin, coin_me, coin_nominal])
        logger.info('Добавление параметров монеты в список')

# Создание колонок для датафрейма
titles = ['Монета','Ном.- Проба - Вес', 'Цена', 'Вес', 'Металл', 'Номинал' ]

# Создание и формирование итогового вида датафрейма
df = pd.DataFrame(data, columns = titles)
df['Ном.- Проба - Вес'] = df['Номинал']  + df['Металл'] + df['Вес'] # создание колонки с описанием монеты
df.drop(columns = ['Номинал', 'Металл', 'Вес'], inplace = True)# удаление ненужных колонок
logger.info('Создан итоговый датафрейм')

# Занесение датафрейма в таблицу через xlsxwriter

with pd.ExcelWriter('results\{}.xlsx'.format(bank_name), engine = 'xlsxwriter') as writer:
    df.to_excel(writer, sheet_name = bank_name, index = False)
    
    sheet = writer.sheets[bank_name]
    sheet.set_column('A:B', 80) # установка ширины столбца "Монета"
    sheet.set_column('B:B', 30) # установка ширины столбца "Ном.- Проба - Вес"
logger.info('Создана таблица {}.xlsx '.format(bank_name) )