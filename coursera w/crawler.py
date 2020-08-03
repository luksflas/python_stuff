import requests
from bs4 import BeautifulSoup
import time
import base64
import os
# from threading import Thread
import threading
from queue import Queue
import mysql.connector
import csv
from datetime import datetime
from forex_python.converter import CurrencyRates
from decimal import *
# import urllib.request
import re
import math
import logging


# create logger with 'spam_application'
logger = logging.getLogger('spam_application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('progress.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

# logger.info('creating an instance of auxiliary_module.Auxiliary')
# a = auxiliary_module.Auxiliary()
# logger.info('created an instance of auxiliary_module.Auxiliary')
# logger.info('calling auxiliary_module.Auxiliary.do_something')
# a.do_something()
# logger.info('finished auxiliary_module.Auxiliary.do_something')
# logger.info('calling auxiliary_module.some_function()')
# auxiliary_module.some_function()
# logger.info('done with auxiliary_module.some_function()')

# logging.basicConfig(level=logging.INFO, file='progress.log')
logger.info('START')
proxies = { 'http': 'http://hypegen:ufp7jq91b7v0@142.93.49.29:40045/','https': 'https://hypegen:ufp7jq91b7v0@142.93.49.29:40045/'}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
headers_amazon = {
    'Host': 'www.amazon.de',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'TE': 'Trailers'
}
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

# db = mysql.connector.connect(host='localhost',database='db93gvmn5zhq46',user='u3vy5wws76cts', password='iy3ubg6e@%*b')
# cursor = db.cursor()

def scrape(input):
    try:
        url = product_id = shop_id = shop_currency = company = product_name = real_price = final_price = sales_price = stock = date_time = date = reevaluated_price = ''
        check_column = 0
        # checking the param if the first column is company column.
        if input[0].isnumeric() != True:
            check_column = 1
        for index, param in enumerate(input):

            if index == 0 + check_column:
                product_id = param
            elif index == 1 + check_column:
                shop_id = param
            elif index == 2 + check_column:
                shop_currency = param
            elif index == 3 + check_column:
                url = param
                if url.find('https://www.amazon') > -1:
                    page_content = requests.get(param,headers=headers_amazon)
                    page = BeautifulSoup(page_content.content, 'html.parser')
                else:
                    try:
                        page_content = requests.get(param,headers=headers,timeout=10)
                    except Exception as e:
                        logger.info(' - Over time out - ')
                        logger.info(e)
                        print(e)
                        return None
                    page = BeautifulSoup(page_content.content, 'html.parser')
            elif index == 4 + check_column:
                product_name = option(param, page).strip()
            elif index == 5 + check_column and param != '':
                # get real_price and reevaluated_price
                price_currency = option(param, page)
                if shop_currency != 'CHF':
                    price_currency = price_currency.replace('.', '')
                else:
                    price_currency = price_currency.replace(',', '')
                if url.find('fourtwenty') > -1:
                    price_currency = ''
                if price_currency.find('<') > -1:
                    if price_currency.split('>', 2)[2] != '':
                        real_price = price_currency.split('>', 2)[2].replace('&nbsp;', '').replace(',', '.').replace('<br>Nur', '').replace('EUR', '').replace(' ', '').replace('€', '')
                    else:
                        real_price = price_currency.split('</', 3)[0].split('>', 2)[1].replace('&nbsp;', '').replace(',', '.').replace('<br>Nur', '').replace('EUR', '').replace(' ', '').replace('€', '')
                else:
                    if price_currency.find('Nur') > -1 or price_currency.find('Ehem') > -1:
                        real_price = price_currency.replace('Ehem', '').replace('Nur', '').replace('.', '').replace('EUR', '').strip().split(' ', 1)[1].replace(',', '.').strip()
                    else:
                        # real_price = price_currency.split(' ', 1)[0].replace(',', '.').replace('&nbsp;', '').replace('EUR','').replace('€', '')
                        real_prices = re.findall('([0-9]+[, .]+[0-9]+)', price_currency)
                        if len(real_prices) > 0:
                            real_price = real_prices[0].replace(',', '.').replace(' ', '').strip()
                        else:
                            real_prices = re.findall('([0-9]+[, .]+)', price_currency)
                            try:
                                real_price = real_prices[0].replace(',', '')
                            except:
                                real_price = ''
            elif index == 6 + check_column and param != '':
                # get sales price
                try:
                    sales_price = option(param, page)
                    sales_price = sales_price.replace('.', '')
                    sales_price = re.findall('([0-9]+[, .]+[0-9]+)', sales_price)
                    if len(sales_price) > 0:
                        sales_price = sales_price[0].replace(',', '.').replace(' ', '').strip()
                    else:
                        sales_price = ''
                    if reevaluated_price == '':
                        reevaluated_price = str(round(CurrencyRates().convert(shop_currency, 'EUR', Decimal(sales_price)), 2))
                except Exception as e:
                    pass
            elif index == 7 + check_column and param != '':
                # get stock
                stock = option(param, page).replace(',', '').replace(' ', '')
                if stock.find('<') > -1:
                    stock = stock.split('</', 1)[0].split('>', 3)[-1].strip()
            else:
                if check_column == 0:
                    if index == 8 and param != '':
                        company = param
                elif check_column == 1:
                    if index == 0 and param != '':
                        company = param
            if real_price.count('.') > 1:
                real_price = real_price.split(' ', 1)[1]
            if sales_price.count('.') > 1:
                sales_price = sales_price.split(' ', 1)[1]
            if sales_price == '' or real_price == '':
                if sales_price == '':
                    final_price = real_price
                elif real_price == '':
                    final_price = sales_price
            else:
                if real_price <= sales_price:
                    final_price = real_price
                else:
                    final_price = sales_price
            if product_name == '':
                real_price = ''
                sales_price = ''
                final_price = ''
            if shop_currency == 'EUR':
                reevaluated_price = final_price
            else:
                try:
                    reevaluated_price = str(round(CurrencyRates().convert(shop_currency, 'EUR', Decimal(final_price)), 2))
                except Exception as e:
                    pass
        now = datetime.now()
        date_time = datetime.timestamp(now)
        # date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        date = now.strftime('%m/%d/%Y')
        print('==============================')
        print(url, product_id, shop_id, shop_currency, company, product_name, real_price, final_price, sales_price, stock, date_time, date, reevaluated_price)

        # execute insert query
        arg = (url, product_id, shop_id, company, product_name, shop_currency, real_price, final_price, sales_price, stock, date_time, date, reevaluated_price)


        return arg
    except Exception as e:
        logger.info(' - Something Went Wrong! - ')
        logger.info(e)
        logger.info(' - ERROR - ')


def option(string, page):
    lists = list(string.split(', '))
    for option in lists:
        try:
            return page.select(option)[0].get_text().strip()
        except Exception as e:
            continue
    else:
        return ''


db = mysql.connector.connect(host='localhost',database='db93gvmn5zhq46',user='u3vy5wws76cts', password='iy3ubg6e@%*b')
cursor = db.cursor()
now = datetime.now()
criteria = datetime.timestamp(now) - 1209600
cursor.execute(f'DELETE FROM crawler WHERE date_time < {criteria}')
db.commit()
cursor.close()
db.close()
# rows=[]
queries = []
count = 0
with open('Crawler_Export.csv') as input_file:
    input_reader = csv.reader(input_file, delimiter=',')
    line_count = 0
    threads = list()
    for row in input_reader:
        if line_count != 0:
            if line_count % 10 == 0:
                try:
                    minVal = math.ceil(line_count / 10) - 1
                    logger.info("here")
                    db = mysql.connector.connect(host='localhost',database='db93gvmn5zhq46',user='u3vy5wws76cts', password='iy3ubg6e@%*b')
                    cursor = db.cursor()
                    query = "INSERT INTO crawler (url, product_id, shop_id, company, product_name, shop_currency, price, final_price, sales_price, stock, date_time, date, eur_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    cursor.executemany(query, queries[minVal * 10:(minVal + 1)* 10])
                    db.commit()
                    cursor.close()
                    db.close()
                except Exception as e:
                    logger.info(e)
            queries.append(scrape(row))
            logger.info(row[3])
            logger.info(f' - succefully scraped : {line_count} line - ')
            print(f' - succefully scraped : {line_count} line - ')
            # rows.append(row)
            line_count += 1
        else:
            line_count += 1
        count = count + 1
        if  count == 400:
        print('Start : %s' % time.ctime())
        time.sleep(1800)
        print('End : %s' % time.ctime())




try:
    db = mysql.connector.connect(host='localhost',database='db93gvmn5zhq46',user='u3vy5wws76cts', password='iy3ubg6e@%*b')
    cursor = db.cursor()
    query = "INSERT INTO crawler (url, product_id, shop_id, company, product_name, shop_currency, price, final_price, sales_price, stock, date_time, date, eur_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    if len(queries) % 10 != 0:
        minVal = math.floor(len(queries) / 10)
        cursor.executemany(query, queries[minVal * 10 :(minVal + 1)* 10])
        db.commit()
    cursor.close()
    db.close()
except Exception as e:
    logger.info(' - sql error - ')
    logger.info(e)

# scrape_numbers = math.ceil(len(rows) / 300)
# for i in range(scrape_numbers):
#     thread = threading.Thread(target=scrape_loop, args=(rows[i * 300:(i + 1) * 300],))
#     thread.start()
logger.info('END')
