import psycopg2 as db;

class Connection():
    def __init__(self, hostname, password, username, port, database):
        self.instance = None
        self.hostname = hostname
        self.password = password
        self.username = username
        self.port = port
        self.database = database

    def getInstance(self):
        if(self.instance == None):
            try:
                connection = db.connect(database=self.database, host=self.hostname, user=self.username, password=self.password, port=self.port)
                self.instance = connection
            except:
                self.instance = None
                raise Exception("Não foi possivel se conectar ao banco de dados")
        return self.instance;
