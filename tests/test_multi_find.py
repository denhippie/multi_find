import pytest

from multi_find.multi_find import MultiFind


@pytest.fixture
def mf() -> MultiFind:
    return MultiFind()


def test_empty_index(mf: MultiFind) -> None:
    assert not mf.find_words('bla bla, yada yada')
    assert not mf.find_words('')


def test_single_word_index(mf: MultiFind) -> None:
    mf.add_word('special')
    assert not mf.find_words('bla bla, yada yada')
    assert not mf.find_words('specia')
    assert not mf.find_words('')
    assert {'special'} == mf.find_words('special')
    assert {'special'} == mf.find_words('special at the start')
    assert {'special'} == mf.find_words('the end is special')
    assert {'special'} == mf.find_words('this is so special, it hurts')


def test_multi_word_index(mf: MultiFind) -> None:
    mf.add_words(['word', 'a full sentence', 'x'])
    assert not mf.find_words('bla bla, yada yada')
    assert {'word', 'a full sentence'} == mf.find_words('words make a full sentence')
    assert {'word', 'a full sentence'} == mf.find_words('a full sentence consists of words')
    assert {'word', 'x'} == mf.find_words('the character x can be in a word')
    assert {'word'} == mf.find_words('the character y can be in a word')


def test_multiple_occurrences(mf: MultiFind) -> None:
    mf.add_words(['word', 'a full sentence', 'x'])
    assert {'word'} == mf.find_words('word word word')
    assert {'word'} == mf.find_words('wordwordword')
    assert {'x'} == mf.find_words('x is x')
    assert {'x'} == mf.find_words('xxxxxxxx')


def test_overlapping_matches(mf: MultiFind) -> None:
    mf.add_words(['first match', 'match second', 'x'])
    assert {'first match', 'match second'} == mf.find_words('first match second')


def test_subset_match(mf: MultiFind) -> None:
    mf.add_words(['bird is the word', 'the'])
    assert {'bird is the word', 'the'} == mf.find_words('now you have "bird is the word" in your head')
