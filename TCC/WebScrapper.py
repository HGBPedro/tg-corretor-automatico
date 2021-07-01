import urllib.request
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup

def obterTemasRedacoes(): 
    url = "https://educacao.uol.com.br/bancoderedacoes/"
    driver = webdriver.Chrome()
    cssclass = 'ver-mais'
    driver.get(url)
    driver.minimize_window()
    links = []

    while True:
        try:
            driver.find_element(By.CLASS_NAME, cssclass).click()
            print('clicou')
        except ElementClickInterceptedException:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            driver.find_element(By.CLASS_NAME, cssclass).click()
        except NoSuchElementException:
            break
        except StaleElementReferenceException:
            driver.refresh()
            print('recarregou a pagina') 

    body = driver.find_element(By.TAG_NAME, 'body')
    innerBody = body.get_attribute("innerHTML")
    soup = BeautifulSoup(innerBody, 'html5lib')
    divs = soup.findAll('div', {'class': 'thumbnails-wrapper'})

    for link in divs:
        links.append(link.find('a').get('href'))
    
    print('quantidade de links:', len(links))
    driver.quit()
    return links

def acessarRedações(links):
    redacoes = []

    for temas in links:
        page = urllib.request.urlopen(temas)
        soup = BeautifulSoup(page, 'html5lib')

        divs = soup.findAll('div', {'class': 'rt-line-option'})

        for redacao in divs:
            if int(redacao.find('span', {'class': 'points'}).string) > 650:
                redacoes.append(redacao.find('a').get('href'))

    print('Links obtidos: ', len(redacoes))
    return redacoes

def obterTextos(redacoes):
    textos = []
    fileRedacoes = open('E:\\TCC\\Redacoes.txt', 'a', encoding='utf-8')
    redacoesTagged = open('E:\\TCC\\RedacoesTagged.txt', 'a', encoding='utf-8')
    big = open('E:\\TCC\\big.txt', 'a', encoding='utf-8')

    for texto in redacoes:
        page = urllib.request.urlopen(texto)
        soup = BeautifulSoup(page, 'html5lib')

        conteudoTexto = soup.find('div', {'class': 'text-composition'})

        try:
            strongs = conteudoTexto.find_all_next('strong')

            for item in strongs:
                conteudoTexto.find_next('strong').decompose()
        except AttributeError:
            continue
        
        textos.append(conteudoTexto.get_text())
        textos.append('\n\n')

    for item in textos:    
        fileRedacoes.write(item)
        redacoesTagged.write(item)
        big.write(item)
    
    return print('\n Quantidade de textos: ', len(textos), '\n fim')

links = obterTemasRedacoes()

redacoes = acessarRedações(links)

obterTextos(redacoes)
