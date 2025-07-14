"""
Autocomplete service implementation
"""

import pandas as pd
from src.data.data_loader import join_results_with_user_rating_count
from src.services.trie_service import TrieService


def get_autocomplete_results(prefix, limit=10):
    """Main function that performs autocomplete search and returns ordered results

    Args:
        prefix (str): The prefix to search for
        limit (int, optional): Maximum number of results to return. Defaults to 10.

    Returns:
        DataFrame: Ordered results matching the prefix
    """
    # Get the singleton instance of TrieService
    trie_service = TrieService.get_instance()
    
    # Check if the trie is initialized
    if not trie_service.is_initialized():
        # If not initialized, return empty results
        return pd.DataFrame()
    
    data_path = "data/restaurants_names.csv"
    
    # Get all words starting with the prefix using the existing trie
    all_words_starting_w_prefix = trie_service.search_prefix(prefix)

    # Join with user ratings and order results
    ordered_list = join_results_with_user_rating_count(
        all_words_starting_w_prefix, data_path
    )

    # Apply limit if specified
    if limit > 0:
        ordered_list = ordered_list.head(limit)

    return ordered_list


def format_autocomplete_response(prefix, results_df, limit=10):
    """Format autocomplete results as a JSON-serializable dictionary

    Args:
        prefix (str): The prefix that was searched for
        results_df (DataFrame): DataFrame with autocomplete results
        limit (int, optional): Maximum number of results. Defaults to 10.

    Returns:
        dict: JSON-serializable dictionary with autocomplete results
    """
    # Calculate total count before applying limit
    total_count = len(results_df)
    
    # Calculate max rating for normalization
    max_rating = results_df["user_rating_count"].max() if not results_df.empty else 1
    
    # Build suggestions list
    suggestions = []
    for _, row in results_df.iterrows():
        # Normalize score between 0 and 1
        score = row["user_rating_count"] / max_rating if max_rating > 0 else 0
        
        suggestions.append({
            "name": row["display_name"],
            "rating_count": int(row["user_rating_count"]),
            "score": round(score, 2)
        })
    
    # Build response
    response = {
        "query": prefix,
        "suggestions": suggestions,
        "total_count": total_count,
        "status": "success"
    }
    
    return response
