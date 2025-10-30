import stanza
import psycopg2

stanza.download("pt")
stanza.download("en")
stanza.download("es")

portuguesNlp = stanza.Pipeline("pt")
inglesNlp = stanza.Pipeline("en")
espanholNlp = stanza.Pipeline("es")
verbos = []

conexao = psycopg2.connect(host="localhost", user="postgres", password="1234", database="qnnovo")
cursor = conexao.cursor()
cursor.execute("select titleqn, language from documents where titleqn is not null")

for item in cursor.fetchall():
    title = item[0].lower()
    if(item[1] == 'pt'):
        #Portugues
        infosTexto = portuguesNlp(title);
    elif(item[1] == 'en'):
        #Ingles
        infosTexto = inglesNlp(title);
    elif(item[1] == 'es'):  
        #Espanhol
        infosTexto = espanholNlp(title);
    else:
        continue;
    
    for frase in infosTexto.sentences:
        for palavra in frase.words:
            if(palavra.upos == "VERB"):
                tags = palavra.feats.split('|');
                formaVerbo = None;
                for tag in tags:
                    if "VerbForm" in tag:
                        formaVerbo = tag.split("=")[1]
                        
                if(formaVerbo and (formaVerbo == "Inf" or formaVerbo == "Ger")):
                    verbos.append((palavra.text, formaVerbo))

contadorGerundio = sum(1 for verbo in verbos if verbo[1] == 'Ger')
contadorInfinitivo = sum(1 for verbo in verbos if verbo[1] == 'Inf')

print(f"Quantidade de verbos no infinitivo: {contadorInfinitivo}")
print(f"Quantidade de verbos no gerúndio: {contadorGerundio}")

cursor.close()
conexao.close()