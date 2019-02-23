import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table as dt

import pandas as pd
import os

PATH_TO_TABLE = os.path.abspath("data_population.txt")


def open_data_from_file(path):
    """Open table from a file using pandas"""
    data = pd.read_csv(path, sep='\t', skiprows=[1, 2], index_col=False)
    return data


df = open_data_from_file(PATH_TO_TABLE)

app = dash.Dash()

app.layout = html.Div(
    children=[
        html.Div([
            html.H1(children='Country statistics',
                    style={'textAlign': 'left', 'width': '100%', 'backgroundColor': 'rgb(0, 153, 230)', 'marginTop': 30,
                           'marginBottom': 30, 'padding': '40px'}
                    ),
            html.H2('Information on countries'),
            dt.DataTable(
                id='table',
                data=df.to_dict('rows'),
                columns=[{"name": i, "id": i} for i in df.columns],
                row_selectable=True,
                sorting=True,
                style_cell={'textAlign': 'left', 'padding': '5px', 'backgroundColor': 'rgb(230, 238, 255)',
                            'minWidth': '0px', 'maxWidth': '50px'},
                style_header={
                    'backgroundColor': 'rgb(0, 153, 230)',
                    'fontWeight': 'bold'
                },
                style_table={'backgroundColor': 'rgb(0, 153, 230)'}

            )
        ], style={'textAlign': 'center', 'width': '100%'}),

        html.Div([
            dcc.Dropdown(
                id='name-dropdown',
                options=[{'label': i, 'value': i} for i in df.columns if i != "COUNTRY"],
                placeholder="Select statistics"),
            html.Div(id='leftoutput-container',
                     style={'backgroundColor': 'rgb(230, 238, 255)',
                            'display': 'inline-block'}),
        ],
            style={'textAlign': 'center', 'width': '100%', 'columnCount': 2, 'marginTop': 30, 'marginBottom': 30})
    ]
)


@app.callback(
    output=dash.dependencies.Output('leftoutput-container', 'children'),
    inputs=[dash.dependencies.Input('name-dropdown', 'value')]
)
def update_output(value):
    if value:
        return generate_plot(df["COUNTRY"], value)


def generate_plot(country, value):
    return html.Div(
        dcc.Graph(
            id='yield-graph',
            figure={
                'data': [
                    {'x': country, 'y': df[value], 'type': 'line', 'name': value},
                ],
                'layout': {
                    'title': '{}'.format(value)
                }
            }
        )
    )


def main():
    app.run_server(debug=True)


if __name__ == '__main__':
    main()
