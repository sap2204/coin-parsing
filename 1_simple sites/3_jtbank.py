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
    soup = BeautifulSoup(responce.content, 'lxml')
    logger.info('Получена страница сайта')
    
    # Создание пустого списка для записи спарсенных данных
    data = []

    # Парсинг списка инвестиционных монет
    coin_list_invest = soup.findAll('div', class_ = 'coin-list')[0]
    coin_list_invest = coin_list_invest.findAll('div', class_ = 'item')
    logger.info('Получен список инвестиционных монет')
    
    # Цикл для перебора инвестиционных монет монет из полученного списка
    for coin in coin_list_invest:
        # Название монеты
        coin_name = coin.find('span', class_ = 'name').text.strip()
        logger.info('Получено название инвест. монеты {0} '.format(coin_name))
        
        # Масса монеты
        weight = coin.find('div', class_ = 'weight').text.strip().replace(' ', '')
        weight_coin = re.search(weight_pattern, weight).group(0)
        logger.info('Получен вес инвест. монеты {0} '.format(coin_name))

        #  Металл монеты
        me = coin.findAll('li')[0].text.strip().lower()
        coin_me = re.search(me_pattern, me).group(0)  + ' ' + re.search(r'\d+', me).group(0) + '-' # добавление разделителя "-"
        logger.info('Получен МЕТАЛЛ инвест. монеты {0} '.format(coin_name))
        
        # Номинал монеты
        nominal = coin.findAll('li')[4].text.strip()
        coin_nominal = re.search(nominal_pattern, nominal).group(0) + '-' # добавление разделителя '-'
        logger.info('Получен номинал инвест. монеты {0} '.format(coin_name))

        # Цена монеты
        price = coin.find('div', class_ = 'selling-price').text.strip().replace(' ', '')
        coin_price = int(re.search(price_pattern, price).group(0))
        logger.info('Получена ЦЕНА монеты {0} '.format(coin_name))

         # Добавление элементов в список
        data.append([coin_name, '', coin_price, weight_coin, coin_me, coin_nominal])
        logger.info('Добавление параметров инвест. монет в список')

    # Парсинг списка памятных монет
    coin_list_memory = soup.findAll('div', class_ = 'coin-list')[1]
    coin_list_memory = coin_list_memory.findAll('div', class_ = 'item')
    logger.info('ПОЛУЧЕН СПИСОК ПАМЯТНЫХ МОНЕТ')

    # Цикл для перебора памятных монет монет из полученного списка
    for coin in coin_list_memory:
        # Название монеты
        coin_name = coin.find('span', class_ = 'name').text.strip()
        logger.info('Получено название памятной монеты {0} '.format(coin_name))

        # Масса монеты 
        weight = coin.find('div', class_ = 'weight').text.strip()
        weight_coin = re.search(weight_pattern, weight).group(0)
        logger.info('Получена МАССА памятной монеты {0} '.format(coin_name))

        # Металл монет (на сайте в этой категории не указан)
        coin_me = '-'
        logger.info('Металл памятной монеты не указан {0} '.format(coin_name))

        # Номинал монеты
        nominal = coin.findAll('li')[2].text.strip().replace(' ', '')
        coin_nominal = re.search(nominal_pattern, nominal).group(0)+ '-' # добавление разделителя '-'
        logger.info('Получен НОМИНАЛ памятной монеты {0} '.format(coin_name))

        # Цена монеты
        price = coin.find('div', class_ = 'selling-price').text.strip().replace(' ', '')
        coin_price = int(re.search(price_pattern, price).group(0))
        logger.info('Получена цена памятной монеты {0} '.format(coin_name))

        # Добавление элементов в список
        data.append([coin_name, '', coin_price, weight_coin, coin_me, coin_nominal])
        logger.info('Добавление параметров инвест. монет в список')

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

    


    