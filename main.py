# Read data
def read_data(data_path):
    with open(data_path, "r") as file:
        data = file.read()
    return data


# Prepare data
def prepare_data(data):
    wiki_titles = data.split("\n")
    return wiki_titles


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


# Search prefix gives the words with a given prefix
list_words = ["prince of oman", "princess", "princeps"]

#

"""
# 3 possibles directions for the ranking of results / relevant results
# - most popular pages
# - most visited types of pages for a given user
# - coming from a given page -> most frequent transition for a user
"""


def main():
    pass


if __name__ == "__main__":
    data = read_data("wiki_titles.txt")
    prepared_data = prepare_data(data)

    # Initialize Trie and insert wiki titles
    trie = Trie()
    for title in prepared_data:
        trie.insert(
            title.lower()
        )  # Insert titles in lowercase for case-insensitive search

    # Example usage
    prefix = "prince"
    if trie.is_prefix(prefix):
        print(f"Words starting with '{prefix}': {trie.search_prefix(prefix)}")
    else:
        print(f"No words found with prefix '{prefix}'")
