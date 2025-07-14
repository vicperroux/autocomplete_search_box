import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import DataManagement from './components/DataManagement';

const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'search' | 'manage'>('search');
  const [trieInitialized, setTrieInitialized] = useState<boolean>(false);

  return (
    <div className="app">
      <h1>Autocomplete search box</h1>
      
      <div className="tabs">
        <div 
          className={`tab ${activeTab === 'search' ? 'active' : ''}`}
          onClick={() => setActiveTab('search')}
        >
          Search
        </div>
        <div 
          className={`tab ${activeTab === 'manage' ? 'active' : ''}`}
          onClick={() => setActiveTab('manage')}
        >
          Manage Data
        </div>
      </div>
      
      <div className={`tab-content ${activeTab === 'search' ? 'active' : ''}`}>
        <SearchBar trieInitialized={trieInitialized} />
      </div>
      
      <div className={`tab-content ${activeTab === 'manage' ? 'active' : ''}`}>
        <DataManagement 
          trieInitialized={trieInitialized}
          setTrieInitialized={setTrieInitialized}
        />
      </div>
    </div>
  );
};

export default App;
