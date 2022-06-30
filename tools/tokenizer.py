import re, string
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def tokenize(text):
    stop = set(stopwords.words("english"))
    stemmer = SnowballStemmer(language='english')

    text = replace_punctuation(text)
    text = replace_digits(text)
    words = word_tokenize(text)
    words = [word.lower() for word in words if word not in stop]
    words = [stemmer.stem(word) for word in words]
    return words

def tokenize_query_expansion(text):
    stop = set(stopwords.words("english"))
    stemmer = SnowballStemmer(language='english')

    text = replace_punctuation(text)
    text = replace_digits(text)
    words = word_tokenize(text)
    words = [word.lower() for word in words if word not in stop]

    return words
    
def tokenize_boolean(token):
    stemmer = SnowballStemmer(language='english')
    word = stemmer.stem(token.lower())
    return word
    
def replace_punctuation(text):
    return re.sub('[%s]' % re.escape(string.punctuation),'', text)

def replace_digits(text):
    return re.sub('[%s]' % re.escape(string.digits),'', text)
