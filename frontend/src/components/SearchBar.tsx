import React, { useState, useRef, KeyboardEvent } from 'react';
import { getAutocompleteSuggestions } from '../api';
import { AutocompleteSuggestion } from '../types';

interface SearchBarProps {
  trieInitialized: boolean;
}

const SearchBar: React.FC<SearchBarProps> = ({ trieInitialized }) => {
  const [query, setQuery] = useState<string>('');
  const [suggestion, setSuggestion] = useState<string>('');
  const [suggestions, setSuggestions] = useState<AutocompleteSuggestion[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  
  const searchInputRef = useRef<HTMLInputElement>(null);
  const debounceTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  // Handle input change with debounce
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setQuery(value);
    setSuggestion('');
    
    // Clear previous timer
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }
    
    // Don't search if query is empty
    if (!value.trim()) {
      setSuggestions([]);
      return;
    }
    
    // Set new timer
    debounceTimerRef.current = setTimeout(() => {
      fetchSuggestions(value);
    }, 300);
  };

  // Fetch suggestions from API
  const fetchSuggestions = async (searchQuery: string) => {
    if (!trieInitialized) {
      setError('Please initialize the data first (click "Load Data" button)');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await getAutocompleteSuggestions(searchQuery);
      
      if (response.status === 'error') {
        setError('Error fetching suggestions');
        setSuggestions([]);
      } else {
        setSuggestions(response.suggestions);
        
        // Show suggestion for top result
        if (response.suggestions.length > 0) {
          const topResult = response.suggestions[0].name;
          if (topResult.toLowerCase().startsWith(searchQuery.toLowerCase())) {
            setSuggestion(topResult);
          }
        }
      }
    } catch (err) {
      setError('Error fetching suggestions');
      setSuggestions([]);
    } finally {
      setLoading(false);
    }
  };

  // Handle suggestion selection
  const selectSuggestion = (suggestion: AutocompleteSuggestion) => {
    setQuery(suggestion.name);
    setSuggestion('');
    setSuggestions([]);
  };

  // Handle Tab key to complete suggestion
  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Tab' && suggestion) {
      e.preventDefault();
      setQuery(suggestion);
      setSuggestion('');
    }
  };

  return (
    <div className="container">
      <h2>Search Restaurants</h2>
      <div className="search-container">
        <input
          ref={searchInputRef}
          type="text"
          className="search-input"
          value={query}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder="Start typing a restaurant name..."
          autoComplete="off"
        />
        {suggestion && (
          <div className="suggestion">
            {suggestion}
          </div>
        )}
      </div>
      
      {loading && <div className="loading">Loading suggestions...</div>}
      
      {error && (
        <div className="status status-error">{error}</div>
      )}
      
      {!loading && !error && suggestions.length > 0 && (
        <div className="results">
          {suggestions.map((suggestion: AutocompleteSuggestion, index: number) => (
            <div 
              key={index} 
              className="result-item"
              onClick={() => selectSuggestion(suggestion)}
            >
              <div className="result-name">{suggestion.name}</div>
              <div className="result-rating">
                Rating count: {suggestion.rating_count}
              </div>
            </div>
          ))}
        </div>
      )}
      
      {!loading && !error && query && suggestions.length === 0 && (
        <div className="results">
          <div className="result-item">No results found</div>
        </div>
      )}
    </div>
  );
};

export default SearchBar;
