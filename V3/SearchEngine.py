import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from collections import Counter
import re

class SearchEngine:
    def __init__(self, corpus):
        self.corpus = corpus
        self.vocab = self.build_vocab()
        self.mat_TF = self.build_tf_matrix()
        self.mat_TFxIDF = self.build_tfidf_matrix()

    def build_vocab(self):
        vocab = {}
        index = 0
        for doc in self.corpus.id2doc.values():
            texte_nettoye = self.nettoyer_texte(doc.texte)
            for mot in texte_nettoye.split():
                if mot not in vocab:
                    vocab[mot] = {'index': index, 'idf': 0}
                    index += 1
        return vocab

    def build_tf_matrix(self):
        num_docs = len(self.corpus.id2doc)
        num_terms = len(self.vocab)
        mat_TF = csr_matrix((num_docs, num_terms), dtype=np.float64)

        for i, doc in enumerate(self.corpus.id2doc.values()):
            term_freq = Counter(self.nettoyer_texte(doc.texte).split())
            for mot, freq in term_freq.items():
                if mot in self.vocab:
                    mat_TF[i, self.vocab[mot]['index']] = freq / len(doc.texte.split())

        return mat_TF

    def build_tfidf_matrix(self):
        num_docs = len(self.corpus.id2doc)
        mat_TFxIDF = self.mat_TF.copy()

        for mot, data in self.vocab.items():
            df = sum(1 for doc in self.corpus.id2doc.values() if mot in self.nettoyer_texte(doc.texte).split())
            idf = np.log(num_docs / (1 + df))
            self.vocab[mot]['idf'] = idf
            mat_TFxIDF[:, data['index']] *= idf

        return mat_TFxIDF

    def nettoyer_texte(self, texte):
        texte = texte.lower()
        texte = re.sub(r'\W+', ' ', texte)
        return texte

    def normalize(self, vector):
        norm = np.linalg.norm(vector)
        if norm == 0:
            return vector
        return vector / norm

    def search(self, query, top_n=10):
        query = self.nettoyer_texte(query)
        query_vector = np.zeros(len(self.vocab))
        for mot in query.split():
            if mot in self.vocab:
                query_vector[self.vocab[mot]['index']] = 1
        query_vector = self.normalize(query_vector)
        scores = self.mat_TFxIDF.dot(query_vector.T).toarray().flatten()
        top_indices = np.argsort(scores)[::-1][:top_n]
        results = [(self.corpus.id2doc[i + 1], scores[i]) for i in top_indices]
        return pd.DataFrame(results, columns=['Document', 'Score'])