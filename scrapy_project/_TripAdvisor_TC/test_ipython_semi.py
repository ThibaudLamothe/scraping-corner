# import pandas as pd
# from tqdm import tqdm, tqdm_notebook # progress bars in Jupyter
# import newspaper # download newspapers' data easily
# from time import time # measure the computation time of a python code
# import pandas as pd # the most basic & powerful data manipulation tool
# import numpy as np # Here, mostly used for np.nan
# import langdetect # detect the language of text
# import stop_words # handles stop words in many languages without having to rebuild them everytime
# import spacy # NLP library for POS tagging
# import nltk
# from nltk.tokenize import word_tokenize
# from nltk.stem.snowball import SnowballStemmer
# from sklearn.model_selection import train_test_split
# from sklearn.metrics import classification_report
# import re
#
# # For spacy use "pip install spacy", then "python -m spacy download en" to download English text mining modules

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import json
from random import randint
import itertools
import numpy as np

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

import warnings
warnings.filterwarnings('ignore')

french_stopwords = ["a","abord","absolument","afin","ah","ai","aie","aient","aies","ailleurs","ainsi","ait","allaient","allo","allons","allô","alors","anterieur","anterieure","anterieures","apres","après","as","assez","attendu","au","aucun","aucune","aucuns","aujourd","aujourd'hui","aupres","auquel","aura","aurai","auraient","aurais","aurait","auras","aurez","auriez","aurions","aurons","auront","aussi","autre","autrefois","autrement","autres","autrui","aux","auxquelles","auxquels","avaient","avais","avait","avant","avec","avez","aviez","avions","avoir","avons","ayant","ayez","ayons","b","bah","bas","basee","bat","beau","beaucoup","bien","bigre","bon","boum","bravo","brrr","c","car","ce","ceci","cela","celle","celle-ci","celle-là","celles","celles-ci","celles-là","celui","celui-ci","celui-là","celà","cent","cependant","certain","certaine","certaines","certains","certes","ces","cet","cette","ceux","ceux-ci","ceux-là","chacun","chacune","chaque","cher","chers","chez","chiche","chut","chère","chères","ci","cinq","cinquantaine","cinquante","cinquantième","cinquième","clac","clic","combien","comme","comment","comparable","comparables","compris","concernant","contre","couic","crac","d","da","dans","de","debout","dedans","dehors","deja","delà","depuis","dernier","derniere","derriere","derrière","des","desormais","desquelles","desquels","dessous","dessus","deux","deuxième","deuxièmement","devant","devers","devra","devrait","different","differentes","differents","différent","différente","différentes","différents","dire","directe","directement","dit","dite","dits","divers","diverse","diverses","dix","dix-huit","dix-neuf","dix-sept","dixième","doit","doivent","donc","dont","dos","douze","douzième","dring","droite","du","duquel","durant","dès","début","désormais","e","effet","egale","egalement","egales","eh","elle","elle-même","elles","elles-mêmes","en","encore","enfin","entre","envers","environ","es","essai","est","et","etant","etc","etre","eu","eue","eues","euh","eurent","eus","eusse","eussent","eusses","eussiez","eussions","eut","eux","eux-mêmes","exactement","excepté","extenso","exterieur","eûmes","eût","eûtes","f","fais","faisaient","faisant","fait","faites","façon","feront","fi","flac","floc","fois","font","force","furent","fus","fusse","fussent","fusses","fussiez","fussions","fut","fûmes","fût","fûtes","g","gens","h","ha","haut","hein","hem","hep","hi","ho","holà","hop","hormis","hors","hou","houp","hue","hui","huit","huitième","hum","hurrah","hé","hélas","i","ici","il","ils","importe","j","je","jusqu","jusque","juste","k","l","la","laisser","laquelle","las","le","lequel","les","lesquelles","lesquels","leur","leurs","longtemps","lors","lorsque","lui","lui-meme","lui-même","là","lès","m","ma","maint","maintenant","mais","malgre","malgré","maximale","me","meme","memes","merci","mes","mien","mienne","miennes","miens","mille","mince","mine","minimale","moi","moi-meme","moi-même","moindres","moins","mon","mot","moyennant","multiple","multiples","même","mêmes","n","na","naturel","naturelle","naturelles","ne","neanmoins","necessaire","necessairement","neuf","neuvième","ni","nombreuses","nombreux","nommés","non","nos","notamment","notre","nous","nous-mêmes","nouveau","nouveaux","nul","néanmoins","nôtre","nôtres","o","oh","ohé","ollé","olé","on","ont","onze","onzième","ore","ou","ouf","ouias","oust","ouste","outre","ouvert","ouverte","ouverts","o|","où","p","paf","pan","par","parce","parfois","parle","parlent","parler","parmi","parole","parseme","partant","particulier","particulière","particulièrement","pas","passé","pendant","pense","permet","personne","personnes","peu","peut","peuvent","peux","pff","pfft","pfut","pif","pire","pièce","plein","plouf","plupart","plus","plusieurs","plutôt","possessif","possessifs","possible","possibles","pouah","pour","pourquoi","pourrais","pourrait","pouvait","prealable","precisement","premier","première","premièrement","pres","probable","probante","procedant","proche","près","psitt","pu","puis","puisque","pur","pure","q","qu","quand","quant","quant-à-soi","quanta","quarante","quatorze","quatre","quatre-vingt","quatrième","quatrièmement","que","quel","quelconque","quelle","quelles","quelqu'un","quelque","quelques","quels","qui","quiconque","quinze","quoi","quoique","r","rare","rarement","rares","relative","relativement","remarquable","rend","rendre","restant","reste","restent","restrictif","retour","revoici","revoilà","rien","s","sa","sacrebleu","sait","sans","sapristi","sauf","se","sein","seize","selon","semblable","semblaient","semble","semblent","sent","sept","septième","sera","serai","seraient","serais","serait","seras","serez","seriez","serions","serons","seront","ses","seul","seule","seulement","si","sien","sienne","siennes","siens","sinon","six","sixième","soi","soi-même","soient","sois","soit","soixante","sommes","son","sont","sous","souvent","soyez","soyons","specifique","specifiques","speculatif","stop","strictement","subtiles","suffisant","suffisante","suffit","suis","suit","suivant","suivante","suivantes","suivants","suivre","sujet","superpose","sur","surtout","t","ta","tac","tandis","tant","tardive","te","tel","telle","tellement","telles","tels","tenant","tend","tenir","tente","tes","tic","tien","tienne","tiennes","tiens","toc","toi","toi-même","ton","touchant","toujours","tous","tout","toute","toutefois","toutes","treize","trente","tres","trois","troisième","troisièmement","trop","très","tsoin","tsouin","tu","té","u","un","une","unes","uniformement","unique","uniques","uns","v","va","vais","valeur","vas","vers","via","vif","vifs","vingt","vivat","vive","vives","vlan","voici","voie","voient","voilà","vont","vos","votre","vous","vous-mêmes","vu","vé","vôtre","vôtres","w","x","y","z","zut","à","â","ça","ès","étaient","étais","était","étant","état","étiez","étions","été","étée","étées","étés","êtes","être","ô"]
english_stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "good", "great", "woburn" "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]



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


