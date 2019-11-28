# -*- coding: utf-8 -*-
import time
import requests
from selenium import webdriver
from urllib.parse import quote
from controlador_vista import ModelSQLite,Controler,View


def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    try:
        h = requests.head(url, allow_redirects=True)
        header = h.headers
        content_type = header.get('content-type')
    except:
        return False
    if 'text' in content_type.lower():
        return False
    if 'html' in content_type.lower():
        return False
    return True



c = Controler(ModelSQLite(),View())
Artistas = c.get_artista("itunes_artist")
for art in Artistas:
    search_word = quote(art[0] + ' descarga directa lang:es')
    #print(art[0])
    #print(search_word)
    url = r'https://twitter.com/search?q='+ str(search_word) +'&src=typed_query'
    driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
    driver
    driver.get(url)
    try:
        driver.find_element_by_css_selector("input.text-input.email-input.js-signin-email").send_keys('jguerrero@apdif.com.mx')
        driver.find_element_by_name("session[password]").send_keys('$Apd1f')
        driver.find_element_by_css_selector("input.EdgeButton.EdgeButton--primary.EdgeButton--medium.submit.js-submit").click()
    except:
        pass
    time.sleep(5)
    ## TOMA LOS TWEETS
    for article in driver.find_elements_by_css_selector('article'):
        Hash = ""
        try:
            href = article.find_element_by_css_selector('div.css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0 > a').get_attribute('title')
        except:
            pass
        #print('HREF: ' + href)
        if is_downloadable(href) == True:
            usuario = article.find_element_by_css_selector('div.css-901oao.css-bfa6kz.r-1re7ezh.r-18u37iz.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-qvutc0 > span').text
            fecha = article.find_element_by_css_selector('time').text
            texto = article.find_element_by_css_selector('div.css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0').text
            try:
                for a in article.find_elements_by_css_selector('article span.r-18u37iz > a'):
                    Hash += a.text + ","
            except:
                pass
            print('------------------------------------------------------------------------')
            print('Fecha: ' + fecha)
            print('Usuario: ' + usuario)
            print('Infringing: ' + href)
            print('Referer: ' + url)
            print('Hashtag: ' + Hash)
            print('Texto: ' + '\n' +texto)
            print('------------------------------------------------------------------------')
            if c.existe_inf(href) == False:
                c.crea_item(usuario, texto, Hash, url, href, fecha)
        #except:
        #    pass
    time.sleep(1)
    driver.close()