import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

import sys
sys.path.insert(1, '/path/to/applicaiton/getdata')
import getdata.getdata as getdata

def get_scatter(df=None):

	# if df is None:
	# 	# x = [0, 50, 100, 200, 300, 400, 500, 600]
	# 	# y = [0, 1.5, 2, 4, 7.5, 12.5, 20, 40.6]
	# 	# y1 = [0, 1.7, 3, 5, 8.5, 15.5, 24, 42.6]

	# 	d1 = np.random.normal(5, 0.5, 200)
	# 	d2 = np.random.normal(30, 1.2, 60)
	# 	d3 = np.random.normal(6, 1, 60)
	# 	d11 = np.random.normal(5, 0.5, 200)
	# 	d22 = np.random.normal(30, 1.2, 60)
	# 	d33 = np.random.normal(6, 1, 60)

	# 	y = np.concatenate((d1, d2, d3)).flatten()
	# 	y1 = np.concatenate((d11, d22, d33)).flatten()
	# 	x = np.arange(len(y))

	# else:
	# 	x = np.arange(len(df))
	# 	y = df['S1']
	# 	y1 = df['S2']
	
	if df is None:
		df = getdata.get_dataframe()

	x = np.arange(len(df))
	y1 = df['S1']
	y2 = df['S2']
	y3 = df['S3']
	y4 = df['S4']
	y5 = df['S5']
	y6 = df['S6']
	y7 = df['S7']

	fig = go.Figure()
	fig.add_trace(go.Scatter(x=x,
	                         y=y1,
	                         name='Sensor 1',
	                         marker_color='#E48F72'))
	fig.add_trace(go.Scatter(x=x,
	                         y=y2,
	                         name='Sensor 2',
	                         marker_color='green'))
	fig.add_trace(go.Scatter(x=x,
	                         y=y3,
	                         name='Sensor 3',
	                         marker_color='black'))
	fig.add_trace(go.Scatter(x=x,
	                         y=y4,
	                         name='Sensor 4',
	                         marker_color='violet'))
	fig.add_trace(go.Scatter(x=x,
	                         y=y5,
	                         name='Sensor 5',
	                         marker_color='gold'))
	fig.add_trace(go.Scatter(x=x,
	                         y=y6,
	                         name='Sensor 6',
	                         marker_color='darkviolet'))
	fig.add_trace(go.Scatter(x=x,
	                         y=y7,
	                         name='Sensor 7',
	                         marker_color='maroon'))

	fig.update_layout(title=dict(
					    x=0.5,
					    y=0.8,
	                    font=dict(size=20, color='white')),
					legend=dict(
				        bgcolor = '#373a40',
				        traceorder='normal',
				        font=dict(
				            size=12,
				            color= 'white'),
				    ),
					template='plotly_dark',
					height=330,
					width=800,
					font=dict(family="Courier",
					        size=12, color='#99aab5'),
					paper_bgcolor='rgba(0,0,0,0)',
					plot_bgcolor='#ccc',
				    margin=dict(t=50, b=70, l=80, r=1))
	fig.update_xaxes(title='Time Interval [2000ms]')
	fig.update_yaxes(title='WEIGHT in KILOGRAMS')
	return fig
