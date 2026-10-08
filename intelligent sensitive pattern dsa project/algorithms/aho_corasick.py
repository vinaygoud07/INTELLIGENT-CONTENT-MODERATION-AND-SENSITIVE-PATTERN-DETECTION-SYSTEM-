"""
Aho-Corasick Multi-Pattern Search Algorithm Implementation.

DSA Concept:
Aho-Corasick is a multi-pattern matching algorithm that constructs a Finite State Automaton
combining a Trie with failure links (similar to KMP's LPS concept applied to trees).

Key Structures:
1. Trie: Stores all patterns sharing common prefixes.
2. Failure Links (fail): Directs state transitions on character mismatch to the longest proper suffix
   that exists in the trie. Built using Breadth-First Search (BFS).
3. Output Links: Collects patterns that end at current state or reachable via failure links.

Time Complexity:
- Preprocessing (Trie + Automaton Construction): O(Sum of pattern lengths) = O(M_total)
- Search Phase: O(N + Z), where N = len(text), Z = total matches found.
- Enables single-pass scanning of text for thousands of sensitive patterns!

Space Complexity:
- O(M_total * Sigma) where Sigma is alphabet size.
"""

from collections import deque
from typing import List, Dict, Any, Tuple, Optional


class AhoCorasickNode:
    """Represents a single node state in the Aho-Corasick Trie."""

    def __init__(self, node_id: int, char: str = ""):
        self.id: int = node_id
        self.char: str = char
        self.children: Dict[str, 'AhoCorasickNode'] = {}
        self.fail: Optional['AhoCorasickNode'] = None
        self.output: List[Tuple[str, str]] = []  # List of (pattern, category) tuples


class AhoCorasick:
    """Aho-Corasick Multi-Pattern Automaton Manager."""

    def __init__(self):
        self.node_counter = 0
        self.root = AhoCorasickNode(node_id=0, char="root")
        self.built = False
        self.patterns: List[Tuple[str, str]] = []  # List of (pattern, category)

    def add_pattern(self, pattern: str, category: str = "General") -> None:
        """Inserts a pattern into the Trie."""
        if not pattern:
            return

        current = self.root
        for char in pattern:
            if char not in current.children:
                self.node_counter += 1
                current.children[char] = AhoCorasickNode(node_id=self.node_counter, char=char)
            current = current.children[char]

        current.output.append((pattern, category))
        self.patterns.append((pattern, category))
        self.built = False

    def build_automaton(self) -> None:
        """Constructs failure links and output links using BFS."""
        queue: deque = deque()

        # Depth 1 nodes: set fail pointer to root and enqueue
        for char, child in self.root.children.items():
            child.fail = self.root
            queue.append(child)

        # BFS for deeper nodes
        while queue:
            current: AhoCorasickNode = queue.popleft()

            for char, child in current.children.items():
                queue.append(child)

                # Fallback via failure links to find longest suffix match
                fail_node = current.fail
                while fail_node is not None and char not in fail_node.children:
                    fail_node = fail_node.fail

                if fail_node is None:
                    child.fail = self.root
                else:
                    child.fail = fail_node.children[char]
                    # Merge outputs from failure link node
                    child.output.extend(child.fail.output)

        self.built = True

    def search(self, text: str) -> Tuple[List[Dict[str, Any]], int]:
        """
        Scans text in a single pass to find all occurrences of added patterns.

        Args:
            text: Input string to search.

        Returns:
            Tuple containing:
            - matches (List[Dict]): List of match dicts with pattern, category, end_index, start_index.
            - total_comparisons (int): Total state transitions evaluated.
        """
        if not self.built:
            self.build_automaton()

        matches: List[Dict[str, Any]] = []
        current = self.root
        transitions = 0

        for i, char in enumerate(text):
            transitions += 1
            # Follow failure links if character transition does not exist
            while current is not None and char not in current.children:
                current = current.fail
                transitions += 1

            if current is None:
                current = self.root
                continue

            current = current.children[char]

            # Check for outputs at this state
            if current.output:
                for pattern, category in current.output:
                    start_idx = i - len(pattern) + 1
                    matches.append({
                        'pattern': pattern,
                        'category': category,
                        'start_index': start_idx,
                        'end_index': i,
                        'matched_text': text[start_idx:i + 1]
                    })

        return matches, transitions

    def get_trie_structure(self) -> Dict[str, Any]:
        """Exposes structure for Streamlit tree visualization."""
        nodes_info = []

        def traverse(node: AhoCorasickNode):
            fail_id = node.fail.id if node.fail else None
            nodes_info.append({
                'id': node.id,
                'char': node.char,
                'fail_id': fail_id,
                'outputs': [p for p, _ in node.output],
                'children': list(node.children.keys())
            })
            for child in node.children.values():
                traverse(child)

        traverse(self.root)
        return {
            'total_nodes': self.node_counter + 1,
            'total_patterns': len(self.patterns),
            'nodes': nodes_info
        }
