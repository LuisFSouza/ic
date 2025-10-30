import psycopg2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

conexao = psycopg2.connect(host="localhost", user="postgres", password="1234", database="qnnovo")
cursor = conexao.cursor()
cursor.execute("select title, volume, issue, cod from documents where yearpublished < 1995")
for result in cursor.fetchall():
    tokens =  word_tokenize(result[0].lower())
    stop_words = set(stopwords.words('portuguese'))
    stop_words = stop_words.union(set(stopwords.words('english')))
    stop_words = stop_words.union(set(stopwords.words('spanish')))
    clearText = [x for x in tokens if x not in stop_words]
    cleanTitleQn = " ".join(word for word in clearText if word not in string.punctuation)
    cursor.execute("UPDATE documents SET titleqn=%s, cleantitleqn=%s WHERE cod=%s", (result[0].lower(), cleanTitleQn, result[3]))
    conexao.commit()
    
cursor.close()
conexao.close()