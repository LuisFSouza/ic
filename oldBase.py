from connection import Connection
from article import Article

connection = Connection('localhost', '1234', 'postgres', 5432, 'quimicanova')
cursor = connection.getInstance().cursor()

cursor.execute("select * from artigos where ano < 1995 and tipo='Review' or tipo='Article'")
results = cursor.fetchall()
for result in results:
    range = ''
    if result[12] != None:
        range += str(result[12])
    range += '-'
    if result[13] != None:
        range += str(result[13])

    authors = []
    for autor in result[11].split(';'):
        authors.append(autor.rstrip())

    abstract = None;
    if(result[4] != ''):
        abstract = result[4]
        abstract = abstract.split('Keywords')[0]

    article = Article(result[0], result[10], authors, result[9], result[8], abstract, result[14], range, result[2], result[3], None, result[1])
    article.save();