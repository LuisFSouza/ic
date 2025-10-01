import psycopg2

conexaobaseantiga = psycopg2.connect(host="localhost", user="postgres", password="1234", database="quimicanova")
cursorbaseantiga = conexaobaseantiga.cursor()
conexaobasenova = psycopg2.connect(host="localhost", user="postgres", password="1234", database="qnnovo")
cursorbasenova = conexaobasenova.cursor()

cursorbasenova.execute("select cod, titleqn, yearpublished, volume, issue from documents where yearpublished < 1995")
for result in cursorbasenova.fetchall():
    try:
        cod = result[0]
        titulo = result[1]
        ano = result[2]
        volume = result[3]
        numero = result[4]

        cursorbaseantiga.execute("select titulo from artigos where lower(titulo)=%s and ano=%s and volume=%s and numero=%s", (titulo, ano, volume, str(numero).strip()))
        resultado = cursorbaseantiga.fetchall()
        if(len(resultado) > 0):
            titulonovo = (resultado[0])[0]
            cursorbasenova.execute("update documents set titleqn=%s, title=%s where cod=%s", (titulonovo, titulonovo, cod,) )
            conexaobasenova.commit()
            print("Atualizando")
        else:
            print(titulo)
    except Exception as error:
        print(error)
cursorbasenova.close();
cursorbaseantiga.close();
conexaobaseantiga.close();
conexaobasenova.close();