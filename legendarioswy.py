# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from Selenium import abre_navegador
from datetime import date
from verifica_link import veri, separa_titulo, separa, strip_spaces
from controlador_vista import ModelSQLite, View, Controler

class legendarioswy(scrapy.Spider):
    name = 'legendarioswy'
    _num_pagina = 1
    start_urls = ['https://legendarioswy.wordpress.com/']
    
    id_domin = 7
    nombre_trelacion = 'dominios'
    #####CREA OBJETO#####
    #c = Controler(ModelSQLite(), View())
    
    def parse(self, response):
        #####COMENTARIOS#####
        print('\n########Pagina ' + str(self._num_pagina) + '########')
        driver = abre_navegador()
        driver.get(response.url)
        SCROLL_PAUSE_TIME = 1
        
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        cnt = 0

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            try:
                cnt +=1
                nm = "div[class='infinite-wrap infinite-view-"+str(cnt)+"']"
                div = driver.find_element_by_css_selector(nm)
                for art in div.find_elements_by_xpath("./article"):
                    print('\n*****************DATOS*****************')
                    print(art.text)
                    print('***************************************\n')
            except:
                pass
            last_height = new_height
            driver.quit()
#             #####IMPRIME INFORMACIÓN#####
#             print('\n*****************DATOS*****************')
#             #print('infringing: ' + infringing)
#             print('referer: ' + str(referer))
#             print('titulo: ' + str(titulo))
#             print('fecha: ' + str(fecha))
#             print('cantante: ' + str(cantante))
#             print('album: ' + str(album))
#             print('***************************************\n')