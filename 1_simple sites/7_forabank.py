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
logger.add("logs\\forabank.log", format = "{time} {level} {message}",
           level = 'INFO', rotation = '10 MB', compression = 'zip')

#Создание фантомного юзер агента
user = UserAgent().random
header = {'user-agent': user}
logger.info('Создан фейковый юзер-агент') 

# Исходные данные по банку
bank_name = 'Форабанк'
url = 'https://www.forabank.ru/landings/coins/'

# Отправка запроса к странице сайта
responce = requests.get(url, headers = header)
logger.info('Получен ответ от сайта {0} - {1} - {2}'.format(bank_name, responce, url))

# Проверка статуса ответа сервера и начало сбора информации
if responce.ok == True:
    # Получение страницы с сайта и выделение тегов
    soup = BeautifulSoup(responce.content, 'lxml')
    logger.info('Получили html-страницу сайта')
    
    # Создание пустого списка для записи спарсенных данных
    data = []

    # Парсинг списка всех монет из раздела "Памятные монеты" (дальше буду парсить отдельно левую и правые части)
    coin_list = soup.findAll('div', class_ = 'coins-wrapper coins-wrapper--grid')
    logger.info('Получен список всех монет')

    # Цикл для перебора данных монет ЛЕВОЙ части из списка всех монет
    for coin_left in coin_list:
        # Название монеты
        coin_name = coin_left.find('div', class_ = 'coin-title order-3').text.strip()
        logger.info('Получено название монеты {0} '.format(coin_name))

        # Масса монеты
        weight = coin_left.find('div', class_ = 'coin-chars coin-chars--flex order-4').find('div', class_ = 'right-char').findAll('strong')[0].text.strip()
        weight_coin = re.search(weight_pattern, weight).group(0)
        logger.info('Получен ВЕС монеты {0} '.format(coin_name))

        # Металл монеты
        met = coin_left.find('div', class_ = 'coin-chars coin-chars--flex order-4').find('div', class_ = 'left-char').findAll('strong')[0].text.strip().lower()
        proba = coin_left.find('div', class_ = 'coin-chars coin-chars--flex order-4').find('div', class_ = 'left-char').findAll('strong')[1].text.strip()
        coin_me = met + ' ' + proba + '-'# соединил металл и пробу, добавил разделитель '-'
        logger.info('Получен металл монеты {0} '.format(coin_name))

        # Номинал монеты
        nominal = coin_left.find('div', class_ = 'coin-chars coin-chars--flex order-4').find('div', class_ = 'left-char').findAll('strong')[-1].text.strip()
        coin_nominal = re.search(nominal_pattern, nominal).group(0) + '-'
        logger.info('Получен НОМИНАЛ монеты {0} '.format(coin_name))

        # Цена монеты
        price = coin_left.find('div', class_ = 'coin-chars coin-chars--flex order-4').find('div', class_ = 'right-char').findAll('strong')[-1].text.strip().replace(' ', '')
        coin_price = int(re.search(price_pattern, price).group(0))
        logger.info('Получена цена монеты {0} '.format(coin_name))

        # Добавление элементов в список
        data.append([coin_name, '', coin_price, weight_coin, coin_me, coin_nominal])
        logger.info('Добавление параметров монеты в список')

        # Разделитель
        logger.info('===================================================')

    # Цикл для перебора данных монет ПРАВОЙ части из списка всех монет
    for coin_right in coin_list:
        # Название монеты
        coin_name = coin_right.find('div', class_ = 'coin-title order-7').text.strip()
        logger.info('Получено название монеты {0} '.format(coin_name))

        # Масса монеты
        weight = coin_right.find('div', class_ = 'coin-chars coin-chars--flex order-8').find('div', class_ = 'right-char').findAll('strong')[0].text.strip()
        weight_coin = re.search(weight_pattern, weight).group(0)
        logger.info('Получен ВЕС монеты {0} '.format(coin_name))

        # Металл монеты
        met = coin_right.find('div', class_ = 'coin-chars coin-chars--flex order-8').find('div', class_ = 'left-char').findAll('strong')[0].text.strip().lower()
        proba = coin_right.find('div', class_ = 'coin-chars coin-chars--flex order-8').find('div', class_ = 'left-char').findAll('strong')[1].text.strip()
        coin_me = met + ' ' + proba + '-'# соединил металл и пробу, добавил разделитель '-'
        logger.info('Получен металл монеты {0} '.format(coin_name))

        # Номинал монеты
        nominal = coin_right.find('div', class_ = 'coin-chars coin-chars--flex order-8').find('div', class_ = 'left-char').findAll('strong')[-1].text.strip()
        coin_nominal = re.search(nominal_pattern, nominal).group(0) + '-'
        logger.info('Получен НОМИНАЛ монеты {0} '.format(coin_name))

        # Цена монеты
        price = coin_right.find('div', class_ = 'coin-chars coin-chars--flex order-8').find('div', class_ = 'right-char').findAll('strong')[-1].text.strip().replace(' ', '')
        coin_price = int(re.search(price_pattern, price).group(0))
        coin_price = int(re.search(price_pattern, price).group(0))
        logger.info('Получена цена монеты {0} '.format(coin_name))

        # Добавление элементов в список
        data.append([coin_name, '', coin_price, weight_coin, coin_me, coin_nominal])
        logger.info('Добавление параметров монеты в список')

        # Разделитель
        logger.info('===================================================')

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
logger.info('Создана таблица {}.xlsx '.format(bank_name))