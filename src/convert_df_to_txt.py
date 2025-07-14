import pandas as pd

google_places_path = "data/detailed_google_maps_places_data.csv"


def normalize_text(text):
    """Normalize text by standardizing apostrophes and other characters"""
    if not isinstance(text, str):
        return text

    # Replace various apostrophe types with a standard apostrophe
    apostrophe_variants = ["'", "`", "´", "′", "’"]
    normalized = text.lower()
    for variant in apostrophe_variants:
        normalized = normalized.replace(variant, "'")

    return normalized


def prepare_names_and_user_ratings(data_path):
    """Extract columns name and user rating"""
    google_places_df = pd.read_csv(data_path).dropna(
        subset=["display_name", "user_rating_count"]
    )

    # Apply normalize_text to each value in the display_name column
    google_places_df["display_name"] = google_places_df["display_name"].apply(
        normalize_text
    )

    # Convert user_rating_count to integer
    google_places_df["user_rating_count"] = google_places_df[
        "user_rating_count"
    ].astype(int)

    # Group by display_name and sum the ratings
    google_places_df = google_places_df.groupby("display_name").sum().reset_index()

    return google_places_df[["display_name", "user_rating_count"]]


# Example usage
if __name__ == "__main__":
    google_places_path = "data/detailed_google_maps_places_data.csv"
    subset_prepared = prepare_names_and_user_ratings(google_places_path)
    print(subset_prepared)
    subset_prepared.to_csv("data/restaurants_names.csv", index=False)
    print("Subset successfully saved")
