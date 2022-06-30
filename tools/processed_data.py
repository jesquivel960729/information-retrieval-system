import json
from tools.tokenizer import *

def processed_corpus(path, collection):
    d = []
    with open(path, 'r') as file:
        contents = file.read()
        d = contents.split('\n.I')
    docs = {} 
    i = 0
    for textd in d:
        i += 1
        text = textd.split('\n.X')
        text = text[0].split('\n.W')
        text_corp = text[1]
        text = text[0].split('\n.A')
        text_authors = text[1]
        text = text[0].split('\n.T')
        text_title = text[1]
        t = ''
        if collection == 2:
            t = text_title + '\n'
        t += text_corp
        docs[i] = tokenize(t)
    return docs

def processed_queries_vect(path, query):
    queries = {}
    q = []
    i = 0
    if query is None:
        with open(path, 'r') as file:
            contents = file.read()
            q = contents.split('\n.I')
        for textd in q:
            i += 1
            text = textd.split('\n.W')
            tok = tokenize(text[1])
            queries[i] = tok
    else:
        i += 1
        queries[i] = tokenize(query)

    return queries

def processed_queries_bool(path, query):
    queries = {}
    q = []
    if query is None:
        with open(path, 'r') as file:
            contents = file.read()
            q = contents.split('\n#')
    else:
        q = [query]
    i = 0
    for qr in q:
        i += 1
        tq = qr.replace(' ','')
        tq = tq.replace('\t', '')
        tq = tq.replace('\n', '')
        tq = tq.replace("'",'')
        tq = tq.replace(';','')
        t = tq.split('=')
        queries[i] = t[1]
    return queries

def save_processed_data_json(path, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)

def load_processed_data_json(path):
    return json.loads(open(path).read())

def processed_relevance(path):
    d = []
    with open(path, 'r') as file:
        contents = file.read()
        d = contents.split('\n')
    r = {}
    for textd in d:
        text = textd.split()
        if len(text) == 3:
            if text[0] in r:
                r[text[0]].append((int(text[1]), int(text[2])))
            else:
                r[text[0]] = [(int(text[1]), int(text[2]))]
    return r