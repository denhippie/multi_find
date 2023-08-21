
class MultiFind:
    class Node:
        def __init__(self):
            self.next_char: dict[str, MultiFind.Node] = {}
            self.terminator = False

    def __init__(self):
        self.root = MultiFind.Node()

    def add_words(self, words: list[str]) -> None:
        for word in words:
            self.add_word(word)

    def add_word(self, word: str) -> None:
        next_node = self.root
        for character in word:
            if character not in next_node.next_char:
                next_node.next_char[character] = MultiFind.Node()
            next_node = next_node.next_char[character]
        next_node.terminator = True

    def find_words(self, search: str) -> set[str]:
        found = []
        for index in range(len(search)):
            found += self._find_at_start_of_string(search, index)
        return {search[match[0]:match[1]] for match in found}

    def _find_at_start_of_string(self, search: str, start_index: int) -> list[tuple[int, int]]:
        found = []
        index = start_index
        node = self.root
        search_len = len(search)
        while index < search_len:
            if search[index] not in node.next_char:
                break
            node = node.next_char[search[index]]
            index += 1
            if node.terminator:
                found.append((start_index, index))
        return found
