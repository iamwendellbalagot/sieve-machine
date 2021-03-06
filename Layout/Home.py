import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

from .plotGenerator import get_scatter

home = html.Div(
	className = 'home',
	children = [
		html.Div(
			className='home__left',
			children=[
				html.Div(
					className='home__leftControls',
					children=[
						html.H2('CONTROLS'),
						html.Hr(),
						html.Fieldset(
							className='controls__createTest',
							children=[
								html.Legend('CREATE A TEST'),
								html.Div(
									id = 'createTest__start',
									children=[
										dcc.Input(
											id='input__testID',
											type='text',
											placeholder='Test ID'
										),
										dcc.Input(
											id='input__sampleWeight',
											type='number',
											placeholder='Weight of Sample (Kg)'
										),
										dcc.Input(
											id='input__time',
											type='number',
											placeholder='Minutes'
										),
										html.Button('START', id='btn__startTest')
									]
								),
								html.Div(
									id='createTest__stop',
									style={'display': 'none'},
									children=[
										html.Div(
											html.H3('12:00', id='timer')
										),
										html.Button('STOP', id='btn__stopTest')
									]
								),
								html.Div(
									id='createTest__again',
									style={'display':'none'},
									children=[
										html.A(html.Button('CREATE ANOTHER TEST?', id='btn__againTest'), href='/')
									]
								)
							]
						),
						html.Fieldset(
							className='controls__utilities',
							children=[
								html.Legend('UTILITIES'),
								html.Div(
									children=[
										html.Span('CHECT TEST RESULTS:'),
										html.Div(
											children=[
												html.Button('CHECK', id='btn__checkTest'),
												dcc.Input(
													id='input__checkTest',
													type='text',
													placeholder='Test ID'
												)
											]
										),
										html.Span('EXPORT DATA:'),
										html.Div(
											children=[
												html.Button('EXPORT', id = 'btn__exportTest'),
												dcc.Input(
													id='input__exportTest',
													type='text',
													placeholder='Test ID'
												)
											]
										),
										html.Span('MOTOR CALIBRATION:'),
										html.Button(
											id='btn__calibrate',
											children='CALIBRATE'
										),
										html.Button(
											id='btn__stopCalib',
											children='STOP'
										)
									]
								)
							]
						),
						html.Fieldset(
							className='controls__results',
							children=[
								html.Legend('RESULTS'),
								html.Ul(
									children=[
										html.Li(
											children=[
												html.Span('Time: '),
												html.P('0 minute/s', id='res__time')
											]
										),
										html.Li(
											children=[
												html.Span('Weight of Sample: '),
												html.P('0 Kg', id='res__weight')
											]
										),
										html.Li(
											children=[
												html.Span('ARTW: '),
												html.P('0 Kg', id='res__artw')
											]
										),
										html.Li(
											children=[
												html.Span('Error %: '),
												html.P('0', id='res__err')
											]
										)
									]
								)
							]
						)
					]
				)
			]
		),
		html.Div(
			className='home__right',
			children=[
				html.Div(
					className='home__rightPlot',
					children =[
						html.H2('LIVE PLOT'),
						html.Hr(),
						dcc.Graph(
							id ='weights__plot',
							figure=get_scatter()
						)
					]
				),
				html.Div(
					className='home__rightWeights',
					children= [
						html.H2('SENSORS OUTPUT'),
						html.Hr(),
						html.Div(
							children=[
								html.Ul(
									children=[
										html.Li([
											html.Span('Sieve 1:'),
											html.P('0.0 kg', id='sieve1')
										]),
										html.Li([
											html.Span('Sieve 2:'),
											html.P('0.0 kg', id='sieve2')
										]),
										html.Li([
											html.Span('Sieve 3:'),
											html.P('0.0 kg', id='sieve3')
										])
									]
								),
								html.Ul(
									children=[
										html.Li([
											html.Span('Sieve 4:'),
											html.P('0.0 kg', id='sieve4')
										]),
										html.Li([
											html.Span('Sieve 5:'),
											html.P('0.0 kg', id='sieve5')
										]),
										html.Li([
											html.Span('Sieve 6:'),
											html.P('0.0 kg', id='sieve6')
										])
									]
								),
							]
						),
						html.Li([
							html.Span('Pan:'),
							html.P('0.0 kg', id='sieve7')
						]),
					]
				)
			]
		),
		#INTERVALS
		dcc.Interval(
			id='interval__timer',
			n_intervals=0,
			interval=1000,
			disabled=True
		),
		dcc.Interval(
			id='interval__graph',
			n_intervals=0,
			interval=1000,
			disabled=True
		),
		dcc.Input(
			id='dummy__timer',
			type='number',
			style={'display': 'none'},
			value=1
		)
	]
)
