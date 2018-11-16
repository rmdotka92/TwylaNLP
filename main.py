"""
TwylaNLP - https://github.com/rmdotka92/TwylaNLP
------------------------------------------------
This is the main code required to run the RESTful service.
It takes in a user-input of the form,
{
    "input" : *some input string*
}
and returns a spell-corrected version of the input string.
-------------------------------------------------
The spellcheckers used here are "symspellpy" and "pyenchant".
You can read more about them here:
* https://github.com/wolfgarbe/SymSpell/blob/master/README.md (description)
* https://github.com/mammothb/symspellpy (version 6.3 used here)
* https://github.com/rfk/pyenchant
"""

import os
import logging
from flask import Flask, make_response, request, jsonify
from flask_restful import Resource, Api
# import enchant
import spacy
from symspellpy.symspellpy import SymSpell, Verbosity

DEFAULT = 1 #1/0 :Symspell spell-checker/Enchant spell-checker
MAXLENGTH = 100 #Maximum acceptable input length
logging.basicConfig(filename = 'main_logger.log', level=logging.WARNING)
nlp = spacy.load('en_core_web_sm') #Spacy English library


def check_symspell_dictionary(sym_spell, term_index=0, count_index=1):
    """
    term_index = column of terms ; count_index = column of word-frequency
    """
    dictionary_path = os.path.join(os.path.dirname(__file__),
                                   "frequency_dictionary_en_82_765.txt")
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        logging.error('Error loading symspell dictionary !'), 402
    else:
        return logging.info('Successfully loaded symspell dictionary.')


def pre_processing(sentence: str)->list:
    """
    sentence tokenising, pos_tagging, (token, pos_tag) generation with Spacy
    :return: list of tokens, list of pos_tags, list of (token,pos_tag) tuples
    :return: 405 Error: Wrong input type! (Expected string)
    :return: 402 Error: Wrong input type! (Expected non-empty string)
    """
    try:
        if not sentence:
            logging.error('Empty string detected!')
            return 402
        elif len(sentence) > MAXLENGTH:
            return 408
        doc = nlp(sentence)
        tokens = [token.text for token in doc] #Tokenise
        letter_case = [1 if token.istitle() else 0 for token in tokens]
        tokens = [token.lower() for token in tokens]
        pos_tags = [token.pos_ for token in doc] #Parts-of-speech tags
        token_tags = list(zip(tokens, pos_tags))
        return tokens, pos_tags, token_tags, letter_case
    except TypeError:
        logging.error('Invalid string detected!')
        return 405


#Spell correction
def symspell_test(tokenpos_list: list, ignore_length = 2, max_edit_distance_lookup=2,
                initial_capacity=83000, max_edit_distance_dictionary=2,
                prefix_length=7, suggestion_verbosity=Verbosity.TOP)->list:
    """
    keyword arguments are:

    suggestion_verbosity =
    TOP: Top suggestion with smallest edit distance with highest term frequency.
    CLOSEST: All suggestions of smallest edit distance found ordered by frequency.
    ALL: All suggestions within maxEditDistance.

    :return: list of suggested corrections, list of ignored words
    :return: 410 Error: Wrong input type! (Expected list of 2 element tuples)
    """
    try:
        sym_spell = SymSpell(initial_capacity, max_edit_distance_dictionary,
                             prefix_length)
        check_symspell_dictionary(sym_spell)
        suggestion_list = []
        intact_words = []
        for (word, pos) in tokenpos_list:
            if pos == 'PROPN' or len(word) <= ignore_length:
                suggestion_list.append(word)
                intact_words.append(word)
            else:
                suggestions = sym_spell.lookup(word, suggestion_verbosity,
                                               max_edit_distance_lookup)
                suggestion = (list(suggestions))[0]
                suggestion_list.append(suggestion.term)
        return suggestion_list, intact_words
    except (ValueError, TypeError):
        logging.error('Invalid type! Type List of tuples expected as input.')
        return 410


