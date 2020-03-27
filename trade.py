import numpy as np
import ffn as f
import pandas as pd

date_train = ['2018-12-01', '2019-01-01', '2019-02-02', '2019-03-01', '2019-04-02', '2019-05-01', '2019-06-02', '2019-07-01', '2019-08-02', '2019-09-01', '2019-10-02', '2019-11-01']
date_train_lag = ['2018-11-30', '2018-12-31', '2019-02-01', '2019-02-28', '2019-04-01', '2019-04-30', '2019-06-01', '2019-06-30', '2019-08-01', '2019-08-30', '2019-10-01', '2019-10-31']
date_trade = ['2019-01-02', '2019-02-01', '2019-03-02', '2019-04-01', '2019-05-02', '2019-06-01', '2019-07-02', '2019-08-01', '2019-09-02', '2019-10-01', '2019-11-02', '2019-12-01']
def mu(df):
    s = 0
    for i in df:
        s += i
    return s/len(df)


def Stdev(df, mean):
    n = 1/(len(df)-1)
    s = 0
    for i in df:
        x = mean - i
        s += x ** 2
    return n * s
def lsrl(m, yint, price):
    return -1 * m * price + yint

for q in range(len(date_train)-1):
	data = f.get('jpm', start=date_train[q], end=date_train[q+1])
	datalag = f.get('bac', start=date_train[q], end=date_train[q+1])
	data['dep'] = datalag
	price_data = data
	data = data.pct_change()
	p1 = data['jpm']
	price1 = []

	for i in p1:
		if str(i) != 'nan':
			price1.append(i)
	p2 = data['dep']
	price2 = []
	for j in p2:
		if str(j) != 'nan':
			price2.append(j)
	muX = mu(price1)
	muY = mu(price2)
	Sx = Stdev(price1, muX)
	Sy = Stdev(price2, muY)
	corr = np.corrcoef(price1,price2)
	corr = corr[0][1]
	m = corr * (Sy/Sx)
	yint = m * muX + muY

	data = f.get('GOOG, FB, MSFT, jpm, bac', start=date_trade[q], end=date_trade[q+1])
	price_data = data
	price_change = data.pct_change()
	pred = []
	for i in price_change['jpm']:
		pred.append(lsrl(m, yint, i))
	money = 0
	buy = lambda price: money - price
	sell = lambda price: money + price
	short = 0

	for i in range(len(pred)-1):
		if pred[i] > 0 and short == 0:
			money = buy(price_data['bac'][i])
			money = sell(price_data['bac'][i+1])
		elif pred[i] > 0 and short != 0:
			for i in range(short):
				money = buy(price_data['bac'][i])
				
			short = 0
		elif pred[i] < 0:
			money = sell(price_data['bac'][i])
			short += 1
		
			
			
		
			
	        
	print('Profits from {} to {} are {}'.format(date_trade[q], date_trade[q+1], money))



