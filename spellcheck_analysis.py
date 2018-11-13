import spacy
from spellchecker import SpellChecker
from textblob import TextBlob
from textblob import Word

nlp = spacy.load('en_core_web_sm')
doc = nlp(u"The fox cn't jump over a fence") #Test sentence
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
