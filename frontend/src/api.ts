import axios from "axios";
import {
  RestaurantListResponse,
  AutocompleteResponse,
  ApiResponse,
} from "./types";

const API_BASE_URL = "http://localhost:8000/api";

// Initialize the trie data structure
export const initializeTrie = async (): Promise<ApiResponse> => {
  try {
    const response = await axios.post<ApiResponse>(
      `${API_BASE_URL}/initialize`
    );
    return response.data;
  } catch (error) {
    console.error("Error initializing trie:", error);
    return { status: "error", message: "Failed to initialize data" };
  }
};

// Get autocomplete suggestions
export const getAutocompleteSuggestions = async (
  prefix: string,
  limit: number = 10
): Promise<AutocompleteResponse> => {
  try {
    const response = await axios.get<AutocompleteResponse>(
      `${API_BASE_URL}/autocomplete?prefix=${encodeURIComponent(
        prefix
      )}&limit=${limit}`
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching autocomplete suggestions:", error);
    return {
      query: prefix,
      suggestions: [],
      total_count: 0,
      status: "error",
    };
  }
};

// Get list of restaurants
export const getRestaurants = async (
  limit: number = 20,
  offset: number = 0
): Promise<RestaurantListResponse> => {
  try {
    const response = await axios.get<RestaurantListResponse>(
      `${API_BASE_URL}/restaurants?limit=${limit}&offset=${offset}`
    );
    return response.data;
  } catch (error) {
    console.error("Error fetching restaurants:", error);
    return { restaurants: [], total: 0, status: "error" };
  }
};

// Add a new restaurant
export const addRestaurant = async (
  name: string,
  rating: number = 0
): Promise<ApiResponse> => {
  try {
    const response = await axios.post<ApiResponse>(
      `${API_BASE_URL}/restaurants`,
      { name, rating }
    );
    return response.data;
  } catch (error) {
    console.error("Error adding restaurant:", error);
    return { status: "error", message: "Failed to add restaurant" };
  }
};
