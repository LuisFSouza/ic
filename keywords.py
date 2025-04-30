import psycopg2
import nltk;
from nltk.corpus import stopwords;
from nltk.tokenize import word_tokenize;
import string

conexao = psycopg2.connect(host="localhost", user="postgres", password="1234", database="qnnovo")
cursor = conexao.cursor()
cursor.execute("select keyword from keywords")
resultado = cursor.fetchall()

for keyword in resultado:
	tokens = word_tokenize(keyword[0])
	stop_words = set(stopwords.words('portuguese'))
	stop_words = stop_words.union(stopwords.words('english'))
	stop_words = stop_words.union(stopwords.words('spanish'))
	cleankeyword = [x for x in tokens if x not in stop_words]
	cleankeyword = " ".join(word for word in cleankeyword if word not in string.punctuation)
	cursor.execute("UPDATE keywords SET cleankeyword=%s where keyword=%s", (cleankeyword,keyword[0],));
	conexao.commit()

cursor.close();
cursor.close()
