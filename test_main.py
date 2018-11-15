"""
Unit tests for main.py

"""
import pytest
import main

# @pytest.mark.skipif(sys.version_info < (3,0) ,reason = 'Not tested to run on python versions < 3.0')
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
