from unittest import result
import streamlit as st
from collections import deque
from collections import defaultdict
import numpy as np
from nltk.tokenize import word_tokenize
from tools.tokenizer import *

class Stack:
    def __init__(self):
        self.__list = deque()

    def push(self, key):
        self.__list.append(key)

    def pop(self):
        return self.__list.pop()

    def peek(self):
        key = self.__list.pop()
        self.__list.append(key)
        return key

    def is_empty(self):
        return len(self.__list) == 0

    def __str__(self):
        return "[" + ", ".join(self.__list) + "]"

    def __len__(self):
        return len(self.__list)

class Boolean_model:
    def __init__(self, docs):
        self.postings = defaultdict(list)
        self.documents = docs
        self.vocabulary = set()
        self.init_data()

    def init_data(self):
        for d in self.documents:
            terms = list(set(self.documents[d]))
            for term in terms:
                self.postings[term].append(int(d))
        self.vocabulary = self.postings.keys()

    def run_boolean_model(self, query):
        query_tokens = word_tokenize(query)
        query_parse = self.parse_query(query_tokens)
        matching_docs = self.evaluate_parse(query_parse)
        return matching_docs

    def evaluate_parse(self, query_parse):
        operands = Stack()
        for token in query_parse:
            if self.is_operator(token):
                right_operand = operands.pop()
                left_operand = operands.pop()
                result = self.resolve_operation(left_operand, right_operand, token)
                operands.push(result)
            else:
                token = tokenize_boolean(token)
                operands.push(self.get_bit_vector(token))

        if len(operands) != 1:
            st.warning('La consulta esta en un mal formato')
            return list()

        matching_docs = [i+1 for i in np.where(operands.peek())[0]]
        return matching_docs

    def resolve_operation(self, left, right, op):
        if op == "&":
            return left & right
        elif op == "|":
            return left | right
        else:
            return 0
    
    def get_bit_vector(self, token):
        n = len(self.documents)
        negate = False
        if token[0] == "~":
            negate = True
            token = token[1:]
        if token in self.vocabulary:
            bit_vector = np.zeros(n, dtype=bool)
            posting = self.postings[token]
            for doc_id in posting:
                bit_vector[doc_id - 1] = True
            if negate:
                bit_vector = np.invert(bit_vector)
            return bit_vector
        else:
            return np.zeros(n, dtype=bool)

    def precedence(self, token):
        __precedence = {"&": 2, "|": 1}
        try:
            return __precedence[token]
        except:
            return -1

    def is_left_bracket(self, token):
        return token == "("

    def is_right_bracket(self, token):
        return token == ")"
    
    def is_operator(self, token):
        return token == "&" or token == "|"

    def parse_query(self, tokens):
        """
        Input : ['god', '&', '(', '~child', '|', 'mother', ')']
        Output : ['god', '~child', 'mother', '|', '&']
        """
        stack = Stack()
        parse_query = list()
        for token in tokens:
            if self.is_left_bracket(token):
                stack.push(token)
            elif self.is_right_bracket(token):
                while (not stack.is_empty()) and stack.peek() != "(":
                    key = stack.pop()
                    parse_query.append(key)
                if not stack.is_empty() and stack.peek() != "(":
                    st.warning('La consulta esta en un mal formato')
                    break
                else:
                    stack.pop()
            elif self.is_operator(token):
                while not stack.is_empty() and ( self.precedence(token) <= self.precedence(stack.peek())):
                    parse_query.append(stack.pop())
                stack.push(token)
            else:
                parse_query.append(token)

        while not stack.is_empty():
            parse_query.append(stack.pop())

        return parse_query
