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