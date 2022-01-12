#import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_auth


from app import app
from app import server

USERNAME_PASSWORD_PAIRS = [['spyros','apiron']]



auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)




from apps import watches, sunglasses

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Watches|', href='/apps/watches'),
        html.Label('<---- Select mode ---->|'), 
        dcc.Link(' Sunglasses', href='/apps/sunglasses'),
    ], className="row" ,
                style={'margin-left': 80,
                       'margin-top': 20,
                       'align':'center'}),
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/watches':
        return watches.layout
    if pathname == '/apps/sunglasses':
        return sunglasses.layout
    else:
        return ""


if __name__ == '__main__':
    app.run_server(debug=False)