def cleaning_data(reviews):
    reviews.review = reviews.review.apply(lambda x: character_replacement(x))
    # reviews["detected_language"] = reviews.review.apply(lambda x: get_review_language(x))
    reviews["tokens"] = reviews.review.apply(lambda x: tokenize(x))
    reviews.tokens = reviews.tokens.apply(
        lambda token_list: [meaningful_word for meaningful_word in token_list if len(meaningful_word) > 3])

    french_reviews = reviews[reviews.review_language == "fr"]
    english_reviews = reviews[reviews.review_language == "en"]

    french_reviews.tokens = french_reviews.tokens.apply(lambda x: remove_stop_words_french(x))
    english_reviews.tokens = english_reviews.tokens.apply(lambda x: remove_stop_words_english(x))

    english_reviews['inflected'] = english_reviews['tokens'].apply(lemmatize)
    french_reviews['inflected'] = french_reviews['tokens'].apply(stem)

    english_reviews['joined_stemmed_text'] = [' '.join(word for word in word_list) for word_list in english_reviews.inflected]
    french_reviews['joined_stemmed_text'] = [' '.join(word for word in word_list) for word_list in french_reviews.inflected]

    return english_reviews

#
# output_path = ''
# df = pd.read_csv(output_path + 'labeled_data.csv', engine='python') # label data only -> used for supervised model
#
# path_data_to_label = ''
# dfu = pd.read_csv(path_data_to_label+'data_unlabeled.csv', encoding = 'utf-8')
# # unlabeled data -> used to together with lable data for semi supervised learning
#
#
#


with open("full.json", "r") as read_file:
    data = json.load(read_file)
