from similarity import cosi_similarity
from traduction import translate
from functions import getSimilarityValueFromTuple
import psycopg2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string

dicionario = {
}

with open('saidas.txt', 'r', encoding='utf-8') as arquivo:
    for linha in arquivo:
        if(linha[:11] == '***/***/***'):
            volume, edicao = (linha[11:].rstrip('\n')).split('-')
            chave = (int(volume), edicao)
        else:
            linha = linha.rstrip('\n')
            if(chave in dicionario):
                dicionario[chave].append(linha)
            else:
                dicionario[chave] = [linha]


conexao = psycopg2.connect(host="localhost", user="postgres", password="1234", database="qnnovo")
cursor = conexao.cursor()
cursor.execute("select title, volume, issue, cod from documents where yearpublished >= 1995 and titleqn is null")
for result in cursor.fetchall():
    try:
        percentSimilarity = []
        searchMatrix = []
        if(result[1] and result[2]):
            #Tem volume e edição
            searchMatrix = dicionario[(int(result[1]), str(result[2].strip()))];
        elif(result[1] and not result[2]):
            #So tem volume
            for chave in dicionario:
                if(chave[0] >=18 and chave[0] == int(result[1])):
                    searchMatrix.extend(dicionario[chave])
        elif(not result[1] and not result[2]):
            #Nao tem nenhum
            for chave in dicionario:
                if(chave[0] >= 18):
                    searchMatrix.extend(dicionario[chave])

        for title in searchMatrix:
            text1 = translate(title)
            text2 = translate(result[0])
            percentSimilarity.append((title, (cosi_similarity([text1, text2])[0][0])))

        if(len(percentSimilarity) != 0):
            most_similarity = max(percentSimilarity, key=getSimilarityValueFromTuple)
            tokens =  word_tokenize(most_similarity[0].lower())
            stop_words = set(stopwords.words('portuguese'))
            stop_words = stop_words.union(set(stopwords.words('english')))
            stop_words = stop_words.union(set(stopwords.words('spanish')))
            clearText = [x for x in tokens if x not in stop_words]
            cleanTitleQn = " ".join(word for word in clearText if word not in string.punctuation)
            cursor.execute("UPDATE documents SET titleqn=%s, cleantitleqn=%s WHERE cod=%s", (most_similarity[0].lower(), cleanTitleQn, result[3]))
            conexao.commit()
    except Exception as error:
        print("Ocorreu um erro ao atualizar o documento")
    
cursor.close()
conexao.close()
