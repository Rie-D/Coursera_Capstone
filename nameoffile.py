# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(
                                    id='side-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value'=: 'All'},
                                        {'label': 'CCAFS LC-40', 'value'=: 'LC-40'},
                                        {'label': 'CVAFB SLC-4E', 'value'=: 'SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value'=: 'LC-39A'},
                                        {'label': 'CCAFS SLC-40', 'value'=: 'SLC-40'}    
                                    ],
                                    value= 'All Sites'
                                    placeholder= 'Select a Launch Site here'
                                    searchable= True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider', ,min=0, max=10000, step=1000, value=['min_payload', 'max_payload']),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback (
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='input-year', component_property='value'))
def pie(site_dropdown):
    if site_dropdown == 'All':
        pie_fig=px.pie(spacex_df, values='class',names='Launch Site', title='Success Launches for All Site')
        return pie_fig
    else:
        filtered_pie=spacex_df[spacex_df['Launch Site'] ==['site_dropdown']]
        class_pie=filtered_pie.groupby(['Launch Site','class']).size().reset_index(name='class count')
        pie_fig=px.pie(class_pie, value='class count', names='class',title='Success Launches for site')
        return pie_fig   



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    [Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_id='value'),
    Input(component_id='payload-slider', component_id='value')])
def scatter(site_dropdown, slider_range):
    low, high=slider_range
    masks=(spacex_df['Payload Mass (kg)'] > low) & (spacex_df['Payload Mass (kg)'] < high)
    df_scatter=spacex_df[masks]
    if site_dropdown == 'All':
        scatter_fig=px.scatter(df_scatter, x='Payload Mass (kg)', y='class', color='Boosster Version Category', title='Payload Success Rate for All site')
        return scatter_fig
    else:
        filterd_scatter=df_scatter[df_scatter['Launch Site'] == site_dropdown]
        scatter_fig=px.scatter(filterd_scatter, x='Payload Mass (kg)' y='class', color='Boosster Version Category' title='Payload Success Rate for {site_dropdown}')    

# Run the app
if __name__ == '__main__':
    app.run_server()
