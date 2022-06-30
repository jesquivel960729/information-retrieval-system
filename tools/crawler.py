import re
import time
from xml.etree.ElementTree import Comment
import numpy as np
from collections import Counter
from tools.tokenizer import *
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

class Crawler:

    def __init__(self, query, initial_node, width = 10, depth = 10, size = 10):
        self.width = width
        self.documents = []
        self.query = tokenize(query)
        self.vq = {}
        self.s = size
        self.depth = []
        self.links = []
        self.links_priority = []
        self.processed_links = []
        self.links.append(initial_node)
        self.links_priority.append(0)
        self.depth.append(depth)
        self.processed_node = 0
        #self.tags_start = re.compile(r"<[^<]+>")
        #self.tags_end = re.compile(r"<[^<]+>")
        #self.references = re.compile(r"\[\d+\]")

    def get_title(self, page):
        return page.title.string

    def go_to_link(self, url):
        try:
            req = urlopen(url)
            soup = BeautifulSoup(req, 'html.parser')
            return soup
        except Exception as e:
            return None

    def get_links(self, url):
        try:
            self.response = requests.get(url)
            linkList = re.findall('(?:href=")(.*?)"', self.response.content.decode('utf8'))
            return linkList
        except Exception as e:
            print(self.r + f'[-] ERROR: {e}')

    def tag_visible(self, text):
        if text.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        return True

    def get_document_info(self, page):
        title = self.get_title(page)
        text = page.findAll(text=True)
        vtext = filter(self.tag_visible, text)
        summary_text = u" ".join(t.strip() for t in vtext)
        
        return title, summary_text

    def get_relevance_node(self, terms):
        vp = {}
        for t in terms:
            try:
                vp[t].append(1)
            except:
                vp[t] = [1]

        for i in vp:
            vp[i] = len(vp[i])

        vocabulary = [term for term in vp]
        
        vq = {}
        terms2 = self.query
        for t in terms2:
            try:
                vq[t].append(1)
            except:
                vq[t] = [1]

        for i in vq:
            vq[i] = len(vq[i])

        vocabulary = vocabulary + [term for term in vq]
        v = len(vocabulary)
        wqi = np.zeros((v))
        wpi = np.zeros((v))
        terms_counter = Counter(terms)
        if len(terms_counter) == 0:
            return 0
        terms_max = terms_counter.most_common(1)[0][1]
        terms_counter2 = Counter(terms2)
        terms_max2 = terms_counter2.most_common(1)[0][1]
        for term in np.unique(vocabulary):
            #cuenta la cantidad de ocurrencias del termino en el documento
            freqij = 0
            if term in terms: 
                freqij = vp[term]
                tfij = freqij / terms_max
                ni = vp[term]
                idfi = np.log(1 / ni)            
                wpi[vocabulary.index(term)] = tfij * idfi
        
        for term in np.unique(vocabulary):
            #cuenta la cantidad de ocurrencias del termino en el consulta
            freqij = 0
            if term in terms2: 
                freqij = vq[term]
                tfij = freqij / terms_max2
                ni = vq[term]
                idfi = np.log(1 / ni)            
                wqi[vocabulary.index(term)] = tfij * idfi
        
        denominador = np.linalg.norm(wqi) * np.linalg.norm(wpi)
        if denominador == 0:
            return 0
        else:
            return np.dot(wpi, wqi) / denominador
            
    def craw(self, alpha = 1.5):
        #start_time = time.time()
        while len(self.links) > 0 and len(self.processed_links) <= self.s:
            current_node = self.links.pop()
            depth_current_node = self.depth.pop()
            priority = self.links_priority.pop()
            page = self.go_to_link(current_node)
            if page is None:
                continue
            self.processed_links.append(current_node)
            title, current_node_info = self.get_document_info(page) #depurar texto del documento
            current_node_info = tokenize(current_node_info)
            current_node_links = self.get_links(current_node) #depurar links
            current_node_potential_score = []
            current_node_relevance = self.get_relevance_node(current_node_info)
            data = {
                "link":current_node,
                "processed_document": current_node_info,
                "title": title,
                "priority": current_node_relevance
            }
            self.documents.append(data)
            
            if depth_current_node > 0:
                if current_node_relevance < 0.7: #irrelevant
                    for i in range(self.width):
                        current_node_potential_score.append(0.5)
                    for i in range(self.width, len(current_node_links)):
                        current_node_potential_score.append(0)
                else:
                    n = int(alpha*self.width)
                    for i in range(n):
                        current_node_potential_score.append(1)
                    for i in range(n, len(current_node_links)):
                        current_node_potential_score.append(0)
                for i in range(len(current_node_links)):
                    if current_node_links[i] in self.links:
                        index = self.links.index(current_node_links[i])
                        maxp = max(self.links_priority[index],current_node_potential_score[i])
                        newd = 0
                        if current_node_relevance < 0.7:
                            newd = depth_current_node
                        else:
                            newd = depth_current_node - 1
                        maxd = max(self.depth[index], newd)
                        if maxp > self.links_priority[index]:
                            node_tmp = self.links.pop(index)
                            self.links_priority.pop(index)
                            self.depth.pop(index)
                            index2 = len(self.links_priority)
                            for j in range(len(self.links_priority)):
                                if maxp > self.links_priority[j]:
                                    index2 = j
                                    break
                            self.links_priority.insert(index2, maxp)
                            self.links.insert(index2, node_tmp)
                            self.depth.insert(index2, maxd)
                        else:
                            self.depth[index] = maxd
                    else:
                        if current_node_links[i] not in self.processed_links:
                            index = len(self.links_priority)
                            for j in range(len(self.links_priority)):
                                if current_node_potential_score[i] > self.links_priority[j]:
                                    index = j
                                    break
                            self.links_priority.insert(index, current_node_potential_score[i])
                            self.links.insert(index, current_node_links[i])
                            if current_node_relevance < 0.7:
                                self.depth.insert(index, depth_current_node)
                            else:
                                self.depth.insert(index, depth_current_node - 1)
        