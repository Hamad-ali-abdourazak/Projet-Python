import pytest
from datetime import datetime
from Classes import Document, NewsDocument, ArxivDocument

def test_document_creation():
    doc = Document(titre="Test Title", auteur="Test Author", date="January 1, 2023", url="http://example.com", texte="This is a test text.")
    assert doc.titre == "Test Title"
    assert doc.auteur == "Test Author"
    assert doc.date == datetime.strptime("January 1, 2023", '%B %d, %Y')
    assert doc.url == "http://example.com"
    assert doc.texte == "This is a test text."
    assert doc.type == "Document"

def test_document_afficher():
    doc = Document(titre="Test Title", auteur="Test Author", date="January 1, 2023", url="http://example.com", texte="This is a test text.")
    assert doc.afficher() == "Titre: Test Title, Auteur: Test Author, Date: 2023-01-01, URL: http://example.com, Texte: This is a test text...."

def test_document_repr():
    doc = Document(titre="Test Title", auteur="Test Author", date="January 1, 2023", url="http://example.com", texte="This is a test text.")
    assert repr(doc) == "Document(titre=Test Title, auteur=Test Author, date=2023-01-01 00:00:00, url=http://example.com, texte=This is a test text....)"

def test_news_document_creation():
    news_doc = NewsDocument(titre="News Title", auteur="News Author", date="February 1, 2023", url="http://news.com", texte="This is a news text.", source="News Source")
    assert news_doc.titre == "News Title"
    assert news_doc.auteur == "News Author"
    assert news_doc.date == datetime.strptime("February 1, 2023", '%B %d, %Y')
    assert news_doc.url == "http://news.com"
    assert news_doc.texte == "This is a news text."
    assert news_doc.source == "News Source"
    assert news_doc.type == "News"

def test_news_document_repr():
    news_doc = NewsDocument(titre="News Title", auteur="News Author", date="February 1, 2023", url="http://news.com", texte="This is a news text.", source="News Source")
    assert repr(news_doc) == "NewsDocument(titre=News Title, auteur=News Author, date=2023-02-01 00:00:00, url=http://news.com, texte=This is a news text...., source=News Source)"

def test_arxiv_document_creation():
    arxiv_doc = ArxivDocument(titre="Arxiv Title", auteur="Arxiv Author", date="March 1, 2023", url="http://arxiv.com", texte="This is an arxiv text.", category="cs.AI")
    assert arxiv_doc.titre == "Arxiv Title"
    assert arxiv_doc.auteur == "Arxiv Author"
    assert arxiv_doc.date == datetime.strptime("March 1, 2023", '%B %d, %Y')
    assert arxiv_doc.url == "http://arxiv.com"
    assert arxiv_doc.texte == "This is an arxiv text."
    assert arxiv_doc.category == "cs.AI"
    assert arxiv_doc.type == "Arxiv"

def test_arxiv_document_repr():
    arxiv_doc = ArxivDocument(titre="Arxiv Title", auteur="Arxiv Author", date="March 1, 2023", url="http://arxiv.com", texte="This is an arxiv text.", category="cs.AI")
    assert repr(arxiv_doc) == "ArxivDocument(titre=Arxiv Title, auteur=Arxiv Author, date=2023-03-01 00:00:00, url=http://arxiv.com, texte=This is an arxiv text...., category=cs.AI)"