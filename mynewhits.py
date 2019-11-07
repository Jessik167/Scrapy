# -*- coding: utf-8 -*-
import scrapy
import time
#from requests_html import HTMLSession
from Selenium import open_adfly, abre_navegador
from datetime import date
from selenium import webdriver
from verifica_link import veri, separa, imprime_datos
from controlador_vista import ModelSQLite, View, Controler
from docutils.nodes import title

class mynewhits(scrapy.Spider):
    name = 'mynewhits'
    _num_pagina = 1
    start_urls = ['http://mynewhits.blogspot.com/']
    
    id_domin = 10
    nombre_trelacion = 'dominios'
    #####CREA OBJETO#####
    c = Controler(ModelSQLite(), View())
    
    
    def __init__(self, name=None, **kwargs):
        #####CREA TABLA#####
        self.c.crea_tabla(self.nombre_trelacion)
        if self.c.existe_id(self.id_domin, self.nombre_trelacion) == False:
        #####TOMA LA FECHA ACTUAL#####
            hoy = date.today().strftime("%d %B, %Y")
        #####INSERTA EN LA TABLA RELACIONAL#####
            self.c.inserta_item_relacional(self.id_domin, self.start_urls[0], hoy, self.nombre_trelacion)
            
            
    def parse(self, response):
        #####COMENTARIOS#####
        print('\n########Pagina ' + str(self._num_pagina) + '########')
        for div in response.css('div.date-posts > div'):
            for a in div.css('article > div > h2 > a'):
               titulo = a.css('::attr(title)').get()
               href = a.css('::attr(href)').get()
               cantante, album = self.separa_titulo(titulo, '-')
               yield scrapy.Request(href, callback= self.parse_attr, meta= {'referer': href, 'titulo': titulo, 'cantante': cantante, 'album': album})
               #break
            #break
        self._num_pagina+=1
        try:
            driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
            #print('URL:' + str(response.url))
            time.sleep(1)
            driver.get(response.url)
            driver.find_element_by_css_selector('div.pagenavi :last-child').click()
            next_page = driver.current_url
            #print('PAGINA SIG: ' + str(next_page))
            #time.sleep(5)
            if next_page is not None:
                driver.close()
                yield response.follow(next_page, callback= self.parse)
                return
        except:
             print('Hubo un problema al abrir la página siguiente')
        
    
    def parse_attr(self, response):
        fecha = response.css('div.post-body.entry-content > div > div.post-info-icon.tanggal > span ::text').get().strip()
        prev_inf = response.xpath('//*[@class="post-body entry-content"]/div[2]/div[3]/a/@href').get()
        infringing = open_adfly(prev_inf,'span[id*="skip_button"]')
        imprime_datos(response.meta['titulo'], fecha, response.meta['cantante'], response.meta['album'], response.meta['referer'], infringing)
        #####INSERTA EN BD#####
        if self.c.existe_inf(infringing, self.id_domin) == False:
            if infringing is not None:
                #if veri(infringing) == True:
                self.c.inserta_item(response.meta['titulo'], response.meta['cantante'], response.meta['album'], response.meta['referer'], infringing, fecha, self.id_domin)
        #####INSERTA EN BD#####
        if self.c.existe_inf(prev_inf, self.id_domin) == False:
            #if veri(prev_inf) == True:
            self.c.inserta_item(response.meta['titulo'], response.meta['cantante'], response.meta['album'], response.meta['referer'], prev_inf, fecha, self.id_domin)
        
        
    def separa_titulo(self, titulo, separador):
        t = titulo.split(separador)
        cantante, album = t[0], t[1]
        return cantante,album