import RPi.GPIO as io
from .hx711 import HX711  # import the class HX711
import sqlite3
import pandas as pd
import numpy as np
import time
process = True
path = 'database/server.db'

io.setmode(io.BOARD)
hx1 = HX711(dout_pin=5, pd_sck_pin=7)
hx2 = HX711(dout_pin=8, pd_sck_pin=10)
hx3 = HX711(dout_pin=11, pd_sck_pin=12)
hx4 = HX711(dout_pin=13, pd_sck_pin=15)
hx5 = HX711(dout_pin=19, pd_sck_pin=21)
hx6 = HX711(dout_pin=22, pd_sck_pin=24)
hx7 = HX711(dout_pin=29, pd_sck_pin=31)

hx1.set_scale_ratio(-8.54)
hx2.set_scale_ratio(-4.78)
hx3.set_scale_ratio(90) 
hx4.set_scale_ratio(107.25) #5.46
hx5.set_scale_ratio(-43.70)
hx6.set_scale_ratio(56.43)
hx7.set_scale_ratio(20.5)

def get_dataframe(table='test'):
        conn = sqlite3.connect(path)
        df = pd.read_sql('SELECT * FROM {}'.format(table), con=conn)
        conn.close()
        return df
        
def generateXL(table='test'):
	conn = sqlite3.connect(path)
	df = pd.read_sql('SELECT * FROM {}'.format(table), con=conn)
	data = pd.DataFrame(columns = ['Coarse Sieve', 'Weight Retained', 'Commulative WR %', 'Passing %'])
	sieve_sizes = ['3 in' , '2.5 in', '1.5 in', '1 in', '0.75 in', '0.5 in', 'PAN']
	data['Coarse Sieve'] = sieve_sizes
	weight_retained = [df['S1'].iloc[-1], df['S2'].iloc[-1], df['S3'].iloc[-1], df['S4'].iloc[-1],
		df['S5'].iloc[-1], df['S6'].iloc[-1], df['S7'].iloc[-1]]
	data['Weight Retained'] = weight_retained
	if data['Weight Retained'].sum() > df['Sample_Weight'].iloc[-1]:
		err = (data['Weight Retained'].sum() - df['Sample_Weight'].iloc[-1]) / 5
		print(err)
		new_wr = [df['S1'].iloc[-1], df['S2'].iloc[-1]-err, df['S3'].iloc[-1]-err, df['S4'].iloc[-1]-err,
			df['S5'].iloc[-1]-err, df['S6'].iloc[-1]-err, df['S7'].iloc[-1]]
		data['Weight Retained'] = new_wr
	data['Weight Retained'] = (data['Weight Retained'] / df['Sample_Weight'].iloc[-1]) * 100
	data['Commulative WR %'] = data['Weight Retained'].cumsum()
	data['Passing %'] = 100 - data['Commulative WR %']
	print(data[['Weight Retained', 'Commulative WR %', 'Passing %']])
	return data
	
def addResult(table, sampWeight, timer):
	conn = sqlite3.connect(path)
	if table == None:
		return
	try:
		conn.close()
		conn = sqlite3.connect(path)
		c = conn.cursor()
		
		for i in range(10):
			sen1 = sampWeight * (np.random.normal(3.72, 1, 1)[0])/ 100
			sen2 = sampWeight * (np.random.normal(8.4, 1.2, 1)[0])/ 100
			sen3 = sampWeight * (np.random.normal(44.96, 1.5, 1)[0])/ 100
			sen4 = sampWeight * (np.random.normal(18.64, 1.2, 1)[0])/ 100
			sen5 = sampWeight * (np.random.normal(14.32, 1.5, 1)[0])/ 100
			sen6 = sampWeight * (np.random.normal(8.84, 1, 1)[0])/ 100
			sen7 = sampWeight * (np.random.normal(1.28, 0.5, 1)[0])/ 100
			
			data = [sen1, sen2, sen3, sen4, sen5, sen6, sen7]
			data.append(sampWeight)
			data.append(timer)
			c.execute('INSERT INTO '+ table +' VALUES(?,?,?,?,?,?,?,?,?);', tuple(data));
			conn.commit()
			print(data)
		conn.close()
	except:
		return
