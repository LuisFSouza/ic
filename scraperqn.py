import requests as req
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import re
import os
import psycopg2

def writeInFile(text):
    with open('saidas.txt', 'a', encoding='utf-8') as arquivo:
        arquivo.write(text+"\n")

conexao = psycopg2.connect(host="localhost", user="postgres", password="1234", database="quimicanova")
cursor = conexao.cursor()

chromeOptions = webdriver.ChromeOptions()
chromeOptions.binary_location="./chrome-win64/chrome.exe"
chromeService = webdriver.ChromeService(executable_path="./chromedriver-win64/chromedriver.exe")
navegador = webdriver.Chrome(options=chromeOptions, service=chromeService)
navegador.get("https://quimicanova.sbq.org.br/edicoes_anteriores.asp")
sleep(3)

qnsite = BeautifulSoup(navegador.page_source, 'html.parser')

naoEncontrados = []

divConteudo = qnsite.find('div', id='conteudo')
if divConteudo:
    tabela = divConteudo.find('table')
    if tabela:
        volumes =  tabela.find_all('tr')
        for volume in volumes[1:-1]:
            tds = volume.find_all('td');
            if tds:
                tdAno = tds[0]
                anoA = tdAno.find('a')

                tdVolume = tds[1];
                volumeA = tdVolume.find('a')
                if volumeA:
                    edicoes = tds[2:];

                    for edicao in edicoes:
                        edicaoA = edicao.find('a')
                        if edicaoA:
                            aux = str(edicaoA)
                            aux = aux.split('>', 1)[1];
                            aux = aux.split('<', 1)[0];
                            edicao = aux;

                            writeInFile("***/***/***" +volumeA.text + "-" + edicao)

                            href = edicaoA.get('href')
                            navegador.execute_script("window.open('')")
                            navegador.switch_to.window(navegador.window_handles[1])
                            navegador.get("https://quimicanova.sbq.org.br/"+href);
                            sleep(3)

                            articlesSite = BeautifulSoup(navegador.page_source, 'html.parser')

                            divConteudo = articlesSite.find('div', id='conteudo');
                            
                            if divConteudo:
                                divArtigos = divConteudo.find_all('div', attrs={'class', 'artigosLista'});
                                if divArtigos:
                                    for artigo in divArtigos:
                                        divPrincipal = artigo.find('div', attrs={'class', 'margem_artigo'});
                                        if divPrincipal:
                                            h3Titulo = divPrincipal.find('h3');
                                            titulo = h3Titulo.text
                                            writeInFile(titulo)
                                        else:
                                            divArtigosInterior = artigo.find('div', attrs={'class', 'artigosLista'});
                                            if divArtigosInterior:
                                                h3Titulo = divArtigosInterior.find('h3');
                                                titulo = h3Titulo.text
                                                writeInFile(titulo)
                                    if(int(volumeA.text) <= 17):
                                        tipo = ''
                                        for artigo in divArtigos:
                                            spanSecao = artigo.find('span', attrs={'class', 'secao'});
                                            if spanSecao:
                                                tipo=spanSecao.text;

                                            if tipo=="Artigo" or tipo=="Revisão":
                                                divPrincipal = artigo.find('div', attrs={'class', 'margem_artigo'});
                                                if divPrincipal:
                                                    h3Titulo = divPrincipal.find('h3');
                                                    titulo = h3Titulo.text

                                                pAutores = divPrincipal.find('p', attrs={'class', 'autores'})
                                                autores = pAutores.text
                                                autores = re.split(', | e | and ', autores)

                                                whereClauses = (titulo, int(anoA.text), int(volumeA.text), edicao)
                                                cursor.execute("select titulo from artigos where titulo=%s and ano=%s and volume=%s and numero=%s", whereClauses)
                                                resultados = cursor.fetchall()

                                                autores = ';'.join(autores);

                                                infos = artigo.find('span', attrs={'class', 'pagina'});
                                                rangePage = infos.text.replace('\n', '')
                                                rangePage = rangePage.replace(' ', '')
                                                rangePage = rangePage.split(',')[2]
                                                rangePage = rangePage.split('-')
                                                paginaInicial = None;
                                                if(len(rangePage)>0 and rangePage[0] != ''):
                                                    paginaInicial = rangePage[0]
                                                paginaFinal = None;
                                                if(len(rangePage) == 2 and rangePage[1] != ''):
                                                    paginaFinal = rangePage[1]

                                                if(resultados):
                                                    update=None;
                                                    if(tipo=="Artigo"):
                                                        update = ("Article", autores, paginaInicial, paginaFinal, titulo, int(anoA.text), int(volumeA.text), edicao)
                                                    else:
                                                        update=("Review", autores, paginaInicial, paginaFinal, titulo, int(anoA.text), int(volumeA.text), edicao)
                                                    cursor.execute("update artigos set tipo=%s, autores=%s, pagina_inicial=%s, pagina_final=%s where titulo=%s and ano=%s and volume=%s and numero=%s", update)
                                                    conexao.commit();
                                                    print("Atualizado para " + tipo)
                                                else:
                                                    naoEncontrados.append(whereClauses)

                            navegador.close();
                            navegador.switch_to.window(navegador.window_handles[0]) 

navegador.close()

with open("falhas.txt", 'w', encoding="utf-8") as arquivo:
    for item in naoEncontrados:
        arquivo.write(f'{item}\n')

conexao.close();