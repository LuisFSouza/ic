from connection import Connection
from similarity import cosi_similarity
from traduction import translate
from time import sleep
from functions import getSimilarityValueFromTuple
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

class Article():
 
    authors=[]
    keywords=[]

    def __init__(self, title, typeDoc, authors, citations, keywords, abstract, language, rangeDoc, volume, issue, doi, year):
        self.keywords=[]
        self.authors=[]
        self.setTitle(title)
        self.setType(typeDoc)
        self.setAuthors(authors)
        self.setCitations(citations)
        self.setKeywords(keywords)
        self.setAbstract(abstract)
        self.setLanguage(language)
        self.setRange(rangeDoc)
        self.setVolume(volume)
        self.setIssue(issue)
        self.setDoi(doi)
        self.setYear(int(year)) 
    
    def getTitle(self):
        return self.title

    def getType(self):
        return self.type

    def getAuthors(self):
        return self.authors;

    def getCitations(self):
        return self.citations

    def getKeywords(self):
        return self.keywords

    def getAbstract(self):
        return self.abstract
    
    def getDoi(self):
        return self.doi
    
    def getIssue(self):
        return self.issue

    def getVolume(self):
        return self.volume

    def getRange(self):
        return self.range
    
    def getYear(self):
        return self.year
    
    def getLanguage(self):
        return self.language

    def setTitle(self, title):
        self.title = title.lower()

    def setType(self, type):
        if(type != None):
            self.type = type.lower()
        else:
            self.type = None;
    def setAuthors(self, authors):
        self.authors = authors

    def setCitations(self, citations):
        if(citations != None and isinstance(citations, int)):
            self.citations = citations
        else:
            self.citations = None

    def setKeywords(self, keywords):
        if(keywords != None and keywords != ''):
            for keyword in keywords:
                self.keywords.append(keyword.lower())
        else:
            self.keywords = None
        
    def setAbstract(self, abstract):
        if(abstract != None):
            self.abstract = abstract.lower()
        else:
            self.abstract = None

    def setLanguage(self, language):
        self.language = language
    
    def setDoi(self, doi):
        self.doi = doi
    
    def setIssue(self, issue):
        self.issue = issue

    def setVolume(self, volume):
        self.volume = volume

    def setRange(self, range):
        self.range = range
    
    def setYear(self, year):
        if(year >= 0):
            self.year = year
        else:
            self.year = -1
    
    def save(self):
        try:
            conPrincipal = Connection('localhost', '1234', 'postgres', 5432, 'qnnovo')
            cursor = conPrincipal.getInstance().cursor()

            if(self.language == None):
                conSecundary = Connection('localhost', '1234', 'postgres', 5432, 'quimicanova')
                cursorSecundary = conSecundary.getInstance().cursor()
                whereClauses = (self.volume, self.issue)
                command = "select titulo, linguagem from artigos where volume=%s and numero=%s"
                cursorSecundary.execute(command, whereClauses)
                percentSimilarity = []

                for (title, language) in cursorSecundary.fetchall():
                    text1 = translate(title)
                    text2 = translate(self.title)
                    percentSimilarity.append((language, (cosi_similarity([text1, text2])[0][0])))

                if(len(percentSimilarity) != 0):
                    most_similarity = max(percentSimilarity, key=getSimilarityValueFromTuple)
                    self.language = most_similarity[0]
            typeDoc = None
            if(self.type != None):
                typeDoc = (self.type).lower()
            
            cleanAbstract = None;
            if(self.abstract):
                tokens =  word_tokenize(self.abstract.lower())
                stop_words = stopwords.words('english')
                clearText = [x for x in tokens if x not in stop_words]
                cleanAbstract = " ".join(word for word in clearText if word not in string.punctuation)
            
            data_insert = (self.title, self.range , self.citations, self.volume, self.issue, self.doi, self.year, self.language, typeDoc, self.abstract, cleanAbstract)
            insert_command = 'insert into documents(title, pagesrange, citations, volume, issue, doi, yearpublished, language, type, abstract, cleanabstract) values(%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s) returning cod;'
            cursor.execute(insert_command, data_insert)
            codDocument = cursor.fetchone()[0]
            if(self.keywords != None):
              
                for keyword in self.keywords:
                    whereClauses = (keyword,)
                    command = "select * from Keywords where keyword=%s"
                    cursor.execute(command, whereClauses)
                    result = cursor.fetchall()
                    if(len(result) == 0):
                        insert_command = 'insert into keywords(keyword) values (%s);'
                        data_insert = (keyword,)
                        cursor.execute(insert_command, data_insert)

                    whereClauses = (codDocument, keyword)
                    command = "select * from have where cod=%s and keyword=%s"
                    cursor.execute(command, whereClauses)
                    result = cursor.fetchall()
                    if(len(result) == 0):
                        insert_command = 'insert into Have(cod, keyword) values (%s, %s);'
                        data_insert = (codDocument, keyword)
                        cursor.execute(insert_command, data_insert)
            if(self.authors != None):
                for author in self.authors:
                    insert_command = 'insert into authors(cod, author) values (%s, %s);'
                    data_insert = (codDocument, author)
                    cursor.execute(insert_command, data_insert)

            conPrincipal.getInstance().commit()
            print("Artigo Salvo")
        except Exception:
            raise

