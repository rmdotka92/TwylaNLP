import spacy
from spellchecker import SpellChecker
from textblob import TextBlob
from textblob import Word
import os
import json


nlp = spacy.load('en_core_web_sm')
test_sentence = "My fried Ane who cn;t jup ovr a wal"
doc = nlp(test_sentence)
tokens = [token.text for token in doc] #Tokenise
pos_tags = [token.pos_ for token in doc] #POS tags
token_tag = list(zip(tokens,pos_tags))
print(f'The tokenized form of the sentence is as follows : \n{tokens}')
print(f'The POS tags of the sentence are as follows : \n{pos_tags}')
print('The (token,postag) tuples are : {}'.format(token_tag))


#using SpellChecker library in python
def spellchecker_test(list_tokens):

    """This is a function to test the SpellChecker library for spell-checking performance."""

    print('\n{} \nBegin \'SpellChecker\' testing \n'.format('#'*20))

    spell = SpellChecker()

    # find those words that may be misspelled
    misspelled = spell.unknown(list_tokens)

    for word in misspelled:

        #print the incorrect word
        print(f'The incorrect word is "{word}"')

        # Get the one `most likely` answer
        print(f'Using Spellchecker, the correction is : {spell.correction(word)}')

        # Get a list of `likely` options
        print(f'The candidate words for the correction of "{word}" is : ')
        print(spell.candidates(word))


# Using textblob library in Python
def textblob_test(sentence):

    """This is a function that tests the TextBlob library for spell-checking performance."""

    print('\n{} \nBegin \'textblob\' testing \n'.format('#'*20))
    tb = TextBlob(sentence)
    print('The attempted correction by "Textblob" is : {}'.format(tb.correct()))


#Using symspellpy library in python
from symspellpy.symspellpy import SymSpell, Verbosity  # import the module

# create object
initial_capacity = 83000
# maximum edit distance per dictionary precalculation
max_edit_distance_dictionary = 3
prefix_length = 7
sym_spell = SymSpell(initial_capacity, max_edit_distance_dictionary,
                     prefix_length)
# load dictionary

term_index = 0  # column of the term in the dictionary text file
count_index = 1  # column of the term frequency in the dictionary text file
max_edit_distance_lookup = 3
suggestion_verbosity = Verbosity.CLOSEST

def symspell_test(tokenpos_list):

    """This is a function that tests the SymSpell library for spell-checking performance."""

    print('\n{} \nBegin \'Symspellpy\' testing \n'.format('#'*20))

    dictionary_path = os.path.join(os.path.dirname(__file__),
                                   "frequency_dictionary_en_82_765.txt")
    if not sym_spell.load_dictionary(dictionary_path, term_index, count_index):
        print("Dictionary file not found")
        return 'Error loading dictionary file'
    suggestion_list = []
    proper_noun = []

    for (w,pos) in tokenpos_list:
        if pos == 'PROPN':
            suggestion_list.append(w)
            proper_noun.append(w)
        elif len(w) <3:
            suggestion_list.append(w)
            proper_noun.append(w)
        else:
            suggestions = sym_spell.lookup(w, suggestion_verbosity,
                                           max_edit_distance_lookup)
            suggestion = (list(suggestions))[0]
            # display suggestion term, term frequency, and edit distance
            print("input_term = {}, suggestion_term = {}, suggestion_count = {},suggestion_distance =  {}".format(w, suggestion.term, suggestion.count,
                                          suggestion.distance))
            suggestion_list.append(suggestion.term)
    return suggestion_list, proper_noun

if __name__ == "__main__":
    sp_result = spellchecker_test(tokens)
    tb_result = textblob_test(test_sentence)
    sym_result, proper_noun_list = symspell_test(token_tag)

    #Generating json format
    print('\n{} \nGenerate json format using symspell results \n'.format('#'*20))

    corrected_sent = ' '.join(sym_result)

    #modifying original list of tokens to add possible repetitions
    correct_token_list = [(word,index) for (index,word) in enumerate(sym_result) if word != test_sentence.lower().split()[index] and word not in proper_noun_list]
    print('correct token list is : {}\n'.format(correct_token_list))

    test_sentence_copy = test_sentence.split()
    flag = 0
    for (w,i) in correct_token_list:
        num_parts = len(nlp(w))
        test_sentence_copy[i+flag : i+flag+1] = test_sentence_copy[i+flag : i+flag+1] * num_parts
        flag += num_parts-1
    print('The modified version of the original token list is : {} \n'.format(test_sentence_copy))

    #tokenising the corrected sentence and generating pos tags
    new_sent = nlp(corrected_sent)
    new_sent_tokens = [w.text for w in new_sent]
    print("New sentence tokens are : {} \n".format(new_sent_tokens))
    new_pos_tags = [w.pos_ for w in new_sent]

    json_list = []
    for i in range(len(new_sent_tokens)):
        json_list.append({"token":new_sent_tokens[i], "pos":new_pos_tags[i], "raw":test_sentence_copy[i]})

    json_list = json.dumps(json_list)
    print(json_list)
