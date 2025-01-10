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
                    vocab[mot] = {'index': index, 'total_occurrences': 0, 'doc_count': 0}
                    index += 1
                vocab[mot]['total_occurrences'] += 1
        for doc in self.corpus.id2doc.values():
            mots = set(self.nettoyer_texte(doc.texte).split())
            for mot in mots:
                vocab[mot]['doc_count'] += 1
        return vocab

    def build_tf_matrix(self):
        rows, cols, data = [], [], []
        for doc_id, doc in self.corpus.id2doc.items():
            texte_nettoye = self.nettoyer_texte(doc.texte)
            word_counts = Counter(texte_nettoye.split())
            for mot, count in word_counts.items():
                if mot in self.vocab:
                    rows.append(doc_id - 1)  # Assurez-vous que les indices commencent à 0
                    cols.append(self.vocab[mot]['index'])
                    data.append(count)
        mat_TF = csr_matrix((data, (rows, cols)), shape=(len(self.corpus.id2doc), len(self.vocab)))
        return mat_TF

    def build_tfidf_matrix(self):
        N = len(self.corpus.id2doc)
        idf = np.log(N / (1 + np.array([self.vocab[mot]['doc_count'] for mot in sorted(self.vocab, key=lambda x: self.vocab[x]['index'])])))
        mat_TF = self.mat_TF
        mat_TFxIDF = mat_TF.multiply(idf)
        mat_TFxIDF = self.normalize(mat_TFxIDF)
        return mat_TFxIDF

    @staticmethod
    def nettoyer_texte(texte):
        texte = texte.lower()
        texte = re.sub(r'\n', ' ', texte)
        texte = re.sub(r'[^\w\s]', '', texte)
        texte = re.sub(r'\d', '', texte)
        return texte

    @staticmethod
    def normalize(matrix):
        norms = np.sqrt(matrix.multiply(matrix).sum(axis=1))
        norms[norms == 0] = 1
        return matrix.multiply(1 / norms)

    def search(self, query, top_n=10):
        query = self.nettoyer_texte(query)
        query_vector = np.zeros(len(self.vocab))
        for mot in query.split():
            if mot in self.vocab:
                query_vector[self.vocab[mot]['index']] = 1
        query_vector = self.normalize(csr_matrix(query_vector))
        scores = self.mat_TFxIDF.dot(query_vector.T).toarray().flatten()
        top_indices = np.argsort(scores)[::-1][:top_n]
        results = [(self.corpus.id2doc[i + 1], scores[i]) for i in top_indices]  # Ajustez l'index pour correspondre à l'ID du document
        return pd.DataFrame(results, columns=['Document', 'Score'])