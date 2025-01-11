import re
import pandas as pd
from collections import Counter
from datetime import datetime
import pickle
import math

class Document:
    def __init__(self, titre, auteur=None, date=None, texte=None, source=None):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.texte = texte
        self.source = source

    def __repr__(self):
        return f"Document(titre={self.titre}, auteur={self.auteur}, date={self.date}, texte={self.texte[:30]}..., source={self.source})"

class Author:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Author(name={self.name})"

class DocumentFactory:
    @staticmethod
    def create_document(row):
        titre = row['descr']
        auteur = row['speaker']
        date = datetime.strptime(row['date'], '%B %d, %Y').strftime('%Y/%m/%d')
        texte = row['text']
        source = row.get('source', None)
        return Document(titre, auteur, date, texte, source)

class Corpus:
    def __init__(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.longueChaineDeCaracteres = ""

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = {"name": doc.auteur, "documents": []}
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]]["documents"].append(doc)
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
        self.longueChaineDeCaracteres += " " + doc.texte

    def get_documents(self, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":
            docs = sorted(docs, key=lambda x: x.titre.lower())
        elif tri == "123":
            docs = sorted(docs, key=lambda x: x.date)
        return docs

    def afficher_documents(self, tri="abc"):
        docs = self.get_documents(tri)
        for doc in docs:
            print(doc)

    def save(self, filename):
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    def search(self, query):
        return [doc for doc in self.id2doc.values() if query in doc.texte]

    def concorde(self, query, context_size=30):
        matches = re.finditer(rf".{{0,{context_size}}}{query}.{{0,{context_size}}}", self.longueChaineDeCaracteres)
        data = []
        for match in matches:
            start, end = match.span()
            left_context = self.longueChaineDeCaracteres[max(0, start-context_size):start]
            right_context = self.longueChaineDeCaracteres[end:end+context_size]
            data.append([left_context, match.group(), right_context])
        return pd.DataFrame(data, columns=["contexte gauche", "motif trouvé", "contexte droit"])

    @staticmethod
    def nettoyer_texte(texte):
        texte = texte.lower()
        texte = re.sub(r'\n', ' ', texte)
        texte = re.sub(r'[^\w\s]', '', texte)
        texte = re.sub(r'\d', '', texte)
        return texte

    def stats(self, n=10):
        vocabulaire = Counter()
        doc_freq = Counter()
        for doc in self.id2doc.values():
            mots = set()
            texte_nettoye = self.nettoyer_texte(doc.texte)
            for mot in texte_nettoye.split():
                vocabulaire[mot] += 1
                mots.add(mot)
            for mot in mots:
                doc_freq[mot] += 1
        freq = pd.DataFrame.from_dict(vocabulaire, orient='index', columns=['term frequency'])
        freq['document frequency'] = pd.Series(doc_freq)
        print(f"Nombre de mots différents : {len(vocabulaire)}")
        print(f"Les {n} mots les plus fréquents :")
        print(freq.nlargest(n, 'term frequency'))

    def compare_corpora(self, corpus2, query):
        results1 = self.search(query)
        results2 = corpus2.search(query)
        common = set([doc.texte for doc in results1]) & set([doc.texte for doc in results2])
        specific1 = set([doc.texte for doc in results1]) - common
        specific2 = set([doc.texte for doc in results2]) - common
        return common, specific1, specific2

    def temporal_analysis(self, query):
        results = self.search(query)
        date_counts = {}
        for doc in results:
            date = doc.date.split('-')[0]  # Extraire l'année
            if date not in date_counts:
                date_counts[date] = 0
            date_counts[date] += 1
        return date_counts

    def tf_idf(self, query):
        tf = Counter()
        df = Counter()
        for doc in self.id2doc.values():
            texte_nettoye = self.nettoyer_texte(doc.texte)
            mots = texte_nettoye.split()
            tf.update(mots)
            df.update(set(mots))
        N = len(self.id2doc)
        tf_idf_scores = {word: (tf[word] / len(tf)) * math.log(N / (df[word] + 1)) for word in tf}
        return tf_idf_scores

    def okapi_bm25(self, query, k1=1.5, b=0.75):
        tf = Counter()
        df = Counter()
        doc_lengths = []
        for doc in self.id2doc.values():
            texte_nettoye = self.nettoyer_texte(doc.texte)
            mots = texte_nettoye.split()
            tf.update(mots)
            df.update(set(mots))
            doc_lengths.append(len(mots))
        N = len(self.id2doc)
        avg_doc_length = sum(doc_lengths) / N
        bm25_scores = {}
        for word in tf:
            idf = math.log((N - df[word] + 0.5) / (df[word] + 0.5))
            for doc in self.id2doc.values():
                texte_nettoye = self.nettoyer_texte(doc.texte)
                mots = texte_nettoye.split()
                tf_word = mots.count(word)
                doc_length = len(mots)
                score = idf * ((tf_word * (k1 + 1)) / (tf_word + k1 * (1 - b + b * (doc_length / avg_doc_length))))
                if word not in bm25_scores:
                    bm25_scores[word] = 0
                bm25_scores[word] += score
        return bm25_scores

class SearchEngine:
    def __init__(self, corpus):
        self.corpus = corpus

    def search(self, query, top_n=None):
        results = self.corpus.search(query)
        if top_n:
            results = results[:top_n]
        return results

    def search_with_filters(self, query, author=None, date=None, start_date=None, end_date=None, top_n=None):
        results = self.corpus.search(query)
        if author:
            results = [doc for doc in results if doc.auteur == author]
        if date:
            results = [doc for doc in results if doc.date == date]
        if start_date and end_date:
            results = [doc for doc in results if start_date <= doc.date <= end_date]
        if top_n:
            results = results[:top_n]
        return results
