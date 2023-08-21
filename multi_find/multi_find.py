import dataclasses


@dataclasses.dataclass
class SearchString:
    """
    Instead of giving MultiFind a plain string, you give it this container class. This allows you to inherit from this
    class and add metadata to it which you can access when getting your search results.
    """
    search: str


@dataclasses.dataclass
class Match:
    match: SearchString  # The found search string
    index: int           # The index in the analyzed string where the match starts.


class MultiFind:
    class Node:
        """
        Every search string gets transformed into this data structure where every character of the string is a node,
        and this node has a pointer to the next node indexed by the character of the search string.
        Once the last characters is mapped, the next node will contain the "terminator" for this search string.
        By throwing all search strings in the same data structure, you can scan in the string you're processing from
        a certain index, and find all search strings that way. Do that len(string) times, and you get everything.
        """
        def __init__(self):
            self.next_char: dict[str, MultiFind.Node] = {}
            self.terminators: list[SearchString] = []

    def __init__(self):
        self.root = MultiFind.Node()

    def add_search_strings(self, search_strings: list[SearchString]) -> None:
        for search_string in search_strings:
            self.add_search_string(search_string)

    def add_search_string(self, search_string: SearchString) -> None:
        assert search_string.search, 'you cannot add empty search words'
        next_node = self.root
        for character in search_string.search:
            if character not in next_node.next_char:
                next_node.next_char[character] = MultiFind.Node()
            next_node = next_node.next_char[character]
        next_node.terminators.append(search_string)

    def find_matches(self, search: str) -> list[Match]:
        found = []
        for index in range(len(search)):
            found += self._find_at_start_of_string(search, index)
        return found

    def _find_at_start_of_string(self, search: str, start_index: int) -> list[Match]:
        found = []
        index = start_index
        node = self.root
        search_len = len(search)
        while index < search_len:
            next_char = search[index]
            if next_char not in node.next_char:
                break
            node = node.next_char[next_char]
            index += 1
            for matched_string in node.terminators:
                found.append(Match(match=matched_string, index=start_index))
        return found
