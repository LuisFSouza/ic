import requests as req;
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from articleError import ArticleError
from article import Article
import traceback
from selenium.common.exceptions import NoSuchElementException

vetorErros = []
with open('articlesErrors.txt', 'r', encoding="utf-8") as arquivo:
    for linha in arquivo:
        if(linha.startswith("WOS")):
            vetorErros.append(linha.split(' ')[0])

for o in vetorErros:
    url = 'https://api.clarivate.com/apis/wos-starter/v1/documents'

    headers = {'X-ApiKey': 'key'}

    params = {'q': 'UT='+o}

    articlesResponse = (req.get(url, headers=headers, params=params)).json();

    articlesSearchError = []

    navegador = None

    for article in articlesResponse["hits"]:
        try:
            articleLink = article["links"]["record"]
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.binary_location="./chrome-win64/chrome.exe"
            chromeOptions.add_argument('--no-sandbox')
            chromeService = webdriver.ChromeService(executable_path="./chromedriver-win64/chromedriver.exe")
            navegador = webdriver.Chrome(options=chromeOptions, service=chromeService)
            navegador.get(articleLink)

            sleep(5)

            try:
                btnAcceptCookies = navegador.find_element(By.ID, "onetrust-accept-btn-handler")
                if(btnAcceptCookies):
                    navegador.execute_script('arguments[0].click()', btnAcceptCookies)
            except NoSuchElementException:
                print("Não aceitou cookies")

            btnViewMore = navegador.find_element(By.ID, "HiddenSecTa-showMoreDataButton")
            if(btnViewMore):
                navegador.execute_script('arguments[0].click()', btnViewMore)

                sleep(1)

                wosSite = BeautifulSoup(navegador.page_source, 'html.parser')

                divAbstract = wosSite.find('div', attrs={'class', 'abstract--instance'})
                    
                if(divAbstract):
                    abstract = divAbstract.find('p')
                    if(abstract):
                        article["abstract"] = abstract.text

                language = wosSite.find('span', id="HiddenSecTa-language-0")
                if(language):
                    article["languageByWoS"] = language.text


                if("doi" in article["identifiers"]):
                    navegador.get("https://search.scielo.org/?q=*&lang=pt&filter[journal_title][]=Qu%C3%ADmica%20Nova")
                
                    sleep(5)

                    textArea = navegador.find_element(By.NAME, "q[]")
                    if(textArea):
                        textArea.send_keys(article["identifiers"]["doi"])
                        sleep(1)

                        btnSearch = navegador.find_element(By.NAME, "search_button")
                        if(btnSearch):
                            btnSearch.click()
                            sleep(3)
                            
                            scieloSite = BeautifulSoup(navegador.page_source, 'html.parser')
                            divLanguages = scieloSite.find('div', attrs={'class', 'line versions'})
                            if(divLanguages):
                                spansLanguages = divLanguages.find_all("span")
                                if(spansLanguages):
                                    language = spansLanguages[2].find("a")
                                    if(language):
                                        article["languageByScielo"] = language["data-original-title"]
        
            title = BeautifulSoup(article["title"], 'html.parser').text
            article["title"] =  title

            totalCitations = 0
            for citation in article["citations"]:
                totalCitations += citation["count"]

            authors = []
            for author in article["names"]["authors"]:
                authors.append(author["displayName"])

            language = None;
            if("languageByScielo" in article):
                if(article["languageByScielo"] == "Inglês"):
                    language = 'en'
                elif(article["languageByScielo"] == "Espanhol"):
                    language = 'es'
                elif(article["languageByScielo"] == "Português"):
                    language = 'pt'

            doi = None;
            if("doi" in article["identifiers"]):
                doi = article["identifiers"]["doi"]

            abstract = None;
            if("abstract" in article):
                abstract = article["abstract"]

            issueDocument = None;
            if("issue" in article["source"]):
                issueDocument = article["source"]["issue"];
            
            rangeA = None;
            if("range" in article["source"]["pages"]):
                rangeA = article["source"]["pages"]["range"];
            
            types = article["sourceTypes"];
            typeA = None;
            if "Article" in types:
                typeA = "Article";
            else:
                if "Review" in types:
                    typeA = "Review"
            
            volumeA = None;
            if("volume" in article["source"]):
                volumeA = article["source"]["volume"];
            
            articleObj = Article(article["title"], typeA,  authors, totalCitations, article["keywords"]["authorKeywords"], abstract, language, rangeA, volumeA, issueDocument, doi, article["source"]["publishYear"])
        
            articleObj.save()
            navegador.close()

        except Exception as error:
            navegador.close()
            articleError = ArticleError(article["uid"], traceback.format_exc())
            articleError.saveError()
