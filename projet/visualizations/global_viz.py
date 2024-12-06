import json
import os
from collections import Counter
import plotly.graph_objects as go

# Mapping for full category names and colors
category_info = {
    "kws": {"name": "keywords", "color": "#636EFA"},       # Blue
    "org": {"name": "organizations", "color": "#EF553B"},  # Red
    "loc": {"name": "locations", "color": "#00CC96"},      # Green
    "per": {"name": "persons", "color": "#AB63FA"}         # Purple
}

# Function to plot top 10 bar charts
def plot_top_10(data, category):
    if category not in data:
        print(f"Category {category} not found in the data.")
        return None

    # Count occurrences
    counter = Counter(data[category])
    top_10 = counter.most_common(10)
    labels, counts = zip(*top_10)

    # Full name and color of the category
    full_name = category_info[category]["name"]
    color = category_info[category]["color"]

    # Create the bar chart
    fig = go.Figure(data=[go.Bar(x=labels, y=counts, marker_color=color)])
    fig.update_layout(
        title=f"Top 10 {full_name} by Frequency",
        xaxis_title=full_name,
        yaxis_title="Frequency",
        template="plotly_dark",
    )
    return fig  # Return the figure instead of showing it

# Function to plot the pie chart
def plot_pie_chart(data):
    # Count categories
    categories = ["kws", "org", "loc", "per"]
    category_counts = {category: len(data[category]) for category in categories if category in data}

    # Use full names and colors
    labels = [category_info[cat]["name"] for cat in category_counts.keys()]
    values = list(category_counts.values())
    colors = [category_info[cat]["color"] for cat in category_counts.keys()]

    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3, marker=dict(colors=colors))])
    fig.update_layout(
        title="Proportions of Categories in the Dataset",
        template="plotly_dark",
    )
    return fig  # Return the figure instead of showing it