def enchant_check(tokenposlist: list, ignore_length = 2)-> list:
    """
    Spell-checking based on the pyenchant libraryself.
    :var: ignore_length : Ignore words having upto 'ignore_length' chars

    :return: list of suggested corrections, list of ignored words
    :return: 410 Error: Wrong input type! (Expected list of 2 element tuples)
    """
    try:
        d = enchant.Dict("en_US")
        suggestions = [] #correction suggestions
        intact_words = [] #ignored words
        for (word,pos) in tokenposlist:
            if pos == 'PROPN' or len(word) <= ignore_length:
                suggestions.append(word)
                intact_words.append(word)
            elif not d.check(word):
                suggestions.append(d.suggest(word)[0])
            else:
                suggestions.append(word)
        return suggestions, intact_words
    except (ValueError, TypeError):
        logging.error('Invalid type! Type List of tuples expected as input.')
        return 410


def post_processing(sentence: str)->list:
    """
    Get the spellchecker output into desired format.
    :return: list of dicts
    :return: 410 Error: Wrong input type! (Expected string)
    """
    try:
        tokens, pos_tags, token_pos, token_case = pre_processing(sentence)
        if DEFAULT:
            suggested_tokens, intact_words_list = symspell_test(token_pos)
        else:
            suggested_tokens, intact_words_list = enchant_check(token_pos)
        corrected_sent = ' '.join(suggested_tokens)
        new_tokens, new_pos_tags, new_token_pos, new_token_case = pre_processing(corrected_sent)

        #modifying original list of tokens to add possible repetitions
        correct_token_list = [(word, index) for (index, word) in enumerate(suggested_tokens)
         if word != sentence.lower().split()[index]
         and word not in intact_words_list]
        original_tokens = tokens  #Make a copy of the original list of tokens
        offset = 0 #Offset to account for shift in index after possible duplication of original incorrect tokens
        for (word, index) in correct_token_list:
            num_parts = len(nlp(word))
            original_tokens[index+offset : index+offset+1] = original_tokens[index+offset : index+offset+1] * num_parts
            if num_parts > 1:
                token_case.insert(index+offset, token_case[index+offset])
            offset += num_parts-1
        payload = []

        #Reassigining case to both, original and corrected tokens
        original_tokens = [token.title() if case == 1 else token for (case,token)
        in list(zip(token_case, original_tokens))]
        new_tokens = [token.title() if case == 1 else token for (case,token)
        in list(zip(token_case, new_tokens))]
        logging.info('Generating RESTful output payload format.')
        for i,_ in enumerate(new_tokens):
            payload.append({"token":new_tokens[i], "pos":new_pos_tags[i], "raw":original_tokens[i]})
        return payload
    except TypeError:
        return 410


class tokenise_api(Resource):
    def get(self):
        """
        This function does a GET operation on the /tokenise end-point.
        :return: 200 OK.
        """
        return {'tokens': ''}

    def post(self):
        """
        This function does a POST operation on the /tokenise end-point.
        :return: 201 Success!
        :return: 402 Error: Empty string detected!
        :return: 406 Error: Wrong key in input json payload (Expected key == "input")
        :return: 408 Error: Max input length exceeded!
        :return: 410 Error: Wrong input type!
        """
        entry = request.get_json(force=True)
        key, value = list(entry.items())[0]
        if key != "input":
            logging.warning('Wrong key in input payload detected!')
            return 'Error: Please set key = "input" in json payload dict !', 406
        elif not isinstance(value, str):
            logging.warning('Wrong data type value in input. String expected!')
            return 'Error: Please enter non-empty string as the value in json payload!', 410
        elif not value:
            logging.warning('Empty string detected!')
            return 'Error: Please enter non-empty string as the value in json payload!', 402
        elif len(value) > MAXLENGTH:
            return 'Error: Please enter input with no. of characters < 100!', 408
        else:
            return {'tokens':post_processing(value)}, 201


def main_restful(debugging=True):
    """
    Main code to run the RESTful api.
    """
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(tokenise_api, '/tokenise')
    app.run(debug=debugging)


if __name__ == '__main__':
    main_restful()
