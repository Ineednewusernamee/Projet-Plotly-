from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd
import plotly.express as px
from itertools import combinations
from collections import Counter

def clustering_analysis(data, combined_entities, min_frequency=5, top_n=1000, n_clusters=5):
    """
    Perform clustering on combined entities based on co-occurrence.
    """
    co_occurrence = Counter()

    for year, months in data['data'].items():
        for month, days in months.items():
            for day, articles in days.items():
                for article in articles:
                    # Gather all entities in an article
                    entities = []
                    for key in ['kws', 'loc', 'org', 'per', 'mis']:
                        if key in article and isinstance(article[key], dict):
                            entities.extend(article[key].keys())
                    # Count co-occurrences
                    for pair in combinations(entities, 2):
                        co_occurrence[pair] += 1

    # Filter entities by frequency
    top_entities = [kw for kw, count in combined_entities.items() if count >= min_frequency]
    top_entities = sorted(top_entities, key=combined_entities.get, reverse=True)[:top_n]

    # Create co-occurrence matrix
    entity_indices = {entity: idx for idx, entity in enumerate(top_entities)}
    matrix_size = len(top_entities)
    co_matrix = np.zeros((matrix_size, matrix_size))

    for (ent1, ent2), count in co_occurrence.items():
        if ent1 in entity_indices and ent2 in entity_indices:
            idx1, idx2 = entity_indices[ent1], entity_indices[ent2]
            co_matrix[idx1, idx2] += count
            co_matrix[idx2, idx1] += count  # Symmetric matrix

    # Perform PCA for dimensionality reduction
    pca = PCA(n_components=2)
    reduced_matrix = pca.fit_transform(co_matrix)

    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(co_matrix)

    # Prepare data for visualization
    df_clusters = pd.DataFrame(reduced_matrix, columns=["PC1", "PC2"])
    df_clusters["entity"] = top_entities
    df_clusters["cluster"] = clusters

    # Visualize clusters
    fig = px.scatter(
        df_clusters,
        x="PC1",
        y="PC2",
        color="cluster",
        text="entity",
        title="Entity Clusters",
        labels={"PC1": "Principal Component 1", "PC2": "Principal Component 2"}
    )
    fig.update_traces(textposition='top center')
    return fig
