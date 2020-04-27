import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go  # or plotly.express as px
import plotly.express as px
import locale
from covid import COVID
locale.setlocale(locale.LC_ALL, '')

def build_df():
    covid = COVID()
    return covid.data.ecdc()

def plot_scatter(df, continent="Americas",start_date="2020-03-01"):

    mask = (df['dateRep'] > start_date)
    df = df.loc[mask]


    print(f"before sort: {df.shape}")
    df = df.sort_values(by=["dateRep"], ascending=True)
    #df = df[(df['continent'] == continent)]
    print(f"unique continents: {df['continent'].unique()}")
    return px.scatter(
        df,
        x="cases_sum_to_date", y="cases_growth",
        animation_frame="dateRep_str", animation_group="countriesAndTerritories",
        size="deaths_sum_to_date", color="continent", hover_name="countriesAndTerritories",
        log_x=True, size_max=50,
        range_x=[df['cases_sum_to_date'].min(), df['cases_sum_to_date'].max()],
        range_y=[df['cases_growth'].min(), df['cases_growth'].quantile(0.75)]
    )

df = build_df()

fig = plot_scatter(df)
#fig = go.Figure()  # or any Plotly Express function e.g. px.bar(...)
# fig.add_trace( ... )
# fig.update_layout( ... )


app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Turn off reloader if inside Jupyter
app.run_server(debug=True, use_reloader=False)
