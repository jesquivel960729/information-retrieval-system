import streamlit as st
from tools.tokenizer import tokenize
from tools.vectorial_model import Vector_model
from tools.boolean_model import Boolean_model
from tools.crawler import Crawler
from tools.expansion_query import expansion_synonyms
from tools.processed_data import processed_corpus, load_processed_data_json, save_processed_data_json, processed_queries_vect, processed_relevance


def showOption(collection): 
    corpus = {}
    queries = {}
    corpus_path = ''
    query_path = ''
    queryb_path = ''
    if collection == 1:
        corpus_path = 'collections/cran/cran_corpus'
        query_path = 'collections/cran/cran_qry'
        relevance_path = 'collections/cran/cran_rel'
        recovery_path = 'collections/cran/cran_qrel'
    else:
        corpus_path = 'collections/cisi/cisi_corpus'
        query_path = 'collections/cisi/cisi_qry'
        relevance_path = 'collections/cisi/cisi_rel'
        recovery_path = 'collections/cisi/cisi_qrel'

    #corpus = processed_corpus(corpus_path, collection)
    #save_processed_data_json(corpus_path+'.json', corpus)
    #queries = processed_queries_vect(query_path, None)
    #save_processed_data_json(query_path+'.json', queries)
    corpus = load_processed_data_json(corpus_path+'.json')
    recovery = processed_relevance(recovery_path)

    method = st.selectbox(
        '',
        ('Escoja la forma de procesamiento', 'Modelo Vectorial', 'Modelo Booleano', 'Ejecutar todas las consultas de prueba de la colección usando el modelo vectorial'))
    if method == 'Modelo Vectorial' or method == 'Modelo Booleano':
        st.write('Realizar una consulta sobre la colección de datos')
        query = st.text_input('Consulta a realizar', '')
        if query != '':
            query_bool = query
            words = expansion_synonyms(query)
            st.write('La expansion de consultas a generado un conjunto de palabras')
            st.write(words)
            expansion = st.selectbox(
                '',
                ('Desea agregar los terminos encontrados a su consulta', 'Si', 'No')) 
            if expansion == 'Si':
                query_bool = query + ' & ' + ' & '.join(words)
                query_vect = query + ' ' + ' '.join(words)
            if st.button('Consultar'):
                if method == 'Modelo Vectorial':
                    query_token = tokenize(query_vect)
                    mv = Vector_model(corpus)
                    results, _ = mv.run_vector_model(query_token)
                    st.success('Finalizó el Modelo Vectorial')
                    st.write('Ranking de documentos')
                    st.write(results)
                elif method == 'Modelo Booleano':
                    mb = Boolean_model(corpus)
                    results = mb.run_boolean_model(query_bool)
                    st.success('Finalizó el Modelo Booleano')
                    st.write(results)
        else:
            st.warning('Es necesario que introduzca una consulta')
    elif method == 'Ejecutar todas las consultas de prueba de la colección usando el modelo vectorial':
        queries = load_processed_data_json(query_path+'.json')
        mv = Vector_model(corpus)
        relevance = load_processed_data_json(relevance_path+".json")
        # relevance = {}
        # for key in queries:
        #     documents, similarity = mv.run_vector_model(queries[key], k = 20)
        #     relevance[key] = [(documents[i], similarity[i]) for i in range(len(documents))]
        # save_processed_data_json(relevance_path + '.json', relevance)
        mv.calculate_measures(len(queries), relevance, recovery)
        
        
def main():
    st.title("SISTEMA DE RECUPERACIÓN DE INFORMACIÓN")

    collection = st.selectbox(
        '',
        ('Escoja la colección de datos que desea procesar', 'Colección Cranfield', 'Colección CISI', 'Web Crawling'))
        
    if collection == 'Colección Cranfield':
        showOption(1)
    elif collection == 'Colección CISI':
        showOption(2)
    elif collection == 'Web Crawling':
        #https://en.wikipedia.org/wiki/Computer_science
        query = st.text_input('Consulta a realizar', '')
        url = st.text_input('Url para comenzar a guiar el crawler', '')
        if st.button('Consultar en la web'):
            if query != '' and url != '':
                words = expansion_synonyms(query)
                st.write('La expansion de consultas a generado un conjunto de palabras')
                st.write(words)
                expansion = st.selectbox(
                    '',
                    ('Desea agregar los terminos encontrados a su consulta', 'Si', 'No')) 
                if expansion == 'Si':
                    query += ' ' + words
                cr = Crawler(query, url, width = 10, depth = 10, size = 10)
                cr.craw()
                st.success("Documentos Recuperados")
                st.write(cr.documents)
            else:
                st.write('Es necesario ingresar una consulta y una url')

if __name__ == '__main__':
    main()