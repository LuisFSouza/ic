class ArticleError():
    def __init__(self, uid, error):
        self.uid = uid
        self.error = error

    def setUid(self, uid):
        self.uid = uid

    def setError(self, error):
        self.error = error
    
    def getUid(self):
        return self.uid

    def getError(self):
        return self.error

    def saveError(self):
        try:
            with open("./articlesErrors.txt", 'a', encoding='utf-8') as articlesErrors:
                articlesErrors.write(self.uid + " - " + self.error + "\n")
        except Exception as error:
            print("Não foi possivel escrever no arquivo")