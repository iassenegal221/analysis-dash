import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import re
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Data Visualization Dashboard"),
    html.Div([
        html.Label("Select Action:", style={'font-size': '18px', 'margin-right': '10px'}),
        dcc.RadioItems(
            id='action-selector',
            options=[
                {'label': 'Visualize Selected Columns', 'value': 'visualize'},
                {'label': 'Print DataFrame', 'value': 'print'},
            ],
            value=None  # No default option selected
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'margin-bottom': '20px'}),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select a File'),
        ]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px auto',
        },
        multiple=False
    ),
    dcc.Markdown(id='dataframe-output', style={'margin-top': '10px', 'font-size': '16px', 'white-space': 'pre-line'}),
    dcc.Dropdown(id='column-selector-x', multi=False, style={'display': 'none'}),
    dcc.Dropdown(id='column-selector-y', multi=False, style={'display': 'none'}),
    dcc.Graph(id='visualization-output'),
    html.Button('Print DataFrame', id='print-button', style={'display': 'none'}),
])

def read_data(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return pd.read_excel(BytesIO(decoded), engine='openpyxl')

@app.callback(
    Output('column-selector-x', 'style'),
    Output('column-selector-y', 'style'),
    Input('action-selector', 'value')
)
def toggle_column_selectors(action):
    if action == 'visualize':
        return {'display': 'block'}, {'display': 'block'}
    return {'display': 'none'}, {'display': 'none'}

@app.callback(
    Output('column-selector-x', 'options'),
    Output('column-selector-y', 'options'),
    Input('upload-data', 'contents')
)
def update_column_selectors(contents):
    if contents is None:
        return [], []

    df = read_data(contents)
    columns = [{'label': col, 'value': col} for col in df.columns]
    return columns, columns

@app.callback(
    Output('visualization-output', 'figure'),
    Output('dataframe-output', 'children'),
    Output('print-button', 'style'),
    Input('upload-data', 'contents'),
    Input('column-selector-x', 'value'),
    Input('column-selector-y', 'value'),
    Input('action-selector', 'value')
)
def update_visualization(contents, selected_column_x, selected_column_y, action):
    if contents is None or (action == 'visualize' and (not selected_column_x or not selected_column_y)):
        return {'data': []}, '', {'display': 'none'}

    df = read_data(contents)

    if action == 'visualize' and selected_column_x in df.columns and selected_column_y in df.columns:
        grouped = df.groupby([selected_column_x, selected_column_y]).size().unstack(fill_value=0)
        grouped.plot(kind='bar', stacked=False)
        plt.xlabel(selected_column_x)
        plt.ylabel('Count')
        plt.title(f'{selected_column_y} by {selected_column_x}')
        plt.xticks(rotation=45)
        plt.legend(title=selected_column_y)
        
        # Convert Matplotlib figure to Plotly figure for use in Dash
        fig = plt.gcf()
        fig.set_size_inches(12, 6)
        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        plt.close(fig)

        return {
            'data': [{
                'x': grouped.index,
                'y': grouped[column],
                'type': 'bar',
                'name': column
            } for column in grouped.columns],
            'layout': {
                'xaxis': {'title': selected_column_x},
                'yaxis': {'title': 'Count'},
                'title': f'{selected_column_y} by {selected_column_x}',
                'xaxis_tickangle': 45,
            }
        }, '', {'display': 'none'}

    elif action == 'print':
        return {'data': []}, '```\n' + df.to_markdown() + '\n```', {'display': 'inline'}

if __name__ == '__main__':
    app.run_server(debug=True)

