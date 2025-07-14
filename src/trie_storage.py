import pandas as pd


# Autocomplete class using Trie data structure
class TrieNode:
    def __init__(self):
        self.children = {}  # Use dictionary instead of fixed array
        self.isLeaf = False


# Autocomplete class using Trie data structure
class Trie:
    def __init__(self):
        self.root = TrieNode()

    # Method to insert a key into the Trie
    def insert(self, key):
        curr = self.root
        for c in key:
            if c not in curr.children:
                curr.children[c] = TrieNode()
            curr = curr.children[c]
        curr.isLeaf = True

    # Method to search for words with a given prefix
    def search_prefix(self, prefix):
        """
        Returns a list of all words in the Trie that start with the given prefix.

        Args:
            prefix (str): The prefix to search for

        Returns:
            list: List of complete words starting with the prefix
        """
        # First, navigate to the end of the prefix
        curr = self.root
        for c in prefix:
            if c not in curr.children:
                return []  # Prefix not found
            curr = curr.children[c]

        # Now collect all words starting from this node
        words = []
        self._collect_words(curr, prefix, words)
        return words

    def is_prefix(self, prefix):
        """
        Check if the given string is a valid prefix in the Trie.
        A prefix is valid if there exists at least one word in the Trie that starts with it.

        Args:
            prefix (str): The prefix to check

        Returns:
            bool: True if the prefix exists in the Trie, False otherwise
        """
        curr = self.root
        for c in prefix:
            if c not in curr.children:
                return False
            curr = curr.children[c]
        return True

    def _collect_words(self, node, current_word, words):
        """
        Helper method to recursively collect all words from a given node.

        Args:
            node (TrieNode): Current node in the Trie
            current_word (str): Word built so far
            words (list): List to store found words
        """
        # If this node marks the end of a word, add it to results
        if node.isLeaf:
            words.append(current_word)

        # Recursively check all children
        for char in node.children:
            self._collect_words(node.children[char], current_word + char, words)


# Read restaurants txt
def read_restaurants_txt(txt_file):
    """Read txt file and create a list of names"""
    return pd.read_csv(txt_file)["display_name"].to_list()


def insert_all_names(list_names):
    """Insert all names from the list in the trie"""
    for restaurant in list_names:
        trie.insert(restaurant)


def join_results_with_user_rating_count(all_words_starting_w_prefix, data_path):
    """Extract subset of the restaurant names df with user rating count

    Args:
        all_words_starting_w_prefix (list): List of restaurant names matching the prefix
        data_path (str): Path to the CSV file with restaurant data

    Returns:
        DataFrame: Ordered results matching the prefix, sorted by user_rating_count
    """
    all_restaurants = pd.read_csv(data_path)

    # Filter restaurants that match our prefix results
    # Use .isin() method for filtering a list of values
    subset_with_prefix = all_restaurants[
        all_restaurants["display_name"].isin(all_words_starting_w_prefix)
    ]

    # Sort by user_rating_count in descending order
    ordered_results = subset_with_prefix.sort_values(
        by="user_rating_count", ascending=False
    )

    return ordered_results


def main(data_path, query):
    """Main function that performs autocomplete search and returns ordered results

    Args:
        data_path (str): Path to the CSV file with restaurant data
        query (str): The prefix to search for

    Returns:
        DataFrame: Ordered results matching the prefix
    """
    # Create a new trie for this search
    trie = Trie()

    # Get restaurant names and build the trie
    list_names = read_restaurants_txt(data_path)
    for name in list_names:
        trie.insert(name)

    # Get all words starting with the prefix
    all_words_starting_w_prefix = trie.search_prefix(query)

    # Join with user ratings and order results
    ordered_list = join_results_with_user_rating_count(
        all_words_starting_w_prefix, data_path
    )

    return ordered_list


if __name__ == "__main__":
    import argparse

    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="Restaurant name autocomplete search")
    parser.add_argument(
        "--data",
        type=str,
        default="data/restaurants_names.csv",
        help="Path to the CSV file with restaurant data",
    )
    parser.add_argument("--query", type=str, default="the", help="Prefix to search for")

    args = parser.parse_args()

    # Call the main function with parsed arguments
    results = main(args.data, args.query)

    # Display results
    if len(results) > 0:
        print(f"Found {len(results)} matches for prefix '{args.query}':\n")
        print(results.head(10))
    else:
        print(f"No matches found for prefix '{args.query}'")
