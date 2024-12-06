import json
import pandas as pd
from datetime import datetime
from collections import Counter

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print("JSON loaded successfully!")
    return data

def process_metadata(data):
    """Extract keyword frequencies from metadata."""
    keywords_data = data['metadata']['all']['kws']
    return pd.DataFrame(keywords_data.items(), columns=["keyword", "frequency"])

def process_data(data):
    """Extract and aggregate article counts by date."""
    article_dates = []

    for year, months in data['data'].items():
        for month, days in months.items():
            for day, articles in days.items():
                date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")
                article_dates.extend([date] * len(articles))

    df_dates = pd.DataFrame(article_dates, columns=["date"])
    daily_counts = df_dates.groupby("date").size().reset_index(name="article_count")
    return daily_counts

def combine_entities(data, min_frequency=1):
    """
    Combine all entity types (kws, loc, org, per, mis) into a single dictionary.
    Optionally filter by minimum frequency.
    """
    combined_entities = Counter()

    for year, months in data['data'].items():
        for month, days in months.items():
            for day, articles in days.items():
                for article in articles:
                    # Combine all entity categories
                    for key in ['kws', 'loc', 'org', 'per', 'mis']:
                        if key in article and isinstance(article[key], dict):
                            combined_entities.update(article[key])

    # Filter by minimum frequency
    filtered_entities = {key: value for key, value in combined_entities.items() if value >= min_frequency}
    print(f"Total unique entities after filtering: {len(filtered_entities)}")
    return filtered_entities
