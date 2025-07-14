"""
Service for managing the Trie data structure as a singleton
"""

from backend.models.trie import Trie
from backend.data.data_loader import read_restaurants_txt
from backend.utils.text_utils import normalize_text


class TrieService:
    """Singleton service for managing the Trie data structure"""
    
    _instance = None
    _is_initialized = False
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of the TrieService
        
        Returns:
            TrieService: The singleton instance
        """
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """Initialize the TrieService with an empty trie"""
        self.trie = Trie()
        self.data_path = "data/restaurants_names.csv"
    
    def build_trie(self):
        """Build the trie from the restaurant data
        
        Returns:
            dict: Status of the operation
        """
        try:
            # Get restaurant names and build the trie
            list_names = read_restaurants_txt(self.data_path)
            
            # Reset the trie
            self.trie = Trie()
            
            # Insert all names
            for name in list_names:
                # Normalize the text before inserting into the trie
                normalized_name = normalize_text(name)
                self.trie.insert(normalized_name)
            
            TrieService._is_initialized = True
            return {
                "status": "success",
                "message": f"Trie built successfully with {len(list_names)} entries"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to build trie: {str(e)}"
            }
    
    def is_initialized(self):
        """Check if the trie has been initialized
        
        Returns:
            bool: True if initialized, False otherwise
        """
        return TrieService._is_initialized
    
    def search_prefix(self, prefix):
        """Search for words with the given prefix
        
        Args:
            prefix (str): The prefix to search for
            
        Returns:
            list: List of words matching the prefix
        """
        if not self.is_initialized():
            return []
        
        # Normalize the prefix before searching
        normalized_prefix = normalize_text(prefix)
        return self.trie.search_prefix(normalized_prefix)
