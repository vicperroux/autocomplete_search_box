"""
Trie data structure for efficient prefix-based search
"""

class TrieNode:
    def __init__(self):
        self.children = {}  # Use dictionary instead of fixed array
        self.isLeaf = False


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
