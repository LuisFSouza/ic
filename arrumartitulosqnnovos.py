import psycopg2
titulos = []

with open('saidas.txt', 'r', encoding='utf-8') as arquivo:
    for linha in arquivo:
        if(linha[:11] != '***/***/***'):
            titulos.append(linha.rstrip('\n'))

def buscarTitulo(titulo):
    for t in titulos:
        if(t.lower() == titulo):
            return t

conexaobasenova = psycopg2.connect(host="localhost", user="postgres", password="1234", database="qnnovo")
cursorbasenova = conexaobasenova.cursor()

cursorbasenova.execute("select cod, titleqn from documents where yearpublished >= 1995")

for resultado in cursorbasenova.fetchall():
    cod = resultado[0]
    titulobusca = resultado[1]

    cursorbasenova.execute("UPDATE documents SET titleqn=%s where cod=%s", (buscarTitulo(titulobusca), cod, ))
    conexaobasenova.commit()
    
cursorbasenova.close();
conexaobasenova.close();