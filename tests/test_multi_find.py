import pytest

from multi_find.multi_find import MultiFind, SearchString, Match


@pytest.fixture
def mf() -> MultiFind:
    return MultiFind()


def test_empty_index(mf: MultiFind) -> None:
    assert not mf.find_matches('bla bla, yada yada')
    assert not mf.find_matches('')


def test_single_word_index(mf: MultiFind) -> None:
    mf.add_search_string(SearchString('special'))
    assert not mf.find_matches('bla bla, yada yada')
    assert not mf.find_matches('specia')
    assert not mf.find_matches('')
    assert [Match(SearchString('special'), 0)] == mf.find_matches('special')
    assert [Match(SearchString('special'), 0)] == mf.find_matches('special at the start')
    assert [Match(SearchString('special'), 11)] == mf.find_matches('the end is special')
    assert [Match(SearchString('special'), 11)] == mf.find_matches('this is so special, it hurts')


def test_multi_word_index(mf: MultiFind) -> None:
    mf.add_search_strings([SearchString('word'), SearchString('a full sentence'), SearchString('x')])
    assert not mf.find_matches('bla bla, yada yada')
    assert mf.find_matches('words make a full sentence') == [
        Match(SearchString('word'), 0),
        Match(SearchString('a full sentence'), 11),
    ]
    assert mf.find_matches('a full sentence consists of words') == [
        Match(SearchString('a full sentence'), 0),
        Match(SearchString('word'), 28),
    ]
    assert mf.find_matches('the character x can be in a word') == [
        Match(SearchString('x'), 14),
        Match(SearchString('word'), 28),
    ]
    assert mf.find_matches('the character y can be in a word') == [
        Match(SearchString('word'), 28)
    ]


def test_multiple_occurrences(mf: MultiFind) -> None:
    mf.add_search_strings([SearchString('word'), SearchString('a full sentence'), SearchString('x')])
    assert mf.find_matches('word word word') == [
        Match(SearchString('word'), 0),
        Match(SearchString('word'), 5),
        Match(SearchString('word'), 10),
    ]
    assert mf.find_matches('wordwordword') == [
        Match(SearchString('word'), 0),
        Match(SearchString('word'), 4),
        Match(SearchString('word'), 8),
    ]
    assert mf.find_matches('x is x') == [
        Match(SearchString('x'), 0),
        Match(SearchString('x'), 5),
    ]
    assert mf.find_matches('xxxxxxx') == [
        Match(SearchString('x'), 0),
        Match(SearchString('x'), 1),
        Match(SearchString('x'), 2),
        Match(SearchString('x'), 3),
        Match(SearchString('x'), 4),
        Match(SearchString('x'), 5),
        Match(SearchString('x'), 6),
    ]


def test_overlapping_matches(mf: MultiFind) -> None:
    mf.add_search_strings([SearchString('first match'), SearchString('match second'), SearchString('x')])
    assert mf.find_matches('first match second') == [
        Match(SearchString('first match'), 0),
        Match(SearchString('match second'), 6),
    ]


def test_subset_match(mf: MultiFind) -> None:
    mf.add_search_strings([SearchString('bird is the word'), SearchString('the')])
    assert mf.find_matches('now you have "bird is the word" in your head') == [
        Match(SearchString('bird is the word'), 14),
        Match(SearchString('the'), 22),
    ]
