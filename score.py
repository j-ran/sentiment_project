""" Input a phrase and get a score of '0' (negative feeling) or '1' (positive feeling).
This pipeline was created with a lot of help from https://nlpforhackers.io/sentiment-analysis-intro/ 

Here's a test:

# expecting a return of '1'
# text = ("love love love love love love")

# expecting a return of '0'
# text = ("hate hate hate hate hate")

# polar_score = swn_polarity(text)
# print(f'The text "{text}" scores {polar_score}.')

"""

# scoring-related modules
import nltk    # natural language toolkit
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk import sent_tokenize, word_tokenize, pos_tag

# output-related modules
import csv   
from random import choice, randint


# defining some important variables
csv_filename = 'werespond_quotes04.csv'
lemmatizer = WordNetLemmatizer()


def penn_to_wn(tag):
    """
    Convert between the PennTreebank tags to simple Wordnet tags.
    """
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None


def clean_text(text):
    """Clean the spaces and breaks from the text."""
    text = text.replace("<br />", " ")
    return text


def swn_polarity(text):
    """
    Return a sentiment polarity: 0 = negative, 1 = positive
    """
 
    sentiment = 0.0
    tokens_count = 0
 
    text = clean_text(text)
 

    raw_sentences = sent_tokenize(text)
    for raw_sentence in raw_sentences:
        tagged_sentence = pos_tag(word_tokenize(raw_sentence))
 
        for word, tag in tagged_sentence:
            wn_tag = penn_to_wn(tag)
            if wn_tag not in (wn.NOUN, wn.ADJ, wn.ADV):
                continue
 
            lemma = lemmatizer.lemmatize(word, pos=wn_tag)
            if not lemma:
                continue
 
            synsets = wn.synsets(lemma, pos=wn_tag)
            if not synsets:
                continue
 
            # Take the first sense, the most common
            synset = synsets[0]
            swn_synset = swn.senti_synset(synset.name())
 
            sentiment += swn_synset.pos_score() - swn_synset.neg_score()
            tokens_count += 1
 
    # judgment call ? Default to positive or negative
    if not tokens_count:
        return 0
 
    # sum greater than 0 => positive sentiment
    if sentiment >= 0:
        return 1
 
    # negative sentiment
    return 0    

#### above here is creating the score
#### below here is applying it to csv

def create_phrase_statement(csv_filename):
    dict = {}
    printed_phrases = []

    with open(csv_filename, "r") as f:
        contents = csv.reader(f)

        for row in contents:
            # this way of writing a dictionary means
            # what's on the left is the key
            # and what's on the right is 'values'
            dict[row[0]] = [row[1]]
        
        for phrase in dict:
            clean = clean_text(phrase)
            row_score = swn_polarity(clean)
            dict[phrase].append(row_score)

        # for phrase, metadata in (dict.items()):
        #       print(f'A {metadata[0]} said, "{phrase}" score={metadata[1]}')    

        vowels = ['a', 'e', 'i', 'o', 'u']
        capitals = ['F','H','M','N','R','S','X']
        for phrase, metadata in dict.items():  
            if metadata[0:1] not in vowels and capitals:
                a_phrase = (f'A {metadata[0]} said, "{phrase}" score={metadata[1]}')
                printed_phrases.append(a_phrase)
            else:
                a_phrase = (f'An {metadata[0]} said, "{phrase}" score={metadata[1]}')
                printed_phrases.append(a_phrase)

        for n in range(randint(3, 10)):
             print('***')
             print(choice(printed_phrases))


create_phrase_statement(csv_filename)