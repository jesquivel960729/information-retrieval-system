import numpy as np
from collections import Counter
from tools.tokenizer import *
import operator
import math
import streamlit as st

class Vector_model:
    def __init__(self, docs, a = 0.4):
        self.a = a
        self.documents = docs
        self.N = len(self.documents)
        self.frequency = dict()
        self.vocabulary = []
        self.max_frecuency = dict()
        self.ni = dict()
        self.tfidf = dict()
        self.sim = []
        self.init_data()
        

    def init_data(self):
        for d in self.documents:
            terms = self.documents[d]
            f = dict()
            for term in terms:
                if term in self.ni:
                    self.ni[term].add(d)
                else:
                    self.ni[term] = {d}
                if term in f:
                    f[term] += 1
                else:
                    f[term] = 1
            if len(f) > 0:
                self.frequency[d] = f
                self.max_frecuency[d] = max(f.items(), key=operator.itemgetter(1))[1]
        self.vocabulary = [term for term in self.ni]

        for d in self.documents:
            for term in self.vocabulary:
                if d in self.frequency:
                    if term in self.frequency[d]:
                        tf = self.frequency[d][term]/self.max_frecuency[d]
                        idf = np.log(self.N / len(self.ni[term]))  
                        self.tfidf[d, term] = tf * idf

    def calculate_tfidf_query(self, query):
        terms_counter = Counter(query)
        N = len(terms_counter)
        tf_idfq = dict()
        for term in np.unique(query):
            tf = self.a + (1 - self.a)*(terms_counter[term]/terms_counter.most_common(1)[0][1])
            idf = 0
            if term in self.vocabulary:
                idf = np.log(self.N / len(self.ni[term]))
            tf_idfq[term] = tf * idf
        return tf_idfq
    
    def calculate_similarity(self, d, tfidfq):
        sum_numerator = 0
        sum_denominator1 = 0
        sum_denominator2 = 0
        for term in self.vocabulary:
            if term in self.documents[d]:
                sum_denominator1 += (self.tfidf[d, term] ** 2)
            if term in tfidfq:
                sum_denominator2 += (tfidfq[term] ** 2)
            if term in self.documents[d] and term in tfidfq:
                sum_numerator += (self.tfidf[d, term] * tfidfq[term])
            
        if sum_denominator1 == 0 or sum_denominator2 == 0 or sum_numerator == 0:
            return 0
        else:
            return sum_numerator/ (math.sqrt(sum_denominator1*sum_denominator2))

    def run_vector_model(self, query, k = 20):
        tfidfq = self.calculate_tfidf_query(query)
        sim = []
        for d in self.documents:
            simdq = self.calculate_similarity(d, tfidfq)
            sim.append(simdq)
        sim = np.array(sim)
        result = []
        if k == 0:
            result = np.array(sim).argsort()[::-1]
        else: 
            result = np.array(sim).argsort()[-k:][::-1]
        
        return [int(i+1) for i in result], [float(x) for x in (sim[result])]

    def calculate_precision(self, q, rel, rec):
        precision = []
        for index in range(q):
            i = str(index + 1)            
            # number of relevant documents retrieved
            RR = 0
            if i in rel and i in rec:
                RR = len([x for x in rel[i][0] if x in rec[i][0]])
            else:
                precision.append(0)
                continue
            
            # total number of documents retrieved
            p = RR / len(rec[i])
            precision.append(p)
        return precision

    def calculate_recovery(self, q, rel, rec):
        recovery = []
        for index in range(q):
            i = str(index + 1)            
            # number of relevant documents retrieved
            RR = 0
            if i in rel and i in rec:
                RR = len([x for x in rel[i][0] if x in rec[i][0]])
            else:
                recovery.append(0)
                continue
            
            # total number of documents retrieved
            r = RR / len(rel[i])
            recovery.append(r)
        return recovery

    def calculate_measure_f(self, p, r, beta = 1):
        f = []
        for i in range(len(p)):
            if p[i] == 0 or r[i] == 0:
                f.append(0.0)
            else:
                n = (1 + (beta**2))*p[i]*r[i]
                d = (beta**2)*p[i] + r[i]
                f.append(n/d)
        return f 

    def calculate_measures(self, q, rel, rec, k = 20):
        st.subheader(f'Primeros {k} documentos de la lista de ranking')
        p = self.calculate_precision(q, rel, rec)
        r = self.calculate_recovery(q, rel, rec)
        f = self.calculate_measure_f(p, r, beta=1) #cuando beta = 1 se calcula medida f1

        for i in range(q):
            st.write(f'Consulta # {(i + 1)} => Precisión : {round(p[i], 4)} , Recobrado : {round(r[i], 4)} , Medida F1 : {round(f[i], 4)}')

        st.write(f'Promedio Precisión: {round(np.mean(p), 4)}')
        st.write(f'Promedio Recobrado: {round(np.mean(r), 4)}')
        st.write(f'Promedio Medida F1: {round(np.mean(f), 4)}')
