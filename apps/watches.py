import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
from app import app
import pathlib
pd.set_option('display.max_columns', None)# -*- coding: utf-8 -*-




PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()




# Resellers
resellers = pd.read_csv(DATA_PATH.joinpath('brandPerResellerWatches.csv'), index_col = 0)
resellers.drop_duplicates(subset = ['RESELLER', 'BRAND', 'GENDER'], inplace=True)
resellers.dropna(inplace=True)
resellers['BRAND'] = resellers['BRAND'].str.lower()
resellers['BRAND'] = resellers['BRAND'].str.title() 
resellers['BRAND'] = resellers['BRAND'].str.replace('-', ' ')
resellers = resellers.sort_values(by=['BRAND'])
resellers.reset_index(inplace=True)

discount = pd.read_csv(DATA_PATH.joinpath('resellerDiscountWatches.csv'), index_col = 0)
discount.reset_index(drop=False, inplace = True)

# Brand-Picker
brand_list=[]
for brand in resellers['BRAND'].unique():
    brand_list.append({'label':str(brand),'value':brand})
    
# Reseller-Picker
reseller_list=[]
for reseller in resellers['RESELLER'].unique():
    reseller_list.append({'label':str(reseller),'value':reseller})
    

# shop-Picker
shop_list=[]
for shop in discount['RESELLER'].unique():
    shop_list.append({'label':str(shop),'value':shop})
    
    
####################################################################
############################## Layout ##############################
####################################################################



# Set Layout

layout = dbc.Container([
    
dbc.Row([
      dbc.Col(html.H1("Watches Case",
                      className='text-center text-primary, mb-4'),
              width=10) 
        
]),
    
   
    
dbc.Row([
    
    dbc.Col([
                html.Label('Select a brand you want to compare'), 
                dcc.Dropdown(id='brand-picker-watches', options=brand_list,
          placeholder="Select a brand",
          ),
                ] , 
                width={'size':3},
                style={'marginBottom': 50, 'marginTop': 150}),
                 
        
    dbc.Col([
                html.Label('Select a brand you want to compare with'), 
                dcc.Dropdown(id='brand-picker2-watches', options=brand_list,
          placeholder="Select a brand",
          ),
                ], 
                width={'size':3},  
                style={'marginBottom': 50, 'marginTop': 150}),
       
    
    dbc.Col([
                html.H3('Brand pick'),
                dcc.Graph(id='resellers-watches-1')
                ], width={'size':6}),
        
]),

dbc.Row([
    
    dbc.Col([
                html.Label('Select a reseller you want to compare'), 
                dcc.Dropdown(id='reseller-picker-watches', options=reseller_list,
          placeholder="Select a reseller",
          ),
                ] , 
                width={'size':3},
                style={'marginBottom': 50, 'marginTop': 150}),
    
   
    dbc.Col([
                html.Label('Select a reseller you want to compare with'), 
                dcc.Dropdown(id='reseller-picker2-watches', options=reseller_list,
          placeholder="Select a reseller",
          ),
                ], 
                width={'size':3},  
                style={'marginBottom': 50, 'marginTop': 150}),
   
    dbc.Col([
                html.H3('Reseller pick'),
                dcc.Graph(id='resellers-watches-2')
                ], width={'size':6}),
   
    
]),

dbc.Row([
    
    dbc.Col([
                dcc.RadioItems(id='mode',
        options=[
            {'label': ' Search the whole site', 'value': 'whole'},
            {'label': ' Keep only landing page', 'value': 'front'},
      
        ],value='whole',
        labelStyle={'display': 'block'}), 
                ],
        style={'marginBottom': 50, 'marginTop': 100}),
                 
        
    dbc.Col([
                html.Label('Select a shop you want to compare'), 
                dcc.Dropdown(id='shop-picker', options=shop_list,
          placeholder="Select a brand",
          ),
                ] , 
                #width={'size':3},
                style={'marginBottom': 50, 'marginTop': 100}),
                 
        
    dbc.Col([
                html.Label('Compare with another shop'), 
                dcc.Dropdown(id='shop-picker2', options=shop_list,
          placeholder="Select a brand",
          ),
                ], 
                #width={'size':3},  
                style={'marginBottom': 50, 'marginTop': 100}),
       
    
    dbc.Col([
                html.H3('Shop discounts'),
                dcc.Graph(id='discountGraphWatches')
                ], width={'size':6}),
            
              
            ]),



], fluid=False)





####################################################################
######################### Callback Graphs ##########################
####################################################################

 
     
 
@app.callback(Output('resellers-watches-1', 'figure'),# Output('children', 'children')],
                [Input('brand-picker-watches', 'value'), 
                 Input('brand-picker2-watches', 'value')])
