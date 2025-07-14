"""
Data processing and preparation for the autocomplete service
"""

import pandas as pd
from backend.utils.text_utils import normalize_text


def prepare_names_and_user_ratings(data_path):
    """Extract columns name and user rating
    
    Args:
        data_path (str): Path to the CSV file with restaurant data
        
    Returns:
        DataFrame: DataFrame with normalized display names and user ratings
    """
    places_df = pd.read_csv(data_path).dropna(
        subset=["display_name", "user_rating_count"]
    )

    # Apply normalize_text to each value in the display_name column
    places_df["display_name"] = places_df["display_name"].apply(
        normalize_text
    )

    # Convert user_rating_count to integer
    places_df["user_rating_count"] = places_df["user_rating_count"].astype(int)

    return places_df


def save_processed_data(input_path, output_path):
    """Process the input data and save to output path
    
    Args:
        input_path (str): Path to the input CSV file
        output_path (str): Path to save the processed CSV file
    """
    processed_df = prepare_names_and_user_ratings(input_path)
    processed_df.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")


if __name__ == "__main__":
    # Example usage
    google_places_path = "data/detailed_google_maps_places_data.csv"
    output_path = "data/restaurants_names.csv"
    save_processed_data(google_places_path, output_path)
