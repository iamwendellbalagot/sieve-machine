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

ui = FlaskUI(server)

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
	Output('interval__timer', 'n_intervals')],
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
		return {'display': 'none'}, {'display':'block'}, False, test_time*60, 0
	if 'btn__stopTest' in changed_id:
		time.sleep(1)
		getdata.process = False
		io.output(relay, True)
		return {'display': 'block'}, {'display':'none'}, True, 0, 0
	else:
		raise PreventUpdate()
		
#START TIMER CALLBACK
@app.callback([Output('timer', 'children'),
	 Output('createTest__again', 'style'),
	 Output('btn__stopTest', 'disabled')],
	[Input('interval__timer', 'n_intervals'),
	 Input('input__time', 'value'),
	 Input('interval__timer', 'disabled')])
def callback__timer (n, inp_time, n_st):
	try:
		if n == inp_time*60 and n_st==False:
			io.output(relay, True)
			getdata.process = False
			return str(datetime.timedelta(seconds=inp_time*60 - n)), {'display':'block'}, True
		if n:
			return str(datetime.timedelta(seconds=inp_time*60 - n)), no_update, no_update
		else:
			raise PreventUpdate()
	except:
		raise PreventUpdate()

#GENERATE DATA CALLBACK
@app.callback(Output('btn__stopTest', 'children'),
	[Input('interval__timer', 'disabled')])
def callback__generateData(n_st):
	#changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
	if n_st == False:
		getdata.generateData()
		return no_update
	else:
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
	app.run_server(debug=True)
	#ui.run()
