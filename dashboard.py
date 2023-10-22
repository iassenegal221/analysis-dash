# myapp/dashapp/dashboard.py
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Data Visualization Dashboard"),
    html.Label("Select Action:", style={'font-size': '18px', 'margin-right': '10px'}),
    dcc.RadioItems(
        id='action-selector',
        options=[
            {'label': 'Visualize Selected Columns', 'value': 'visualize'},
            {'label': 'Print DataFrame', 'value': 'print'},
        ],
        value=None  # No default option selected
    ),
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

if __name__ == '__main__':
    app.run_server(debug=True)
