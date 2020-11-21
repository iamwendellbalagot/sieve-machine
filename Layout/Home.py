import dash_core_components as dcc
import dash_html_components as html

home = html.Div(
	className = 'home',
	children = [
		html.Div(
			className='home__right',
			children=[
				html.Div(
					className='home__leftControls',
					children='This is Controls'
				)
			]
		),
		html.Div(
			className='home__left',
			children=[
				html.Div(
					className='home__rightPlot',
					children ='This is a plot'
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