from Classes import Author  # Importation de la classe Author depuis le module 'Classes'



class Corpus:
    def __init__(self, nom):
        self.nom = nom  # Le nom du corpus
        self.authors = {}  # Dictionnaire pour stocker les auteurs, avec leur ID en clé
        self.aut2id = {}  # Dictionnaire pour associer le nom de l'auteur à son ID
        self.id2doc = {}  # Dictionnaire pour stocker les documents avec un ID unique
        self.ndoc = 0  # Compteur du nombre de documents dans le corpus
        self.naut = 0  # Compteur du nombre d'auteurs dans le corpus
    def add(self, doc):

        if doc.auteur not in self.aut2id:  # Si l'auteur n'existe pas encore, on lui associe un nouvel ID
            self.naut += 1  # Incrémente le compteur des auteurs
            self.authors[self.naut] = Author(doc.auteur)  # Crée un nouvel auteur avec un ID unique
            self.aut2id[doc.auteur] = self.naut  # Associe le nom de l'auteur à l'ID nouvellement créé

        self.authors[self.aut2id[doc.auteur]].add(doc)  # Ajout du document à l'auteur correspondant

        self.ndoc += 1  # Incrémente le compteur des documents
        self.id2doc[self.ndoc] = doc  # Associe un ID unique au document dans id2doc

    def get_documents(self, tri="abc"):
        docs = list(self.id2doc.values()) # Récupère tous les documents sous forme de liste
        if tri == "abc":  # Tri alphabétique
            docs = sorted(docs, key=lambda x: x.titre.lower())  # Trie les documents par titre, insensible à la casse
        elif tri == "123":  # Tri temporel
            docs = sorted(docs, key=lambda x: x.date) # Trie les documents par date
        return docs

    def show(self, n_docs=-1, tri="abc"):
        docs = self.get_documents(tri)  # Récupère la liste des documents triés
        if n_docs > 0:
            docs = docs[:n_docs]  # Limite l'affichage aux n_docs premiers documents
        print("\n".join(map(repr, docs)))  # Affiche chaque document sous forme de chaîne de caractères

    def __repr__(self):
        docs = self.get_documents("abc") # Récupère les documents triés par titre
        return "\n".join(map(str, docs)) # Retourne tous les documents sous forme de chaîne de caractères


    def __str__(self):
        return f"Corpus '{self.nom}' avec {self.ndoc} documents et {self.naut} auteurs."

