import React, { useState, useEffect } from 'react';
import { initializeTrie, getRestaurants, addRestaurant } from '../api';
import { Restaurant, RestaurantListResponse, ApiResponse } from '../types';

interface DataManagementProps {
  trieInitialized: boolean;
  setTrieInitialized: (initialized: boolean) => void;
}

const DataManagement: React.FC<DataManagementProps> = ({ 
  trieInitialized, 
  setTrieInitialized 
}) => {
  // State for restaurant list
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [totalRestaurants, setTotalRestaurants] = useState<number>(0);
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [pageSize] = useState<number>(20);
  const [loading, setLoading] = useState<boolean>(false);
  const [loadingStatus, setLoadingStatus] = useState<string | null>(null);
  
  // State for adding new restaurant
  const [newRestaurantName, setNewRestaurantName] = useState<string>('');
  const [newRestaurantRating, setNewRestaurantRating] = useState<number>(0);
  const [addStatus, setAddStatus] = useState<string | null>(null);
  
  // Load restaurant list
  const loadRestaurantList = async () => {
    setLoading(true);
    try {
      const response: RestaurantListResponse = await getRestaurants(pageSize, (currentPage - 1) * pageSize);
      setRestaurants(response.restaurants);
      setTotalRestaurants(response.total);
    } catch (error) {
      console.error('Error loading restaurants:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Initialize trie
  const handleInitializeTrie = async () => {
    setLoadingStatus('Initializing data...');
    try {
      const response: ApiResponse = await initializeTrie();
      if (response.status === 'success') {
        setLoadingStatus(`Success! Loaded ${response.count} restaurant names.`);
        setTrieInitialized(true);
      } else {
        setLoadingStatus(`Error: ${response.message}`);
      }
    } catch (error) {
      setLoadingStatus('Error initializing data');
      console.error('Error initializing trie:', error);
    }
  };
  
  // Add new restaurant
  const handleAddRestaurant = async () => {
    if (!newRestaurantName.trim()) {
      setAddStatus('Please enter a restaurant name');
      return;
    }
    
    setAddStatus('Adding restaurant...');
    try {
      const response: ApiResponse = await addRestaurant(newRestaurantName, newRestaurantRating);
      if (response.status === 'success') {
        setAddStatus(response.message || 'Restaurant added successfully');
        setNewRestaurantName('');
        setNewRestaurantRating(0);
        loadRestaurantList(); // Refresh the list
      } else {
        setAddStatus(`Error: ${response.message}`);
      }
    } catch (error) {
      setAddStatus('Error adding restaurant');
      console.error('Error adding restaurant:', error);
    }
  };
  
  // Pagination
  const totalPages = Math.ceil(totalRestaurants / pageSize);
  
  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };
  
  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };
  
  // Load restaurants when page changes
  useEffect(() => {
    loadRestaurantList();
  }, [currentPage]);
  
  return (
    <>
      <div className="container">
        <h2>Load Data</h2>
        <p>Initialize the autocomplete system by loading restaurant data into memory.</p>
        <button onClick={handleInitializeTrie}>
          Load Data
        </button>
        {loadingStatus && (
          <div className={`status ${loadingStatus.includes('Success') ? 'status-success' : 'status-error'}`}>
            {loadingStatus}
          </div>
        )}
      </div>
      
      <div className="container">
        <h2>Add New Restaurant</h2>
        <div className="form-group">
          <label htmlFor="restaurant-name">Restaurant Name:</label>
          <input
            type="text"
            id="restaurant-name"
            value={newRestaurantName}
            onChange={(e) => setNewRestaurantName(e.target.value)}
            placeholder="Enter restaurant name"
          />
        </div>
        <div className="form-group">
          <label htmlFor="rating-count">Rating Count:</label>
          <input
            type="number"
            id="rating-count"
            value={newRestaurantRating}
            onChange={(e) => setNewRestaurantRating(parseInt(e.target.value) || 0)}
            min="0"
          />
        </div>
        <button 
          className="secondary"
          onClick={handleAddRestaurant}
        >
          Add Restaurant
        </button>
        {addStatus && (
          <div className={`status ${addStatus.includes('successfully') || addStatus.includes('added') ? 'status-success' : 'status-error'}`}>
            {addStatus}
          </div>
        )}
      </div>
      
      <div className="container">
        <h2>Restaurant List</h2>
        <button 
          className="secondary"
          onClick={() => {
            setCurrentPage(1);
            loadRestaurantList();
          }}
        >
          Refresh List
        </button>
        
        {loading ? (
          <div className="loading">Loading restaurants...</div>
        ) : (
          <>
            <div className="results">
              {restaurants.length === 0 ? (
                <div className="result-item">No restaurants found</div>
              ) : (
                restaurants.map((restaurant: Restaurant, index: number) => (
                  <div key={index} className="result-item">
                    <div className="result-name">{restaurant.display_name}</div>
                    <div className="result-rating">Rating count: {restaurant.user_rating_count}</div>
                  </div>
                ))
              )}
            </div>
            
            <div className="pagination">
              <button 
                onClick={handlePrevPage} 
                disabled={currentPage <= 1}
              >
                Previous
              </button>
              <span>Page {currentPage} of {totalPages || 1}</span>
              <button 
                onClick={handleNextPage} 
                disabled={currentPage >= totalPages}
              >
                Next
              </button>
            </div>
          </>
        )}
      </div>
    </>
  );
};

export default DataManagement;
