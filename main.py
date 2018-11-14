from flask import Flask, make_response, request
from flask_restful import Resource, Api
import enchant
import json
import os
import spacy
from symspellpy.symspellpy import SymSpell, Verbosity #spell-checking

nlp = spacy.load('en_core_web_sm') #English library

def check_symspell_dictionary(term_index=0, count_index=1):
    """term_index = column of terms ; count_index = column of word-frequency"""
    dictionary_path = os.path.join(os.path.dirname(__file__),
                                   "frequency_dictionary_en_82_765.txt")
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        sys.exit('Error loading symspell dictionary !')
    else:
        return 'Successfully loaded symspell dictionary.'

#Sentence pre-processing
def pre_processing(user_response):
    """Tokenising, pos_tagging, (token, pos_tag) generation with Spacy"""
    try:
        doc = nlp(user_response)
        tokens = [token.text for token in doc] #Tokenise
        pos_tags = [token.pos_ for token in doc] #Parts-of-speech tags
        token_tags = list(zip(tokens, pos_tags))
        return tokens, pos_tags, token_tags
    except TypeError as error:
        print(f'Invalid string : {error}')
        return 405

#Spell correction
def symspell_test(tokenpos_list, max_edit_distance_lookup=2,
                initial_capacity=83000, max_edit_distance_dictionary=2,
                prefix_length=7, suggestion_verbosity = Verbosity.CLOSEST):
    """
    Key-word arguments are:
        ** max_edit_distance_lookup : (Recommended maximum = 3)
    """
    try:
        check_symspell_dictionary()
        sym_spell = SymSpell(initial_capacity, max_edit_distance_dictionary,
                             prefix_length)
        ignore_length = 2 #Ignore words having upto 'ignore_length' characters
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
    except TypeError as error:
        print(f'Invalid type! Enter list of tokens as input: {error}')
        return 405

def post_processing(user_response):
    """Get the spellchecker output into desired format."""

    tokens, pos_tags, token_tags = pre_processing(user_response)
    sym_result, intact_words_list = symspell_test(token_tags)

    corrected_sent = ' '.join(sym_result)
    #modifying original list of tokens to add possible repetitions
    correct_token_list = [(word, index) for (index, word) in enumerate(sym_result) if word != user_response.lower().split()[index] and word not in intact_words_list]

    user_response_copy = user_response.split()
    offset = 0 #Offset inorder to account for shift in index after possible duplication of original incorrect tokens
    for (word, index) in correct_token_list:
        num_parts = len(nlp(word))
        user_response_copy[index+offset : index+offset+1] = user_response_copy[index+offset : index+offset+1] * num_parts
        offset += num_parts-1

    #tokenising the corrected sentence and generating pos tags
    new_sent = nlp(corrected_sent)
    new_sent_tokens = [w.text for w in new_sent]
    new_pos_tags = [w.pos_ for w in new_sent]

    json_list = []
    for i,_ in enumerate(new_sent_tokens):
        json_list.append({"token":new_sent_tokens[i], "pos":new_pos_tags[i], "raw":user_response_copy[i]})
    return json_list


app = Flask(__name__)
api = Api(app)

# user_input = {}
class spellcheck(Resource):
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
        :return: 406 Error!
        """
        entry = request.get_json()
        key, val = list(entry.items())[0]
        if key != "input":
            return 'Error : Please set key = "input" in POST request !', 406
        else:
            return {'tokens':post_processing(val)}, 201

api.add_resource(spellcheck, '/tokenise')

if __name__ == '__main__':
    app.run(debug=True)
