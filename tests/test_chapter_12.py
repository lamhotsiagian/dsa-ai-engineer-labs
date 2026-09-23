"""Unit tests for Chapter 12."""
from __future__ import annotations
from dsa_labs.chapter_12.vocab_trie import VocabularyTrie
from dsa_labs.chapter_12.leetcode_solutions import Trie, WordDictionary, find_words

def test_vocab_trie():
    vt = VocabularyTrie()
    vt.add("hello", token_id=1)
    assert vt.longest_match("hello world") == (5, 1)

def test_trie():
    trie = Trie()
    trie.insert("apple")
    assert trie.search("apple") is True
    assert trie.search("app") is False
    assert trie.startsWith("app") is True

def test_word_dictionary():
    wd = WordDictionary()
    wd.addWord("bad")
    wd.addWord("dad")
    assert wd.search("pad") is False
    assert wd.search("bad") is True
    assert wd.search(".ad") is True

def test_find_words():
    board = [["o","a","a","n"],["e","t","a","e"],["i","h","k","r"],["i","f","l","v"]]
    words = ["oath","pea","eat","rain"]
    res = sorted(find_words(board, words))
    assert res == ["eat", "oath"]
