"""
The purpose of this code is to analyze different spell-checking
solutions available and compare them side-by-side.
"""

import json
import os
from pprint import pprint
import spacy
from spellchecker import SpellChecker
from symspellpy.symspellpy import SymSpell, Verbosity
from textblob import TextBlob

nlp = spacy.load('en_core_web_sm')
test_sentence = "I love to eat appl"

#Sentence pre-processing
def pre_processing(test_sentence):

    """
    The operations that are done here are :
       ** tokenising
       ** pos_tagging
       ** (token, pos_tag) generation.
    """

    try:
        doc = nlp(test_sentence)
        tokens = [token.text for token in doc] #Tokenise
        pos_tags = [token.pos_ for token in doc] #POS tags
        token_tags = list(zip(tokens, pos_tags))

        print('\nThe test sentence is : {} \n'.format(test_sentence))
        print(f'The tokenized form of the sentence is as follows : \n{tokens}')
        print(f'The Part of Speech (POS) tags of the sentence are as follows : \n{pos_tags}')
        print('The (token,pos_tag) tuples are : {}'.format(token_tags))
        return tokens, pos_tags, token_tags
    except TypeError as error:
        print(f'Invalid string : {error}')
        return 405


#using SpellChecker library in python
def spellchecker_test(list_tokens, token_tags):

    """This is a function to test the SpellChecker library for spell-checking performance."""
    print('\n{} \nBegin \'SpellChecker\' testing \n'.format('#'*20))

    try:
        spell = SpellChecker()
        # find those words that may be misspelled
        misspelled = spell.unknown(list_tokens)

        for word in misspelled:
            #print the incorrect word
            print(f'\nThe incorrect word is "{word}"')
            # Get the one `most likely` answer
            print(f'Using Spellchecker, the correction is : {spell.correction(word)}')
        return 0
    except TypeError as error:
        print(f'Invalid string : {error}')
        return 405


# Using textblob library in Python
def textblob_test(sentence):

    """This is a function that tests the TextBlob library for spell-checking performance."""
    print('\n{} \nBegin \'textblob\' testing \n'.format('#'*20))
    try:
        text = TextBlob(sentence)
        print('The attempted correction by "Textblob" is : {}'.format(text.correct()))
        return text.correct()
    except TypeError as error:
        print(f'Invalid type : {error}')
        return 405

#Using symspellpy library in python
def symspell_test(tokenpos_list, max_edit_distance_lookup=3,
                initial_capacity=83000, max_edit_distance_dictionary=3,
                prefix_length=7, term_index=0, count_index=1):

    """
    This is a function that tests the SymSpell library for spell-checking performance.
    Key-word arguments are:
        ** max_edit_distance_lookup : (Recommended maximum = 3)
        ** term_index : term column in dictionary (0)
        ** count_index : frequency column in dictionary (1)
    """
    print('\n{} \nBegin \'Symspellpy\' testing \n'.format('#'*20))

    try:
        sym_spell = SymSpell(initial_capacity, max_edit_distance_dictionary,
                             prefix_length)
        suggestion_verbosity = Verbosity.CLOSEST

        dictionary_path = os.path.join(os.path.dirname(__file__),
                                       "frequency_dictionary_en_82_765.txt")
        if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
            print("Dictionary file not found")
            return 'Error loading dictionary file'
        suggestion_list = []
        proper_noun = []

        for (word, pos) in tokenpos_list:
            if pos == 'PROPN':
                suggestion_list.append(word)
                proper_noun.append(word)
            elif len(word) < 3:
                suggestion_list.append(word)
                proper_noun.append(word)
            else:
                suggestions = sym_spell.lookup(word, suggestion_verbosity, max_edit_distance_lookup)
                suggestion = (list(suggestions))[0]
                # display suggestion term, term frequency, and edit distance
                print("input_term = {}, suggestion_term = {}, suggestion_count = {},\
                suggestion_distance =  {}".format(word, suggestion.term, suggestion.count, suggestion.distance))
                suggestion_list.append(suggestion.term)
        print("\n\nThe corrected sentence is : {}".format(' '.join(suggestion_list)))
        print(suggestion_list)
        print(proper_noun)
        return suggestion_list, proper_noun
    except TypeError as error:
        print(f'Invalid type : {error}')
        return 405


def main():
    """Main code"""

    tokens, pos_tags, token_tags = pre_processing(test_sentence)
    sym_result, proper_noun_list = symspell_test(token_tags)

    #Generating json format
    print('\n{} \nGenerating json format using \'Symspellpy\' results \n'.format('#'*20))

    corrected_sent = ' '.join(sym_result)
    #modifying original list of tokens to add possible repetitions
    correct_token_list = [(word, index) for (index, word) in enumerate(sym_result) if word != test_sentence.lower().split()[index] and word not in proper_noun_list]
    print('The corrected tokens along with their original indices are : {}\n'.format(correct_token_list))

    test_sentence_copy = test_sentence.split()
    offset = 0 #Offset inorder to account for shift in index after possible duplication of original incorrect tokens
    for (word, index) in correct_token_list:
        num_parts = len(nlp(word))
        test_sentence_copy[index+offset : index+offset+1] = test_sentence_copy[index+offset : index+offset+1] * num_parts
        offset += num_parts-1
    print('The modified version of the original token list is : {} \n'.format(test_sentence_copy))

    #tokenising the corrected sentence and generating pos tags
    new_sent = nlp(corrected_sent)
    new_sent_tokens = [w.text for w in new_sent]
    print("New sentence tokens are : {} \n".format(new_sent_tokens))
    new_pos_tags = [w.pos_ for w in new_sent]

    json_list = []
    for i,_ in enumerate(new_sent_tokens):
        json_list.append({"token":new_sent_tokens[i], "pos":new_pos_tags[i], "raw":test_sentence_copy[i]})

    json_list = json.dumps(json_list)
    json_dict = {"tokens" : json_list}
    pprint('The desired json output format is : \n{} '.format(json_list))
    return json_dict

if __name__ == "__main__":
    exit(main())
