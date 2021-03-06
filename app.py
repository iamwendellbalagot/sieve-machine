import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import RPi.GPIO as io
import time
import datetime
import pandas as pd

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash.dash import no_update

import flask
from flaskwebgui import FlaskUI



import getdata.getdata as getdata

from Layout.Home import home
import Layout.plotGenerator as pg

relay = 16
io.setwarnings(False)
io.setmode(io.BOARD)
io.setup(relay, io.OUT)
io.output(relay, True)

server = flask.Flask(__name__)

TIMER = True

app = dash.Dash(
	__name__,
	server=server
)
app.title = 'Sieve Machine'

ui = FlaskUI(server, maximized=True)

app.layout = html.Div(
	className='app',
	children = [
		home
	]
)

#START TEST CALLBACK
@app.callback([Output('createTest__start', 'style'),
	Output('createTest__stop', 'style'),
	Output('interval__timer', 'disabled'),
	Output('interval__timer', 'max_intervals'),
	Output('interval__timer', 'n_intervals'),
	Output('interval__graph', 'disabled')],
	[Input('btn__startTest', 'n_clicks'),
	 Input('btn__stopTest', 'n_clicks'),
	 Input('input__testID', 'value'),
	 Input('input__sampleWeight', 'value'),
	 Input('input__time', 'value')])
def callback__startTestUI(btn__start, btn__stop, test_id, test_weight, test_time):
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

	if 'btn__startTest' in changed_id \
		and test_id != None and test_weight != None and test_time != None:
		time.sleep(1)
		getdata.process = True
		io.output(relay, False)
		return {'display': 'none'}, {'display':'block'}, False, test_time*60, 0, False
	if 'btn__stopTest' in changed_id:
		io.output(relay, True)
		time.sleep(5)
		getdata.process = False
		return {'display': 'block'}, {'display':'none'}, True, 0, 0, True
	else:
		raise PreventUpdate()
		
#START TIMER CALLBACK
@app.callback([Output('timer', 'children'),
	 Output('createTest__again', 'style'),
	 Output('btn__stopTest', 'disabled')],
	[Input('interval__timer', 'n_intervals'),
	 Input('input__time', 'value'),
	 Input('interval__timer', 'disabled'),
	 Input('input__testID', 'value'),
	 Input('input__sampleWeight', 'value')])
def callback__timer (n, inp_time, n_st, table, sampWeight ):
	try:
		if n == inp_time*60 and n_st==False:
			io.output(relay, True)
			time.sleep(5)
			getdata.process = False
			getdata.addResult(table=table, sampWeight=sampWeight, timer=inp_time)
			return str(datetime.timedelta(seconds=inp_time*60 - n)), {'display':'block'}, True
		if n:
			return str(datetime.timedelta(seconds=inp_time*60 - n)), no_update, no_update
		else:
			raise PreventUpdate()
	except:
		raise PreventUpdate()

#GENERATE DATA CALLBACK
@app.callback(Output('btn__stopTest', 'children'),
	[Input('interval__timer', 'disabled'),
	 Input('input__testID', 'value'),
	 Input('input__sampleWeight', 'value'),
	 Input('input__time', 'value')])
def callback__generateData(n_st, inp_id,inp_sampW, inp_timer):
	#changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	if n_st == False:
		getdata.generateData(table=inp_id, sampWeight=inp_sampW, timer=inp_timer)
		getdata.addResult(table=inp_id, sampWeight=inp_sampW, timer=inp_timer)
		return no_update
	else:
		raise PreventUpdate()

#GRAPH CALLBACK
@app.callback([Output('weights__plot', 'figure'),
	 Output('res__time', 'children'),
	 Output('res__weight', 'children'),
	 Output('res__artw', 'children'),
	 Output('res__err', 'children'),],
	[Input('btn__checkTest', 'n_clicks'),
	 Input('input__testID', 'value'),
	 Input('input__checkTest', 'value'),
	 Input('interval__graph', 'n_intervals'),
	 Input('interval__graph', 'disabled'),
	 Input('btn__exportTest', 'n_clicks'),
	 Input('input__exportTest', 'value')])
