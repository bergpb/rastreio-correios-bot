# -*- coding: utf-8 -*-

import os
import re
import json
import time
import random
import telepot
import datetime
import cfscrape
from bs4 import BeautifulSoup
from telepot.loop import MessageLoop
from urllib.request import urlopen, Request

def getLastState(codigo):
    data = []
    row_num = 0
    scraper = cfscrape.create_scraper()
    url = 'http://www.websro.com.br/correios.php?P_COD_UNI='+codigo
    html_doc = scraper.get(url).content
    soup = BeautifulSoup(html_doc, "html.parser")
    for tr in soup.find_all('tr'):
        if row_num > 0:
            cidade = tr.find("label")
            status = tr.find("strong")
            reg_data = re.search("\d{2}\:\d{2}", tr.text).group(0)
            reg_hora = re.search("\d{2}\/\d{2}\/\d{4}", tr.text.strip()).group(0)
            data.append({
                         'status': status.text.strip(),
                         'data': reg_data,
                         'hora': reg_hora,
                         'cidade': cidade.text.strip()
                        })
        row_num = row_num + 1
        
    return json.dumps(data, indent=4, sort_keys=True)

def getAllState(codigo):
    data = []
    row_num = 0
    scraper = cfscrape.create_scraper()
    url = 'http://www.websro.com.br/detalhes.php?P_COD_UNI='+codigo
    print(url)
    html_doc = scraper.get(url).content
    soup = BeautifulSoup(html_doc, "html.parser")
    row_num = 0
    for tr in soup.find_all('tr'):
        if row_num > 0:
            cidade = tr.find("label")
            status = tr.find("strong")
            reg_data = re.search("\d{2}\:\d{2}", tr.text.strip()).group(0)
            reg_hora = re.search("\d{2}\/\d{2}\/\d{4}", tr.text.strip()).group(0)
            data.append({
                         'status': status.text.strip(),
                         'data': reg_data,
                         'hora': reg_hora,
                         'cidade': cidade.text.strip()
                        })
        row_num = row_num + 1
        
    return json.dumps(data, indent=4, sort_keys=True)

def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    if command == '/start':
        bot.sendMessage(chat_id, random.randint(1,6))

    elif len(msg['text']) == 13:
        codigo = msg['text']
        getLastState(codigo)
        print(codigo)

bot = telepot.Bot(yourtoken)

MessageLoop(bot, handle).run_as_thread()
print ('I am listening ...')

while 1:
    time.sleep(10)

    

    
