"""
Unit tests for main.py
Run with:
python -m pytest -v
"""

import pytest
import main

DEFAULT = 1 #1/0 :Symspell spell-checker/Enchant spell-checker

def test_pre_processing_tokens():
    case, _, dummy, token_case = main.pre_processing('I love to eat apples')
    expected = ['i', 'love', 'to', 'eat', 'apples']
    assert case == expected


def test_pre_processing_postags():
    _, case, dummy, token_case = main.pre_processing('I love to eat apples')
    expected = ['PRON', 'VERB', 'PART', 'VERB', 'NOUN']
    assert case == expected


def test_pre_processing_tokenpostags():
    _, dummy, case, token_case = main.pre_processing('I love to eat apples')
    expected = [('i', 'PRON'), ('love', 'VERB'), ('to', 'PART'), ('eat', 'VERB'),('apples', 'NOUN')]
    assert case == expected


def test_pre_processing_notstring():
    case = main.pre_processing(['I love to eat apples'])
    expected = 405
    assert case == expected


def test_pre_processing_emptystring():
    case = main.pre_processing('')
    expected = 402
    assert case == expected

def test_pre_processing_maxinputlength():
    case = main.pre_processing('And when the broken hearted people living in the world agree,\
There will be an answer let it be,\
For though they may be parted there is still a chance that they will see,\
There will be an answer let it be,\
Let it be let it be let it be let it be,\
There will be an answer let it be,\
Let it be let it be let it be let it be,\
Whisper words of wisdom let it be,\
Let it be let it be let it be let it be,\
Whisper words of wisdom let it be')
    expected = 408
    assert case == expected


if DEFAULT:
    def test_symspell_test_suggestions():
        # Example : Boxer and the dog cn't jump over the fenc
        case, _ = main.symspell_test(
        [('Boxer', 'PROPN'), ('and', 'CCONJ'), ('the', 'DET'), ('dog', 'NOUN'),
         ("cn't", 'VERB'), ('jump', 'VERB'), ('over', 'ADP'), ('the', 'DET'),
          ('fenc', 'NOUN')]
        )
        expected = ['Boxer', 'and', 'the', 'dog', "can't", 'jump', 'over', 'the', 'fence']
        assert case == expected


    def test_symspell_test_intactwords():
        # Example : Boxer and the dog cn't jump over the fenc
        _, case = main.symspell_test(
        [('Boxer', 'PROPN'), ('and', 'CCONJ'), ('the', 'DET'), ('dog', 'NOUN'),
         ("cn't", 'VERB'), ('jump', 'VERB'), ('over', 'ADP'), ('the', 'DET'),
          ('fenc', 'NOUN')]
        )
        expected = ['Boxer']
        assert case == expected


    def test_symspell_test_notlistoftups():
        case = main.symspell_test("Boxer and the dog cn't jump over the fenc")
        expected = 410
        assert case == expected


else:
    def test_enchant_check_suggestions():
        case,_ = main.enchant_check(
        [('Boxer', 'PROPN'), ('and', 'CCONJ'), ('the', 'DET'), ('dog', 'NOUN'),
         ("cn't", 'VERB'), ('jump', 'VERB'), ('over', 'ADP'), ('the', 'DET'),
          ('fenc', 'NOUN')]
        )
        expected = ['Boxer', 'and', 'the', 'dog', "can't", 'jump', 'over', 'the', 'enc']
        assert case == expected


    def test_enchant_check_notlistoftups():
        # Example : Boxer and the dog cn't jump over the fenc
        case = main.enchant_check("Boxer and the dog cn't jump over the fenc")
        expected = 410
        assert case == expected


#Integration testing
def test_pre_processing_symspell_test_strinput():
    tokens,postags,toktags,tokcase = main.pre_processing('Robert sems to be extraordinry')
    case, _ = main.symspell_test(toktags)
    expected = ['robert','seems','to','be','extraordinary']
    assert case == expected


def test_post_processing():
    # tokens,postags,toktags,tokcase = main.pre_processing('Robert sems to be extraordinry')
    # sugg, intact = main.symspell_test(toktags)
    case = main.post_processing('Robert sems to be extraordinry')
    expected = [{"token":'Robert',"pos":'NOUN', "raw":'Robert'},
    {"token":'seems',"pos":'VERB', "raw":'sems'},
    {"token":'to',"pos":'PART', "raw":'to'},
    {"token":'be',"pos":'VERB', "raw":'be'},
    {"token":'extraordinary',"pos":'ADJ', "raw":'extraordinry'}]
    assert case == expected
