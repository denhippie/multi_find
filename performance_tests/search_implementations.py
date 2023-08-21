import abc
import re
import time

from multi_find.multi_find import MultiFind, SearchString


class Searcher(abc.ABC):
    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def search(self, source: str) -> list[str]:
        raise NotImplementedError


class BruteForce(Searcher):
    def __init__(self, search_words: list[str]) -> None:
        self.search_words = search_words

    def name(self) -> str:
        return 'Brute Force'

    def search(self, source: str) -> list[str]:
        found = []
        for word in self.search_words:
            if word in source:
                found.append(word)
        return found


class Regex(Searcher):
    def __init__(self, search_words: list[str]) -> None:
        start = time.time()
        pipes = '|'.join(search_words)
        self.regex = re.compile(f'({pipes})')
        print(f'Regex compiled in {time.time()-start}s')

    def name(self) -> str:
        return 'Regex'

    def search(self, source: str) -> list[str]:
        return re.findall(self.regex, source)


class Multi(Searcher):
    def __init__(self, search_words: list[str]) -> None:
        start = time.time()
        self.multi = MultiFind()
        for word in search_words:
            self.multi.add_search_string(SearchString(word))
        print(f'MultiFind index built in {time.time() - start}s')

    def name(self) -> str:
        return 'MultiFind'

    def search(self, source: str) -> list[str]:
        matches = self.multi.find_matches(source)
        return [m.match.search for m in matches]
