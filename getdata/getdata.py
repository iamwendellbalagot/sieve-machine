import RPi.GPIO as io
from .hx711 import HX711  # import the class HX711
import sqlite3
import pandas as pd
import numpy as np

process = True
path = 'database/server.db'

io.setmode(io.BOARD)
hx1 = HX711(dout_pin=11, pd_sck_pin=13)
hx2 = HX711(dout_pin=29, pd_sck_pin=31)

def generateData(table='test'):
	conn = sqlite3.connect(path)
	
	
	try:
		conn.close()
		conn = sqlite3.connect(path)
		c = conn.cursor()
		print(process)
		while process:
			print('generate')
			sen1 = hx1.get_data_mean(readings=2)
			sen2 = hx2.get_data_mean(readings=2)
			
			c.execute('INSERT INTO '+ table +' VALUES(?,?);',(sen1, sen2));
			conn.commit()
			if process == False:
				break
		conn.close()
	except:
		print('RUNNING EXCEPT')
		query = '''CREATE TABLE IF NOT EXISTS {0} (
                                        S1 REAL,
                                        S2 REAL
									);'''.format(table)
		con.close()
		c = conn.cursor()
		c.execute(query)
		while process:
			print('generate2')
			sen1 = hx1.get_data_mean(readings=2)
			sen2 = hx2.get_data_mean(readings=2)
			
			c.execute('INSERT INTO '+ table +' VALUES(?,?);',(sen1, sen2));
			conn.commit()
			if process == False:
				break
		conn.close()
