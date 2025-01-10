import re
import pandas as pd
from collections import Counter
from Classes import Document, NewsDocument, ArxivDocument
from datetime import datetime

class Corpus:
    _instance = None

    def __new__(cls, nom, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Corpus, cls).__new__(cls, *args, **kwargs)
            cls._instance.init_singleton(nom)
        return cls._instance

    def init_singleton(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.longueChaineDeCaracteres = ""

    def add(self, doc):
        if doc.author not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = {"name": doc.author, "documents": []}
            self.aut2id[doc.author] = self.naut
        self.authors[self.aut2id[doc.author]]["documents"].append(doc)
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc
        self.longueChaineDeCaracteres += " " + doc.text

    def get_documents(self, tri="abc"):
        docs = list(self.id2doc.values())
        if tri == "abc":
            docs = sorted(docs, key=lambda x: x.title.lower())
        elif tri == "123":
            docs = sorted(docs, key=lambda x: x.date)
        return docs

    def search(self, query):
        return [doc for doc in self.id2doc.values() if query in doc.text]

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
            texte_nettoye = self.nettoyer_texte(doc.text)
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