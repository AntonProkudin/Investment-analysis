import investpy
import now as now
from matplotlib import pyplot as plt
from datetime import datetime
import numpy as np

search_result = investpy.search_quotes(text='pfe', products=['stocks'],
                                       countries=['united states'], n_results=1)
recent_data = search_result.retrieve_recent_data()

x = np.arange(15)
y = []
i = 0
for value in recent_data['Close'][-15:]:
    y.append(value)


plt.figure(figsize=(12, 7))
plt.plot(x, y, 'o-r', alpha=0.7, label="Изменение цены ", lw=5, mec='b', mew=2, ms=10)
plt.xlabel('Последние 15 дней')
plt.ylabel('Цена на момент закрытия дня')
plt.grid(True)
plt.savefig('saved_figure.png')

technical_indicators = investpy.technical.technical_indicators("pfe", "united states", 'stock', interval='daily')

tech_sell = len(technical_indicators[technical_indicators['signal'] == 'sell'])
tech_buy = len(technical_indicators[technical_indicators['signal'] == 'buy'])

moving_averages = investpy.technical.moving_averages("pfe", "united states", 'stock', interval='daily')
moving_sma_sell = len(moving_averages[moving_averages['sma_signal'] == 'sell'])
moving_sma_buy = len(moving_averages[moving_averages['sma_signal'] == 'buy'])

moving_ema_sell = len(moving_averages[moving_averages['ema_signal'] == 'sell'])
moving_ema_buy = len(moving_averages[moving_averages['ema_signal'] == 'buy'])
sma_20 = moving_averages['sma_signal'][2]
sma_100 = moving_averages['sma_signal'][4]
ema_20 = moving_averages['ema_signal'][2]
ema_100 = moving_averages['ema_signal'][4]
print('Индикаторы технических продаж: к покупке =', tech_buy, 'из 12; ', 'к продаже =', tech_sell, 'из 12')
print('SMA скользящие средние: к покупке =', moving_sma_buy, 'из 6; ', 'к продаже =', moving_sma_sell, 'из 6')
print('EMA скользящие средние: к покупке =', moving_ema_buy, 'из 6; ', 'к продаже =', moving_ema_sell, 'из 6')
print('SMA_20 =', sma_20, ';', 'SMA_100 =', sma_100, ';', 'EMA_20 =', ema_20, ';', 'EMA_100 =', ema_100)

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
print(ret)