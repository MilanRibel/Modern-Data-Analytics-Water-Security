# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 17:29:50 2022

@author: shivs
"""

import pandas as pd
import plotly.express as px

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
app = dash.Dash(__name__)
server=app.server

df = pd.read_csv("water_security.csv")

app.layout = html.Div([

    html.H1("Water Security by decade", style={'text-align': 'center'}),
    html.P("[0-1): Low stress (<10%) - LEVEL 1"),
    html.P("[1-2): Low ro medium stress (10-20%) - LEVEL 2"),
    html.P( "[2-3): Medium to high stress (20-40%) - LEVEL 3"),
    html.P( "[3-4): High stress (40-80%) - LEVEL 4"),
    html.P("[4-5): Extremely high stress (>80%) - LEVEL 5"),

    dcc.Dropdown(id="slct_year",
                 options=[
                     {"label": "2020", "value": "Year_2020"},
                     {"label": "2030", "value": "Year_2030"},
                     {"label": "2040", "value": "Year_2040"},
                 ],
                 multi=False,
                 value="Year_2040",
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[["Name", option_slctd]]

    # Plotly Express
    fig = px.choropleth(
        data_frame=dff,
        locations=dff['Name'],
        locationmode='country names',
        color=option_slctd,
        hover_data=['Name', option_slctd],
        color_continuous_scale=px.colors.sequential.YlOrRd
    )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)