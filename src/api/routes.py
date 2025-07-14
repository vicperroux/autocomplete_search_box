"""
FastAPI routes for autocomplete API
"""

from fastapi import APIRouter, Query, HTTPException, Body
from typing import Optional, Dict, Any, List
import pandas as pd
import os

from src.services.autocomplete_service import (
    get_autocomplete_results,
    format_autocomplete_response,
)
from src.services.trie_service import TrieService
from src.utils.text_utils import normalize_text

# Create router
router = APIRouter()

# Constants
DATA_PATH = "data/restaurants_names.csv"


@router.post("/initialize")
def initialize_trie() -> Dict[str, Any]:
    """Initialize the trie with restaurant data

    This endpoint should be called once before using the autocomplete endpoint.
    It builds the trie data structure with all restaurant names.

    Returns:
        Dict[str, Any]: Status of the initialization
    """
    trie_service = TrieService.get_instance()
    result = trie_service.build_trie()

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result


@router.get("/restaurants")
def list_restaurants(
    limit: int = Query(100, description="Maximum number of restaurants to return"),
    offset: int = Query(0, description="Number of restaurants to skip"),
) -> Dict[str, Any]:
    """Get a list of restaurant names

    Args:
        limit: Maximum number of restaurants to return
        offset: Number of restaurants to skip

    Returns:
        Dict with restaurants list and total count
    """
    try:
        # Check if file exists
        if not os.path.exists(DATA_PATH):
            return {"restaurants": [], "total": 0}

        # Read the CSV file
        df = pd.read_csv(DATA_PATH)

        # Get total count
        total = len(df)

        # Apply pagination
        df = df.iloc[offset : offset + limit]

        # Convert to list of dictionaries
        restaurants = df.to_dict(orient="records")

        return {"restaurants": restaurants, "total": total}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error reading restaurants: {str(e)}"
        )


@router.post("/restaurants")
def add_restaurant(
    name: str = Body(..., embed=True, description="Restaurant name to add"),
    rating: int = Body(0, embed=True, description="User rating count"),
) -> Dict[str, Any]:
    """Add a new restaurant name to the dataset

    Args:
        name: Restaurant name to add
        rating: User rating count

    Returns:
        Status of the operation
    """
    try:
        # Normalize the name
        normalized_name = normalize_text(name)

        # Create DataFrame for the new restaurant
        new_restaurant = pd.DataFrame(
            {"display_name": [normalized_name], "user_rating_count": [rating]}
        )

        # Check if file exists
        if os.path.exists(DATA_PATH):
            # Read existing data
            df = pd.read_csv(DATA_PATH)

            # Check if restaurant already exists
            if normalized_name in df["display_name"].values:
                return {"status": "error", "message": "Restaurant already exists"}

            # Append new restaurant
            df = pd.concat([df, new_restaurant], ignore_index=True)
        else:
            # Create new file with the restaurant
            df = new_restaurant

        # Save to CSV
        df.to_csv(DATA_PATH, index=False)

        # If trie is initialized, add the new restaurant to it
        trie_service = TrieService.get_instance()
        if trie_service.is_initialized():
            trie_service.trie.insert(normalized_name)

        return {"status": "success", "message": f"Added restaurant: {name}"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error adding restaurant: {str(e)}"
        )


@router.get("/autocomplete")
def api_autocomplete(
    prefix: str = Query(..., description="Prefix to search for"),
    limit: Optional[int] = Query(10, description="Maximum number of results to return"),
):
    """API endpoint function for autocomplete that returns JSON-serializable results

    Args:
        prefix (str): The prefix to search for
        limit (int, optional): Maximum number of results to return. Defaults to 10.

    Returns:
        dict: JSON-serializable dictionary with autocomplete results
        {
            "query": "prefix",
            "suggestions": [
                {
                    "name": "Restaurant Name",
                    "rating_count": 123,
                    "score": 0.95  # Normalized score based on rating count
                },
                ...
            ],
            "total_count": 15,  # Total number of matches before limit
            "status": "success"
        }
    """
    # Check if the trie has been initialized
    trie_service = TrieService.get_instance()
    if not trie_service.is_initialized():
        raise HTTPException(
            status_code=400,
            detail="Trie not initialized. Please call the /initialize endpoint first.",
        )

    # Get the ordered DataFrame of results
    results_df = get_autocomplete_results(prefix, limit)

    # Format the response
    response = format_autocomplete_response(prefix, results_df, limit)

    return response
