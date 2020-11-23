import dash_core_components as dcc
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
										html.Button('START', id='btn__start')
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
												html.Button('CHECK'),
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
												html.Button('EXPORT'),
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
												html.P('12 minutes')
											]
										),
										html.Li(
											children=[
												html.Span('Weight of Sample: '),
												html.P('25 Kg')
											]
										),
										html.Li(
											children=[
												html.Span('ARTW: '),
												html.P('97')
											]
										),
										html.Li(
											children=[
												html.Span('Error: '),
												html.P('56')
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
											html.P('100 grams')
										]),
										html.Li([
											html.Span('Sieve 2:'),
											html.P('100 grams')
										]),
										html.Li([
											html.Span('Sieve 3:'),
											html.P('100 grams')
										])
									]
								),
								html.Ul(
									children=[
										html.Li([
											html.Span('Sieve 4:'),
											html.P('100 grams')
										]),
										html.Li([
											html.Span('Sieve 5:'),
											html.P('1200 grams')
										]),
										html.Li([
											html.Span('Sieve 6:'),
											html.P('0 grams')
										])
									]
								),
							]
						),
						html.Li([
							html.Span('Sieve 7:'),
							html.P('100 grams')
						]),
					]
				)
			]
		)
	]
)
