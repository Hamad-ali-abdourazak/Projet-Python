from Classes import Author, Document, NewsDocument, ArxivDocument
import pickle
import re
import pandas as pd
from collections import Counter

class Corpus:
    _instance = None

    def __new__(cls, nom=None, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Corpus, cls).__new__(cls, *args, **kwargs)
            if nom is not None:
                cls._instance.init_singleton(nom)
        return cls._instance

    def init_singleton(self, nom):
        self.nom = nom
        self.authors = {}
        self.aut2id = {}
        self.id2doc = {}
        self.ndoc = 0
        self.naut = 0
        self.longueChaineDeCaracteres = None

    def add(self, doc):
        if doc.auteur not in self.aut2id:
            self.naut += 1
            self.authors[self.naut] = {"name": doc.auteur, "documents": []}
            self.aut2id[doc.auteur] = self.naut
        self.authors[self.aut2id[doc.auteur]]["documents"].append(doc)
        self.ndoc += 1
        self.id2doc[self.ndoc] = doc

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

    @staticmethod
    def load(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)

    def __str__(self):
        return f"Corpus '{self.nom}' avec {self.ndoc} documents et {self.naut} auteurs."

    def search(self, keyword):
        if self.longueChaineDeCaracteres is None:
            self.longueChaineDeCaracteres = " ".join([doc.texte for doc in self.id2doc.values()])
        return re.findall(rf".{{0,30}}{keyword}.{{0,30}}", self.longueChaineDeCaracteres)

    def concorde(self, keyword, context_size=30):
        if self.longueChaineDeCaracteres is None:
            self.longueChaineDeCaracteres = " ".join([doc.texte for doc in self.id2doc.values()])
        matches = re.finditer(rf".{{0,{context_size}}}{keyword}.{{0,{context_size}}}", self.longueChaineDeCaracteres)
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