def update_brand_figure_(selected_brand, selected_brand2):
    
    filtered_df = resellers[resellers['BRAND'] == selected_brand]
    filtered_df.reset_index(drop=True, inplace=True)
   
    
    filtered_df2 = resellers[resellers['BRAND'] == selected_brand2]
    filtered_df2.reset_index(drop=True, inplace=True)

    data = [{
              'legendgroup': '',
              'line': {'color': '#fa6386', 'dash': 'solid'},
              'marker': {'symbol': 'x', 'size': 10},
              'mode': 'markers',
              'name': '',
              'orientation': 'v',
              'showlegend': False,
              'type': 'scatter',
              'x':filtered_df['LM_Ratings'],
              'xaxis': 'x',
              'y': filtered_df['LM_Positive'],
              'hovertemplate' : 'RESELLER: ' + filtered_df['RESELLER'] + ' BRAND: ' + filtered_df['BRAND'],
              'yaxis': 'y'},
            {
              'legendgroup': '',
              'line': {'color': '#636efa', 'dash': 'dashed'},
              'marker': {'symbol': 'cross', 'size': 10},
              'mode': 'markers',
              'name': '',
              'orientation': 'v',
              'showlegend': False,
              'type': 'scatter',
              'x': filtered_df2['LM_Ratings'],
              'xaxis': 'x',
              'y': filtered_df2['LM_Positive'],
              'hovertemplate' : 'RESELLER: ' + filtered_df2['RESELLER'] + ' BRAND: ' + filtered_df2['BRAND'],
              'yaxis': 'y'}]

    fig = {
          'data': data,
          'layout': go.Layout(
              xaxis={'title': 'Number of Reviews'},
              yaxis={'title': 'Percentage of positive Reviews'},
              hovermode='closest', paper_bgcolor="LightSteelBlue",
          )
          }
      
    return fig
 


@app.callback(Output('resellers-watches-2', 'figure'),# Output('children', 'children')],
                [Input('reseller-picker-watches', 'value'), 
                Input('reseller-picker2-watches', 'value')])
def update_reseller_figure(selected_reseller, selected_reseller2):
    
    filtered_df = resellers[resellers['RESELLER'] == selected_reseller]
    filtered_df = filtered_df[['RESELLER', 'GENDER','LM_Ratings', 'LM_Positive', 'BRAND']]
    filtered_df.reset_index(drop=True, inplace=True)
    filtered_df = filtered_df.groupby(['RESELLER','GENDER','LM_Ratings','LM_Positive']).count()
    filtered_df.reset_index(drop=False, inplace=True)
    print(filtered_df)
    filtered_df2 = resellers[resellers['RESELLER'] == selected_reseller2]
    filtered_df2 = filtered_df2[['RESELLER', 'GENDER','LM_Ratings', 'LM_Positive', 'BRAND']]
    filtered_df2.reset_index(drop=True, inplace=True)
    filtered_df2 = filtered_df2.groupby(['RESELLER','GENDER','LM_Ratings','LM_Positive']).count()
    filtered_df2.reset_index(drop=False, inplace=True)
    print(filtered_df2)
    
    data = [{
              'legendgroup': filtered_df['RESELLER'],
              'name': selected_reseller,
              'orientation': 'v',
              'showlegend': True,
              'type': 'bar',
              'x':filtered_df['GENDER'],
              'xaxis': 'x',
              'y': filtered_df['BRAND'],
              'text': filtered_df['BRAND'],
              'color': filtered_df['RESELLER'],
              'yaxis': 'y'},
            {
              'legendgroup': filtered_df2['RESELLER'],
              'name': selected_reseller2,
              'orientation': 'v',
              'showlegend': True,
              'type': 'bar',
              'x': filtered_df2['GENDER'],
              'xaxis': 'x',
              'y': filtered_df2['BRAND'],
              'text': filtered_df2['BRAND'],
              'color': filtered_df2['RESELLER'],
              'yaxis': 'y'}]
    
            

    fig = {
          'data': data,
          'layout': go.Layout(
              xaxis={'title': 'Gender'},
              yaxis={'title': 'Number of Brands'}, barmode='group',
              hovermode='closest', paper_bgcolor="LightSteelBlue",
          )
          }
    
    
    
    
    

      
    return fig
 
    
@app.callback(Output('discountGraphWatches', 'figure'),
                [Input('shop-picker', 'value'), 
                 Input('shop-picker2', 'value'),
                 Input('mode', 'value')])
def update_shop_figure(selected_reseller, selected_reseller2, mode):
    
    if mode == 'whole':
        filtered_df = discount[discount['RESELLER'] == selected_reseller]
        filtered_df.reset_index(drop=True, inplace=True)
        
        filtered_df2 = discount[discount['RESELLER'] == selected_reseller2]
        filtered_df2.reset_index(drop=True, inplace=True)
        
    elif mode == 'front':
        front = pd.DataFrame()
        for shop in discount['RESELLER'].unique():
            front = front.append(discount[discount['RESELLER']==shop].head(30))
            
        filtered_df = front[front['RESELLER'] == selected_reseller]
        filtered_df.reset_index(drop=True, inplace=True)
        
        filtered_df2 = front[front['RESELLER'] == selected_reseller2]
        filtered_df2.reset_index(drop=True, inplace=True)

    data = [{
              'legendgroup': '',
              'name': selected_reseller,
              'orientation': 'v',
              'showlegend': True,
              'type': 'histogram',
              'x':filtered_df['Discount'],
              'xaxis': 'x',
              #'y': filtered_df['LM_Positive'],
              #'hovertemplate' : 'RESELLER: ' + filtered_df['RESELLER'] + ' BRAND: ' + filtered_df['BRAND'],
              'yaxis': 'y'},
            {
              'legendgroup': '',
              'name': selected_reseller2,
              'orientation': 'v',
              'showlegend': True,
              'type': 'histogram',
              'x': filtered_df2['Discount'],
              'xaxis': 'x',
              #'y': filtered_df2['LM_Positive'],
              #'hovertemplate' : 'RESELLER: ' + filtered_df2['RESELLER'] + ' BRAND: ' + filtered_df2['BRAND'],
              'yaxis': 'y'}]

    fig = {
         'data': data,
         'layout': go.Layout(
             xaxis={'title': 'Discount'},
             yaxis={'title': 'counts'},
             hovermode='closest', paper_bgcolor="LightSteelBlue",
         )
         }
      
    return fig
