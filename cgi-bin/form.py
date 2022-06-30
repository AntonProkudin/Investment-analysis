#!/usr/bin/env python3
import cgi
import html
import os
import requests
import investpy
import now as now
from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np
from datetime import datetime, date, time
import xlrd
import cssutils
import cgitb; cgitb.enable()

form = cgi.FieldStorage()
a = form.getfirst("TEXT_1", "не задано")
a = html.escape(a)
a = a.title()
print("Content-Type: text/html; charset=utf-8\r")
print('\r')
print("""<!DOCTYPE HTML>
<html>

<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="../css/main.css" type="text/css" charset="utf-8">
    <title>CGI</title>
</head>

   <body>

<p class="text_effect">Найдите акцию по тикеру:</p>
<br>
  <form action="/cgi-bin/form.py">
	<fieldset>
		<input type="text" name="TEXT_1">
		<button type="submit"><i class="fa fa-search"></i></button>
			<output type="text" name="OUT">
	</fieldset>
  </form>
  <br><br>
""")
# скрипт
search_result = investpy.search_quotes(text=a.title(), products=['stocks'],
                                       countries=['united states'], n_results=1)
recent_data = search_result.retrieve_recent_data()

history = []
history.append(a.title())
x = np.arange(15)
y = []
i = 0
for value in recent_data['Close'][-15:]:
    y.append(value)


plt.figure(figsize=(12, 7))
plt.plot(x, y, 'o-r', alpha=0.7, label="Изменение цены ", lw=5, mec='b', mew=2, ms=10)
plt.xlabel('Последние 15 дней')
plt.ylabel('Цена в usd')
plt.grid(True)
plt.savefig('saved_figure.png')
fn = os.path.basename("../img/saved_figure.png")
print('<p class="text_effect">График и аналитика:<br></p>')
print('<small><div id="image"><img src=\"http://localhost:8000/{}\" width="1250px" height="800px" align="top" class="round"/></div>'.format(fn))

technical_indicators = investpy.technical.technical_indicators(a.title(), "united states", 'stock', interval='daily')
tech_sell = len(technical_indicators[technical_indicators['signal'] == 'sell'])
tech_buy = len(technical_indicators[technical_indicators['signal'] == 'buy'])

moving_averages = investpy.technical.moving_averages(a.title(), "united states", 'stock', interval='daily')
moving_sma_sell = len(moving_averages[moving_averages['sma_signal'] == 'sell'])
moving_sma_buy = len(moving_averages[moving_averages['sma_signal'] == 'buy'])
moving_ema_sell = len(moving_averages[moving_averages['ema_signal'] == 'sell'])
moving_ema_buy = len(moving_averages[moving_averages['ema_signal'] == 'buy'])

sma_20 = moving_averages['sma_signal'][2]
sma_100 = moving_averages['sma_signal'][4]
ema_20 = moving_averages['ema_signal'][2]
ema_100 = moving_averages['ema_signal'][4]
print('<a><br>Индикаторы технических продаж:<br> к покупке =', tech_buy, 'из 12; ', 'к продаже =', tech_sell, 'из 12'+"<br><br>")
print('SMA скользящие средние:<br> к покупке =', moving_sma_buy, 'из 6; ', 'к продаже =', moving_sma_sell, 'из 6'+"<br><br>")
print('EMA скользящие средние:<br> к покупке =', moving_ema_buy, 'из 6; ', 'к продаже =', moving_ema_sell, 'из 6'+"<br><br>")
print('SMA_20 =', sma_20, ';', 'SMA_100 =', sma_100, ';<br>', 'EMA_20 =', ema_20, ';', 'EMA_100 =', ema_100+"<br><br>")
counter = 0
if (sma_20 == 'buy'):
    counter = counter + 1
else:
    counter = counter - 1
if (sma_100 == 'buy'):
    counter = counter + 1
else:
    counter = counter - 1
if (ema_20 == 'buy'):
    counter = counter + 1
else:
    counter = counter - 1
if (ema_100 == 'buy'):
    counter = counter + 1
else:
    counter = counter - 1

if (counter == 4):
    ret = 'Активно покупать'
if (counter == -4):
    ret = "Активно продавать"
if (counter == -3 or counter == -2):
    ret = "Продавать"
if (counter == 3 or counter == 2):
    ret = "Покупать"
if (counter == 0 or counter == 1 or counter == -1):
    ret = "Нейтрально"
print("Совет: "+ ret + "</a></small>")




# Закрываем html

print("""
</body>
        </html>""")