reviews = pd.DataFrame.from_dict(data)

df = reviews.loc[:1000, :]
dfu = reviews.loc[1000:, :]


df["topic1"] = 0
df["topic1"] = df.topic1.apply(lambda x: x + randint(0, 1))



print(df.topic1.value_counts())


## split between train and test at the beginning
# we will use the same test set for supervised and semi supervised learning, so that we can compare the performances of
# both approaches
df_train, df_test = train_test_split(df, test_size=0.3, random_state=42, stratify=df.topic1)

# Preparing data
df_train = cleaning_data(df_train)
df_test = cleaning_data(df_test)
dfu = cleaning_data(dfu)

## in order to have the same features on train data sets (for both supervised and semi-sup) and test data sets
# build the tf idf with vocab which is the union the 3 above data sets
vocab = list(set(itertools.chain(*dfu.inflected.tolist()))|set(itertools.chain(*df_test.inflected.tolist()))|set(itertools.chain(*df_train.inflected.tolist())))
vocab_dict = dict((y, x) for x, y in enumerate(vocab))
print(len(vocab))

# build tf idf matrix separately for train and test and unlabeled data sets
tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, ngram_range=(1,3), use_idf=True, vocabulary = vocab_dict)
td_train = tfidf_vectorizer.fit_transform(df_train.joined_stemmed_text.tolist())
td_test = tfidf_vectorizer.fit_transform(df_test.joined_stemmed_text.tolist())
td_u = tfidf_vectorizer.fit_transform(dfu.joined_stemmed_text.tolist())


# same with NMF dimensionality reduction
# the NMF decomposes this Term Document matrix into the product of 2 smaller matrices: W and H
n_dimensions = 50 # This can also be interpreted as topics in this case. This is the "beauty" of NMF. 10 is arbitrary
nmf_model = NMF(n_components=n_dimensions, random_state=42, alpha=.1, l1_ratio=.5)

X_train = pd.DataFrame(nmf_model.fit_transform(td_train))
X_test = pd.DataFrame(nmf_model.fit_transform(td_test))
X_u = pd.DataFrame(nmf_model.fit_transform(td_u))

# get the labels for both train and test
y_train = df_train.topic1.map(int)
y_test = df_test.topic1.map(int)

# lets look at the number of positive in the data sets
print(len(X_train))
print(sum(y_train))
print(sum(y_test))


# lets estimate a gradient boosting classifier
model = GradientBoostingClassifier(n_estimators=100, random_state=42, learning_rate=0.1)


fitted_model = model.fit(X_train, y_train)

print(fitted_model)


df.loc[df.topic1==1].head()


print(confusion_matrix(y_train, model.predict(X_train)))
print(confusion_matrix(y_test, model.predict(X_test)))


print(classification_report(y_test, model.predict(X_test)))

from sklearn.semi_supervised import LabelPropagation
label_prop_model = LabelPropagation(kernel = 'knn', n_neighbors=10, max_iter = 3000)
label_prop_model.fit(pd.concat([X_train, X_test]), pd.concat([y_train, y_test]))


y_semi_proba = label_prop_model.predict_proba(X_u) # first column gives the proba of 0, second column gives the proba of 1
y_semi = pd.Series(label_prop_model.predict(X_u))
print(y_semi.value_counts())


proba_1 = y_semi_proba[:,1] # get the proba of 1
pd.Series(proba_1).describe()


# with n neigh = 10
X_train_semi = pd.concat([X_train, X_u])
y_train_semi = pd.concat([y_train, y_semi])
model.fit(X_train_semi, y_train_semi)

print(confusion_matrix(y_train_semi, model.predict(X_train_semi)))
print(confusion_matrix(y_test, model.predict(X_test)))

print(classification_report(y_test, model.predict(X_test)))


# try to spread more labels (use thereshold lower than 0.5 in order to predict more labels)
# here we spread the same proportion of 1 in the unlabeled data set as in the labeled train data set
y_semi_bis = pd.Series([1 if x > pd.Series(proba_1).quantile(q=1-np.mean(y_train)) else 0 for x in proba_1])
y_train_semi_bis = pd.concat([y_train, y_semi_bis])
model.fit(X_train_semi, y_train_semi_bis)
print(confusion_matrix(y_train_semi_bis, model.predict(X_train_semi)))
print(confusion_matrix(y_test, model.predict(X_test)))

print(classification_report(y_test, model.predict(X_test)))

