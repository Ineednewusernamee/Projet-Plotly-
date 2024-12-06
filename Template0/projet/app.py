import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from visualizations.visualizations import create_treemap, create_heatmap
from visualizations.global_viz import plot_top_10, plot_pie_chart
from visualizations.clustering import clustering_analysis
from visualizations.wordclouds import create_and_save_word_cloud
from utils.json_processor import load_json, process_metadata, process_data, combine_entities

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True,
)
server = app.server

# --- Load the JSON Data ---
file_path = "./data/fr.sputniknews.africa--20220630--20230630.json"
data = load_json(file_path)
metadata = process_metadata(data)
daily_data = process_data(data)
combined_entities = combine_entities(data)

# --- Generate Figures ---
pie_chart_fig = plot_pie_chart(data["metadata"]["all"])
top_10_figures = [
    plot_top_10(data["metadata"]["all"], category) for category in ["kws", "org", "loc", "per"]
]

# --- App Layout ---
app.layout = dbc.Container([
    html.H1("Data Visualization Dashboard", style={"textAlign": "center", "marginBottom": "20px"}),

    # KPIs
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Total Articles"),
            dbc.CardBody(html.H5(f"{daily_data['article_count'].sum()}")),
        ], color="primary", inverse=True), width=3),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Total Keywords"),
            dbc.CardBody(html.H5(f"{len(metadata)}")),
        ], color="success", inverse=True), width=3),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Entities Analyzed"),
            dbc.CardBody(html.H5(f"{len(combined_entities)}")),
        ], color="info", inverse=True), width=3),
    ]),

    # Pie Chart
    html.H2("Category Distribution", style={"textAlign": "center"}),
    dcc.Graph(figure=pie_chart_fig),

    # Top 10 Bar Charts for Each Category
    html.H2("Top 10 Keywords, Organizations, Locations, and Persons", style={"textAlign": "center"}),
    dbc.Row([dcc.Graph(figure=fig) for fig in top_10_figures]),

    # Existing Graphs
    html.H2("Treemap", style={"textAlign": "center"}),
    dcc.Graph(figure=create_treemap(metadata)),

    html.H2("Heatmap", style={"textAlign": "center"}),
    dcc.Graph(figure=create_heatmap(daily_data)),

    html.H2("Clustering Analysis", style={"textAlign": "center"}),
    dcc.Graph(figure=clustering_analysis(data, combined_entities)),

    html.H2("Word Cloud", style={"textAlign": "center"}),
    html.Img(src="/assets/wordcloud.png", style={"width": "80%", "margin": "auto"}),
], fluid=True)

if __name__ == "__main__":
    # Generate and save the Word Cloud only once
    print("JSON loaded successfully!")
    print(f"Total unique entities after filtering: {len(combined_entities)}")
    entity_dict = metadata.set_index("keyword")["frequency"].to_dict()
    create_and_save_word_cloud(entity_dict, output_path="./assets/wordcloud.png")
    
    # Run the app
    app.run_server(debug=True)
