import json
import re
from string import punctuation
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from stopwords import french_stopwords, english_stopwords
import pandas as pd
from textblob import TextBlob

from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer


import gensim
from gensim import corpora

import warnings
warnings.filterwarnings('ignore')



with open("full2.json", "r") as read_file:
    data = json.load(read_file)


def character_replacement(input_string):
    character_mapping = {"\\u00e9": "é",
                        "\\u2019": "'",
                        "\\": "",
                        "\\u00fb": "û",
                        "u00e8": "è",
                        "u00e0": "à",
                        "u00f4": "ô",
                        "u00ea": "ê",
                        "u00ee": "i",
                        "u00fb": "û",
                        "u2018": "'",
                        "u00e2": "a",
                        "u00ab": "'",
                        "u00bb": "'",
                        "u00e7": "ç",
                        "u00e2": "â",
                        "u00f9": "ù",
                        "u00a3": "£",
                        }


    for character in character_mapping:
        input_string = input_string.replace(character, character_mapping[character])

    input_string = input_string.lower()

    characters_to_remove = ["@", "/", "#", ".", ",", "!", "?", "(", ")", "-", "_", "’", "'", "\"", ":", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    transformation_dict = {initial: " " for initial in characters_to_remove}
    no_punctuation_reviews = input_string.translate(str.maketrans(transformation_dict))

    return no_punctuation_reviews

def tokenize(input_string):
    return word_tokenize(input_string)

def remove_stop_words_french(input_tokens):
    return [token for token in input_tokens if token not in french_stopwords]

def remove_stop_words_english(input_tokens):
    return [token for token in input_tokens if token not in english_stopwords]

# Lemmatization
lemmatizer = WordNetLemmatizer()
def lemmatize(tokens):
    tokens = [lemmatizer.lemmatize(lemmatizer.lemmatize(lemmatizer.lemmatize(token,pos='a'),pos='v'),pos='n') for token in tokens]
    return tokens

# Stemming
frenchStemmer=SnowballStemmer("french")
def stem(tokens):
    tokens = [frenchStemmer.stem(token) for token in tokens]
    return tokens



reviews = pd.DataFrame.from_dict(data)

reviews.review = reviews.review.apply(lambda x: character_replacement(x))
#reviews["detected_language"] = reviews.review.apply(lambda x: TextBlob(x).detect_language())
reviews["tokens"] = reviews.review.apply(lambda x: tokenize(x))
reviews.tokens = reviews.tokens.apply(lambda token_list: [meaningful_word for meaningful_word in token_list if len(meaningful_word) > 3])



french_reviews = reviews[reviews.review_language == "fr"]
english_reviews = reviews[reviews.review_language == "en"]

french_reviews.tokens = french_reviews.tokens.apply(lambda x: remove_stop_words_french(x))
english_reviews.tokens = english_reviews.tokens.apply(lambda x: remove_stop_words_english(x))



english_reviews['inflected'] = english_reviews['tokens'].apply(lemmatize)

french_reviews['inflected'] = french_reviews['tokens'].apply(stem)

dictionary = corpora.Dictionary(english_reviews['inflected'])
doc_term_matrix = [dictionary.doc2bow(rev) for rev in english_reviews['inflected']]


# Creating the object for LDA model using gensim library
LDA = gensim.models.ldamodel.LdaModel

# Build LDA model
num_topics = 5
lda_model = LDA(corpus=doc_term_matrix, id2word=dictionary,
                num_topics=num_topics,
                alpha=[0.0001] * num_topics,
                eta=[0.0001] * len(dictionary),
                chunksize=2000,
                passes=60,
                random_state=100,
               )

print(lda_model.print_topics(num_words=8))