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
logger.add("logs\logs.txt", format = "{time} {level} {message}",
level = 'INFO', rotation = '10 MB', compression = 'zip')

# Создание рандомного юзер-агента
user = UserAgent().random
header = {'user-agent': user}

# Исходные данные по банку
bank_name = 'ГТ банк'
url = 'https://gaztransbank.ru/chastnym-litsam/monety/'

# Отправка запроса к странице сайта
responce = requests.get(url, headers = header)
logger.info('Получен ответ от сайта {0} {1}'.format(bank_name, url))

# Проверка статуса ответа сервера и начало сбора информации
if responce.ok == True:
    # Получение страницы сайта и выделение тегов
    soup = BeautifulSoup(responce.text, 'lxml')
    
    # Название монеты
    coin_name = soup.find('div', class_ = 'monets__title').text.strip()
    logger.info('Получили название монеты')

    # Получение массы монеты
    weight = soup.find_all('div', class_ = 'monets-right__item')[4].text.strip()
    weight_coin = re.search(weight_pattern, weight).group(0).replace(',', '.')
    logger.info('Получили вес монеты')
    
    # Металл монеты
    me = soup.find_all('div', class_ = 'monets-right__item')[0].text.strip().lower()
    coin_me = re.search(me_pattern, me).group(0)  + ' ' + re.search(r'\d+', me).group(0) + '-' # добавление разделителя "-"
    logger.info('Получили металл монеты')

    # Номинал монеты
    nominal = soup.find_all('div', class_ = 'monets-right__item')[3].text.strip() # получение номинала
    coin_nominal = (re.search(nominal_pattern, nominal).group(0)) + '-' # добавление разделителя "-"
    logger.info('Получили номинал монеты')

    # Цена монеты
    price = soup.find('div', class_ = 'monets__price-int').text.strip().replace(' ', '')
    coin_price = re.search(price_pattern, price).group(0)
    logger.info('Получили цену монеты')

 
# Названия колонок таблицы с парсенными данными
data = [coin_name, [], coin_price, weight_coin, coin_me, coin_nominal ]
header = ['Монета','Ном.- Проба - Вес', 'Цена', 'Вес', 'Металл', 'Номинал' ]
logger.info('Созданы колонки с названиями {0}'.format(bank_name))


# Создание и формирование итогового вида датафрейма 
df = pd.DataFrame([data], columns = header) # когда в массиве одно значение, то надо писать в скобках
df['Ном.- Проба - Вес'] = df['Номинал']  + df['Металл'] + df['Вес'] # создание колонки с описанием монеты
df.drop(columns = ['Номинал', 'Металл', 'Вес'], inplace = True)# удаление ненужных колонок
logger.info('Создан датафрейм для {0} {1}'.format(bank_name, url))



# Занесение датафрейма в таблицу через xlsxwriter
with pd.ExcelWriter('{}.xlsx'.format(bank_name), engine = 'xlsxwriter') as writer:
    df.to_excel(writer, sheet_name = bank_name, index = False)
    
    sheet = writer.sheets[bank_name]
    sheet.set_column('A:B', 80) # установка ширины столбца "Монета"
    sheet.set_column('B:B', 30) # установка ширины столбца "Ном.- Проба - Вес"
logger.info('Запись в таблицу {0} {1}'.format(bank_name, url))

