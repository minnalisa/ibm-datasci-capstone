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
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {"label": "All Site", "value": "all_site"},
                                        {"label": "CCAFS LC-40",
                                            "value": "CCAFS LC-40"},
                                        {"label": "VAFB SLC-4E",
                                            "value": "VAFB SLC-4E"},
                                        {"label": "KSC LC-39A",
                                            "value": "KSC LC-39A"},
                                        {"label": "CCAFS SLC-40",
                                            "value": "CCAFS SLC-40"}
                                    ],
                                    value="all_site",
                                    placeholder="Select a Launch Site here",
                                    searchable=True
),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(
                                    id='payload-slider',
                                    min=0,
                                    max=10000,
                                    step=1000,
                                    value=[min_payload, max_payload]
),
    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(
                                    dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_graph(launch_site):
    if launch_site == "all_site":
        fig = px.pie(
            spacex_df,
            values="class",
            names="Launch Site",
            title="Total Success Launches by Site"
        )
    else:
        data = spacex_df[spacex_df["Launch Site"] == launch_site]
        fig = px.pie(
            data,
            values=[data[data["class"] == 1]["class"].count(
            ), data[data["class"] == 0]["class"].count()],
            names=[1, 0],
            title="Total Success Launches for site " + launch_site
        )
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


@app.callback(
    Output(component_id='success-payload-scatter-chart',
           component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def get_graph(launch_site, payload):
    data = spacex_df
    data["Payload Mass (kg)"] = data["Payload Mass (kg)"].astype("int")
    data = data[(data["Payload Mass (kg)"] >= payload[0]) &
                (data["Payload Mass (kg)"] <= payload[1])]
    site_name = "All Sites"
    if launch_site != "all_site":
        data = data[data["Launch Site"] == launch_site]
        site_name = launch_site

    fig = px.scatter(
        data,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        title="Correlation between Payload (KG) and Success Rate for " +
        site_name
    )
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