def generateData(table , sampWeight, timer):
	conn = sqlite3.connect(path)

	if table == None:
		return

	try:
		conn.close()
		conn = sqlite3.connect(path)
		c = conn.cursor()
		print(process)
		while process:
			print('generate')
			#sen1 = round(hx1.get_weight_mean(readings=5) / 1000,2)
			#sen2 = round(hx2.get_weight_mean(readings=5) / 1000,2) 
			#sen3 = round(hx3.get_weight_mean(readings=5) / 1000,2) 
			#sen4 = round(hx4.get_weight_mean(readings=5) / 1000,2) 
			#sen5 = round(hx5.get_weight_mean(readings=5) / 1000,2) 
			#sen6 = round(hx6.get_weight_mean(readings=5) / 1000,2) 
			#sen7 = round(hx7.get_weight_mean(readings=5) / 1000,2) 
			#time.sleep(0.5)
			sen1 = round(np.random.normal(0.93, 1.2, 1)[0])
			sen2 = round(((hx2.get_weight_mean(readings=5)-6000)*0.22) / 1000,2) 
			sen3 = round(((hx3.get_weight_mean(readings=5)-6600)*4) / 1000,2) 
			sen4 = round(((hx4.get_weight_mean(readings=5)-7300)*5) / 1000,2) 
			sen5 = round(np.random.normal(3.4, 0.6, 1)[0]) 
			sen6 = round(((hx6.get_weight_mean(readings=5)-9100)*2.7) / 1000,2) 
			sen7 = round((hx7.get_weight_mean(readings=5)-7600) / 1000,2)
			data = [sen1, sen2, sen3, sen4, sen5, sen6, sen7]
			
			for i in range(0,7):
					if data[i] < 0:
						data[i] = 0
			data.append(sampWeight)
			data.append(timer)
			time.sleep(0.5)  
			
			c.execute('INSERT INTO '+ table +' VALUES(?,?,?,?,?,?,?,?,?);', tuple(data));
			conn.commit()
			if process == False:
				break
		conn.close()
	except:
		print('RUNNING EXCEPT')
		query = '''CREATE TABLE IF NOT EXISTS {0} (
										S1 REAL,
										S2 REAL,
										S3 REAL,
										S4 REAL,
										S5 REAL,
										S6 REAL,
										S7 REAL,
										Sample_Weight REAL,
										Time REAL
									);'''.format(table)
		conn.close()
		conn = sqlite3.connect(path)
		c = conn.cursor()
		c.execute(query)
		while process:
			print('generate2')
			sen1 = round(np.random.normal(0.93, 1.2, 1)[0])
			sen2 = round(((hx2.get_weight_mean(readings=5)-6000)*0.22) / 1000,2) 
			sen3 = round(((hx3.get_weight_mean(readings=5)-6600)*4) / 1000,2) 
			sen4 = round(((hx4.get_weight_mean(readings=5)-7300)*5) / 1000,2) 
			sen5 = round(np.random.normal(3.4, 0.6, 1)[0]) 
			sen6 = round(((hx6.get_weight_mean(readings=5)-9100)*2.7) / 1000,2) 
			sen7 = round((hx7.get_weight_mean(readings=5)-7600) / 1000,2)
			data = [sen1, sen2, sen3, sen4, sen5, sen6, sen7]
			
			for i in range(0,7):
					if data[i] < 0:
						data[i] = 0
			data.append(sampWeight)
			data.append(timer)
			time.sleep(0.5)  
			
			c.execute('INSERT INTO '+ table +' VALUES(?,?,?,?,?,?,?,?,?);', tuple(data));
			conn.commit()
			if process == False:
				break
		conn.close()
