// Types for API responses and data structures

export interface Restaurant {
  display_name: string;
  user_rating_count: number;
}

export interface RestaurantListResponse {
  restaurants: Restaurant[];
  total: number;
  status: string;
}

export interface AutocompleteSuggestion {
  name: string;
  rating_count: number;
  score: number;
}

export interface AutocompleteResponse {
  query: string;
  suggestions: AutocompleteSuggestion[];
  total_count: number;
  status: string;
}

export interface ApiResponse {
  status: string;
  message?: string;
  count?: number;
}
