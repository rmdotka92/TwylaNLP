import spacy
from spellchecker import SpellChecker
from textblob import TextBlob
from textblob import Word
import os
import json

nlp = spacy.load('en_core_web_sm')
test_sentence = "The fox cn't jump over a fence"
doc = nlp(test_sentence) #Test sentence
tokens = [token.text for token in doc]
print(f'The tokenized form of the sentence is as follows : \n{tokens}')

#using SpellChecker library in python
print('\n{} \nBegin \'SpellChecker\' testing \n'.format('#'*20))

spell = SpellChecker()

# find those words that may be misspelled
misspelled = spell.unknown(tokens)
print('The probability of the word "can\'t" is :')
print(spell.word_probability("can't"))

for word in misspelled:
    print(f'The incorrect word is "{word}"')

    # Get the one `most likely` answer
    print(f'Using Spellchecker, the correction is : {spell.correction(word)}')

    # Get a list of `likely` options
    print(f'The candidate words for the correction of "{word}" is : ')
    print(spell.candidates(word))

# Using textblob library in Python
print('\n{} \nBegin \'textblob\' testing \n'.format('#'*20))

tb = TextBlob("The fox cn't jump over a fence")
print('The attempted correction by "Textblob" is : {}'.format(tb.correct()))
w = Word("can't")
print('The word, confidence tuple of the word "can\'t" is : {}'.format(w.spellcheck()))

#using symspellpy library in python
print('\n{} \nBegin \'Symspellpy\' testing \n'.format('#'*20))

from symspellpy.symspellpy import SymSpell, Verbosity  # import the module

def symspelltest():
    # create object
    initial_capacity = 83000
    # maximum edit distance per dictionary precalculation
    max_edit_distance_dictionary = 2
    prefix_length = 7
    sym_spell = SymSpell(initial_capacity, max_edit_distance_dictionary,
                         prefix_length)
    # load dictionary
    dictionary_path = os.path.join(os.path.dirname(__file__),
                                   "frequency_dictionary_en_82_765.txt")
    term_index = 0  # column of the term in the dictionary text file
    count_index = 1  # column of the term frequency in the dictionary text file
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        print("Dictionary file not found")
        return

    # lookup suggestions for multi-word input strings (supports compound
    # splitting & merging)
    input_term = test_sentence
    # max edit distance per lookup (per single word, not per whole input string)
    max_edit_distance_lookup = 2
    suggestions = sym_spell.lookup_compound(input_term,
                                            max_edit_distance_lookup)
    # display suggestion term, edit distance, and term frequency
    for suggestion in suggestions:
        print("suggestion_term = {}, suggestion_count = {},suggestion_distance =  {}".format(suggestion.term, suggestion.count,
                                  suggestion.distance))
    return suggestion.term

if __name__ == "__main__":
    symspelltest()

#Generating json format
print('\n{} \nGenerate json format \n'.format('#'*20))

corrected_sent = symspelltest()
new_sent = nlp(corrected_sent)
new_sent_tokens = [w.text for w in new_sent]
pos_tags = [w.pos_ for w in new_sent]

json_list = []
for i in range(len(tokens)):
    json_list.append({"token":new_sent_tokens[i], "pos":pos_tags[i], "raw":tokens[i]})

json_list = json.dumps(json_list)
print(json_list)
