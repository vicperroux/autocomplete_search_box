"""
Data loading and processing functions for restaurant data
"""

import pandas as pd


def read_restaurants_txt(txt_file):
    """Read txt file and create a list of names
    
    Args:
        txt_file (str): Path to the CSV file with restaurant data
        
    Returns:
        list: List of restaurant names
    """
    return pd.read_csv(txt_file)["display_name"].to_list()


def join_results_with_user_rating_count(all_words_starting_w_prefix, data_path):
    """Extract subset of the restaurant names df with user rating count

    Args:
        all_words_starting_w_prefix (list): List of restaurant names matching the prefix
        data_path (str): Path to the CSV file with restaurant data

    Returns:
        DataFrame: Ordered results matching the prefix, sorted by user_rating_count
    """
    all_restaurants = pd.read_csv(data_path)

    # Filter restaurants that match our prefix results
    # Use .isin() method for filtering a list of values
    subset_with_prefix = all_restaurants[
        all_restaurants["display_name"].isin(all_words_starting_w_prefix)
    ]

    # Sort by user_rating_count in descending order
    ordered_results = subset_with_prefix.sort_values(
        by="user_rating_count", ascending=False
    )

    return ordered_results