def callback__graph(btn_check, test_id, inp_check, n, n_st, btn_export, inp_export):
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	try:
		if n and n_st == False:
			print('UPDATING')
			return pg.get_scatter(df=getdata.get_dataframe(table=test_id)), no_update, no_update, no_update, no_update
		if 'btn__checkTest' in changed_id:
			df = getdata.get_dataframe(table=inp_check)
			data = getdata.generateXL(table=inp_check)
			data = data.round(2)
			x_bar = ((df['Sample_Weight'].iloc[-1]*(data['Weight Retained'].sum()/100)) + df['Sample_Weight'].iloc[-1]) / 2
			err_perc = ((x_bar - df['Sample_Weight'].iloc[-1])/ df['Sample_Weight'].iloc[-1]) * 100
			err_perc = round(abs(err_perc), 1)
			return pg.get_scatter(df=df), \
				str(df['Time'].iloc[-1])+' minute/s', str(df['Sample_Weight'].iloc[-1]) +' Kg', \
				str(round(df['Sample_Weight'].iloc[-1]*(data['Weight Retained'].sum()/100), 1)) + ' Kg', str(err_perc) + ' %'
		if 'btn__exportTest' in changed_id:
			#print(inp_export)
			#print(getdata.generateXL(table=inp_export))
			data = getdata.generateXL(table=inp_export)
			data = data.round(2)
			data = data.drop('Weight Retained', axis=1)
			data = data[['Coarse Sieve', 'Weight Retained Kg', 'Commulative WR %', 'Passing %']]
			data.to_csv('./csv_files/' + inp_export + '.csv', index=False, header=True)
			return no_update, no_update, no_update, no_update, no_update
		else:
			raise PreventUpdate()
	except:
		raise PreventUpdate()
		
#WEIGHTS CALLBACK
@app.callback([Output('sieve1', 'children'),
	Output('sieve2', 'children'),
	Output('sieve3', 'children'),
	Output('sieve4', 'children'),
	Output('sieve5', 'children'),
	Output('sieve6', 'children'),
	Output('sieve7', 'children')],
	[Input('input__testID', 'value'),
	 Input('interval__graph', 'n_intervals'),
	 Input('interval__graph', 'disabled')])
def callback__weight(test_id, n , n_st):
	try:
		if n and n_st == False:
			print('WEIGHING...')
			df = getdata.get_dataframe(table=test_id)
			return str(df['S1'].iloc[-1]) + ' kg', str(df['S2'].iloc[-1]) + ' kg', \
				str(df['S3'].iloc[-1])+ ' kg', str(df['S4'].iloc[-1])+ ' kg', \
				str(df['S5'].iloc[-1]) + ' kg', str(df['S6'].iloc[-1])+ ' kg', \
				str(df['S7'].iloc[-1])+ ' kg'
		else:
			raise PreventUpdate()
	except:
		raise PreventUpdate()
		
		

#CALIBRATION CALLBACK
@app.callback([Output('btn__stopCalib', 'style'),
	Output('btn__calibrate', 'style')],
	[Input('btn__calibrate', 'n_clicks'),
	Input('btn__stopCalib', 'n_clicks'),])
def callback__calibrate(btn__calibrate, btn__stopCalib):
	changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	if 'btn__calibrate' in changed_id:
		io.output(relay, False)
		return {'display': 'block'}, {'display': 'none'}
	if 'btn__stopCalib' in changed_id:
		io.output(relay, True)
		return {'display': 'none'}, {'display': 'block'}
	else:
		raise PreventUpdate();
		

if __name__ == '__main__':
	#app.run_server(debug=True)
	ui.run()
