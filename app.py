import dash
import dash_core_components as dcc
import dash_html_components as html
import RPi.GPIO as io
import time
import pandas as pd

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
from dash.dash import no_update

import flask
from flaskwebgui import FlaskUI

from Layout.Home import home

relay = 16
io.setwarnings(False)
io.setmode(io.BOARD)
io.setup(relay, io.OUT)
io.output(relay, True)

server = flask.Flask(__name__)

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
