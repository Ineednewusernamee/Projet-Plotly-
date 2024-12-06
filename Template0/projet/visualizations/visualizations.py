import plotly.express as px
from itertools import combinations
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd
def create_treemap(df_keywords):
    """Generate a treemap of keywords."""
    df_top_keywords = df_keywords.sort_values(by="frequency", ascending=False).head(50)
    fig = px.treemap(
        df_top_keywords,
        path=["keyword"],
        values="frequency",
        title="Treemap of Top Keywords",
        labels={"frequency": "Frequency"}
    )
    return fig

def create_heatmap(daily_counts):
    """Generate a heatmap of daily article counts."""
    fig = px.density_heatmap(
        daily_counts,
        x="date",
        y="article_count",
        title="Daily Article Count Heatmap",
        labels={"date": "Date", "article_count": "Number of Articles"}
    )
    return fig 

def create_keyword_clusters(data):
    """Generate keyword clusters based on co-occurrence."""
    from itertools import combinations
    co_occurrence = {}
    unique_keywords = set()

    # Extract co-occurrence data
    for year, months in data['data'].items():
        for month, days in months.items():
            for day, articles in days.items():
                for article in articles:
                    if 'kws' in article and isinstance(article['kws'], dict):
                        kws = list(article['kws'].keys())
                        unique_keywords.update(kws)
                        for pair in combinations(kws, 2):
                            if pair not in co_occurrence:
                                co_occurrence[pair] = 0
                            co_occurrence[pair] += 1

    # Create co-occurrence matrix
    keywords_list = list(unique_keywords)
    matrix_size = len(keywords_list)
    co_matrix = np.zeros((matrix_size, matrix_size))
    keyword_to_idx = {keyword: idx for idx, keyword in enumerate(keywords_list)}

    for (kw1, kw2), count in co_occurrence.items():
        idx1, idx2 = keyword_to_idx[kw1], keyword_to_idx[kw2]
        co_matrix[idx1, idx2] = count
        co_matrix[idx2, idx1] = count  # Symmetric matrix

    # Debugging: Print matrix stats
    print("Co-occurrence Matrix Shape:", co_matrix.shape)
    print("Sample Co-occurrence Matrix:", co_matrix[:5, :5])

    # PCA for dimensionality reduction
    pca = PCA(n_components=2)
    reduced_matrix = pca.fit_transform(co_matrix)

    # Debugging: Check explained variance
    print("Explained Variance by PCA:", pca.explained_variance_ratio_)

    # K-Means Clustering
    kmeans = KMeans(n_clusters=5, random_state=42)
    clusters = kmeans.fit_predict(co_matrix)

    # Prepare DataFrame for visualization
    df_clusters = pd.DataFrame(reduced_matrix, columns=["PC1", "PC2"])
    df_clusters["keyword"] = keywords_list
    df_clusters["cluster"] = clusters

    # Debugging: Check cluster distribution
    print(df_clusters['cluster'].value_counts())

    # Visualize clusters
    fig = px.scatter(
        df_clusters,
        x="PC1",
        y="PC2",
        color="cluster",
        text="keyword",
        title="Keyword Clusters",
        labels={"PC1": "Principal Component 1", "PC2": "Principal Component 2"}
    )
    fig.show()