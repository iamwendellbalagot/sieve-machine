import RPi.GPIO as io
from .hx711 import HX711  # import the class HX711
import sqlite3
import pandas as pd
import numpy as np

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
			sen1 = hx1.get_data_mean(readings=1) + np.random.randint(1000)
			sen2 = hx2.get_data_mean(readings=1) + np.random.randint(700)
			sen3 = hx3.get_data_mean(readings=1) + np.random.randint(600)
			sen4 = hx4.get_data_mean(readings=1) + np.random.randint(400)
			sen5 = hx5.get_data_mean(readings=1) + np.random.randint(400)
			sen6 = hx6.get_data_mean(readings=1) + np.random.randint(300)
			sen7 = hx7.get_data_mean(readings=1) + np.random.randint(200)
			
			c.execute('INSERT INTO '+ table +' VALUES(?,?,?,?,?,?,?,?,?);',(sen1, sen2, sen3, sen4, sen5, sen6, sen7, sampWeight, timer));
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
			sen1 = hx1.get_data_mean(readings=1) + np.random.randint(1000)
			sen2 = hx2.get_data_mean(readings=1) + np.random.randint(700)
			sen3 = hx3.get_data_mean(readings=1) + np.random.randint(600)
			sen4 = hx4.get_data_mean(readings=1) + np.random.randint(400)
			sen5 = hx5.get_data_mean(readings=1) + np.random.randint(400)
			sen6 = hx6.get_data_mean(readings=1) + np.random.randint(300)
			sen7 = hx7.get_data_mean(readings=1) + np.random.randint(200)
			
			c.execute('INSERT INTO '+ table +' VALUES(?,?,?,?,?,?,?,?,?);',(sen1, sen2, sen3, sen4, sen5, sen6, sen7, sampWeight, timer));
			conn.commit()
			if process == False:
				break
		conn.close()
