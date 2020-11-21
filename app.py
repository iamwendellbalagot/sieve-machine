import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

from Layout.Home import home

app = dash.Dash(
	__name__,
)

app.layout = html.Div(
	className='app',
	children = [
		home
	]
)

if __name__ == '__main__':
	app.run_server(debug=True)