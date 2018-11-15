"""
TwylaNLP - https://github.com/rmdotka92/TwylaNLP
------------------------------------------------

This is the main code required to run the RESTful service.

It takes in a user-input of the form,
{
    "input" : *some input string*
}
and returns a spell-corrected version of the input string.

The spellcheckers used here are "symspellpy" and "pyenchant".
You can read more about them here:
* https://github.com/wolfgarbe/SymSpell/blob/master/README.md (description)
* https://github.com/mammothb/symspellpy (version 6.3 used here)
* https://github.com/rfk/pyenchant
"""

import os
import json
import sys
from flask import Flask, make_response, request, jsonify
from flask_restful import Resource, Api
import enchant
import spacy
from symspellpy.symspellpy import SymSpell, Verbosity

nlp = spacy.load('en_core_web_sm') #Spacy English library

def check_symspell_dictionary(sym_spell, term_index=0, count_index=1):
    """
    term_index = column of terms ; count_index = column of word-frequency
    """
    dictionary_path = os.path.join(os.path.dirname(__file__),
                                   "frequency_dictionary_en_82_765.txt")
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        sys.exit('Error loading symspell dictionary !')
    else:
        return 'Successfully loaded symspell dictionary.'

def pre_processing(sentence: str):
    """
    sentence tokenising, pos_tagging, (token, pos_tag) generation with Spacy
    """
    try:
        doc = nlp(sentence)
        tokens = [token.text for token in doc] #Tokenise
        pos_tags = [token.pos_ for token in doc] #Parts-of-speech tags
        token_tags = list(zip(tokens, pos_tags))
        return tokens, pos_tags, token_tags
    except TypeError:
        # print('Invalid string detected!')
        return 405

#Spell correction
def symspell_test(tokenpos_list, max_edit_distance_lookup=2,
                initial_capacity=83000, max_edit_distance_dictionary=2,
                prefix_length=7, suggestion_verbosity=Verbosity.TOP):
    """
    keyword arguments are:

    suggestion_verbosity =
    TOP: Top suggestion with smallest edit distance with highest term frequency.
    CLOSEST: All suggestions of smallest edit distance found ordered by frequency.
    ALL: All suggestions within maxEditDistance.
    """
    try:
        sym_spell = SymSpell(initial_capacity, max_edit_distance_dictionary,
                             prefix_length)
        check_symspell_dictionary(sym_spell)
        ignore_length = 2 #Ignore words made of upto 'ignore_length' characters
        suggestion_list = []
        intact_words = []
        for (word, pos) in tokenpos_list:
            if pos == 'PROPN':
                suggestion_list.append(word)
                intact_words.append(word)
            elif len(word) <= ignore_length:
                suggestion_list.append(word)
                intact_words.append(word)
            else:
                suggestions = sym_spell.lookup(word, suggestion_verbosity,
                                               max_edit_distance_lookup)
                suggestion = (list(suggestions))[0]
                suggestion_list.append(suggestion.term)
        return suggestion_list, intact_words
    except (ValueError, TypeError):
        # print(f'Invalid type! Enter list of tokens as input: {error}')
        return 410

def enchant_check(tokenposlist, ignore_length = 2):
    """
    Spell-checking based on the pyenchant libraryself.
    :var: ignore_length : Ignore words having upto 'ignore_length' chars
    """
    try:
        d = enchant.Dict("en_US")
        suggestions = [] #correction suggestions
        intact_words = [] #ignored words
        for (word,pos) in tokenposlist:
            if pos == 'PROPN':
                suggestions.append(word)
                intact_words.append(word)
            elif len(word) <= ignore_length:
                suggestions.append(word)
                intact_words.append(word)
            elif d.check(word) == False:
                suggestions.append(d.suggest(word)[0])
            else:
                suggestions.append(word)
        return suggestions, intact_words
    except (ValueError, TypeError):
        return 410

def post_processing(sentence):
    """
    Get the spellchecker output into desired format
    """

    tokens, pos_tags, token_tags = pre_processing(sentence)
    # sym_tokens, intact_words_list = symspell_test(token_tags)
    sym_tokens, intact_words_list = enchant_check(token_tags)
    corrected_sent = ' '.join(sym_tokens)
    new_tokens, new_pos_tags, new_token_tags = pre_processing(corrected_sent)

    #modifying original list of tokens to add possible repetitions
    correct_token_list = [(word, index) for (index, word) in enumerate(sym_tokens) if word != sentence.lower().split()[index] and word not in intact_words_list]

    original_tokens = tokens
    offset = 0 #Offset to account for shift in index after possible duplication of original incorrect tokens
    for (word, index) in correct_token_list:
        num_parts = len(nlp(word))
        original_tokens[index+offset : index+offset+1] = original_tokens[index+offset : index+offset+1] * num_parts
        offset += num_parts-1

    payload = []
    for i,_ in enumerate(new_tokens):
        payload.append({"token":new_tokens[i], "pos":new_pos_tags[i], "raw":original_tokens[i]})
    return payload

class tokenise_api(Resource):
    def get(self):
        """
        This function does a GET operation on the /tokenise end-point.
        :return: 200 OK
        """
        return {'tokens': ''}

    def post(self):
        """
        This function does a POST operation on the /tokenise end-point.
        :return: 201 Success!
        :return: 406 Error : Wrong key!
        :return: 410 Error : Non-string value!
        """
        entry = request.get_json(force=True)
        key, val = list(entry.items())[0]
        if key != "input":
            return 'Error: Please set key = "input" in json payload !', 406
        elif not isinstance(val, str):
            return 'Error: Please enter string as the value in json payload!', 410
        else:
            return {'tokens':post_processing(val)}, 201

def main_restful(debugging=True):
    '''
    Main code to run the api
    '''
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(tokenise_api, '/tokenise')
    app.run(debug=debugging)

if __name__ == '__main__':
    main_restful()
