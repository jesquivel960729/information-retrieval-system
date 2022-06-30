from tools.tokenizer import tokenize_query_expansion

from nltk.corpus import wordnet as wn

def expansion_synonyms(query):
    tokens = tokenize_query_expansion(query)

    words=[]
    synonyms = []
    for token in tokens:
        print(token)
        for syn in wn.synsets(token):
            # print(syn.lemmas())
            for lm in syn.lemmas():
                # print(lm/)
                synonyms.append(lm.name())

        synonyms = (set(synonyms))
        words.extend(list(synonyms)[:2])
        synonyms = []

    return words
