from wordcloud import WordCloud
import matplotlib.pyplot as plt

def create_and_save_word_cloud(entity_dict, output_path="./assets/wordcloud.png", title="Word Cloud"):
    """
    Generate and save a word cloud for the given dictionary of entities.

    Parameters:
    - entity_dict: Dictionary of word frequencies (e.g., {"word": frequency}).
    - output_path: Path to save the word cloud image.
    - title: Title for the word cloud plot (optional).
    """
    # Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(entity_dict)
    
    # Save the word cloud to a file
    wordcloud.to_file(output_path)
    print(f"Word cloud saved to {output_path}")