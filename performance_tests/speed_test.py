import random
import string
import time

from .search_implementations import Searcher, BruteForce, Regex, Multi


def speed_test() -> None:
    search = mock_search_strings()
    bf = BruteForce(list(search))
    rex = Regex(list(search))
    mul = Multi(list(search))
    searchers: list[Searcher] = [
        bf,
        rex,
        mul
    ]
    timings: dict[str, float] = {}
    for searcher in searchers:
        start = time.time()
        searches = 1000
        for i in range(searches):
            source = ''.join(random.choices(string.ascii_lowercase, k=250))
            searcher.search(source)
        time_taken = time.time() - start
        timings[searcher.name()] = time_taken
        print(f'{searcher.name()} {searches} queries in {time_taken}s')
    speedup = timings['Brute Force'] / timings['MultiFind']
    print(f'MultiFind speedup: {speedup:.2f}x')


def mock_search_strings() -> set[str]:
    return {mock_string() for i in range(10000)}


def mock_string() -> str:
    characters = random.randint(3, 25)
    return ''.join(random.choices(string.ascii_lowercase, k=characters))
