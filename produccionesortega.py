# -*- coding: utf-8 -*-
import scrapy
import time
import requests
import selenium
from Selenium import abre_navegador
from datetime import date
from verifica_link import veri, separa_titulo, separa
from controlador_vista import ModelSQLite, View, Controler

class produccionesortega(scrapy.Spider):
    name = 'produccionesortega'
    _num_pagina = 1
    start_urls = ['http://produccionesortega507.com']
    
    id_domin = 6
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
            #id_trelacion = c.ultimo_id(self.nombre_trelacion)
            self.c.inserta_item_relacional(self.id_domin, self.start_urls[0], hoy, self.nombre_trelacion)
       
            
            
    def parse(self, response):
        id = '0'
        #####COMENTARIOS#####
        print('\n########Pagina ' + str(self._num_pagina) + '########')
        for art in response.xpath('//*[@id="content"]/div[1]/article'):
            band = True
            titulo = art.css(' h2 > a ::text').get()
            fecha = art.css('p > span > a ::text').get()
            album, cantante = separa_titulo(titulo, '-')
            referer = art.css('div > div.post-entry-content > a ::attr(href)').get()
            id = self.get_id(referer,'/', 3)
            infringing = self.get_infr(id)
            if referer is None:
                referer = art.css('div > div > p > strong > a ::attr(href)').get()
                if referer is None:
                    #print('PATH: ' + str(art.xpath('//div/div/p[2]/a').extract()))
                    #print('A: ' + str(art.css('div.post-entry-content').get()))
                    for p in art.css('div.post-entry-content > strong > span > span > a') or art.css('div.post-entry-content > p > a'):
                        band = False
                        #print ('A: ' + str(art.css('div.post-entry-content').get()))
                        referer = p.css('::attr(href)').get()
                        id = self.get_id(referer,'/', 3)
                        infringing = self.get_infr(id)
                        #print('REF: ' + referer)
                        if self.comprueba_refer(referer, 'open') == True:
                            r = art.css('div.post-entry-content > p')
                            #print('A: ' + str(art.css('div.post-entry-content > p > strong').get()))
                            if r.css('strong') is not None:
                                r = r.css('strong > span')
                            referer = r.css('a ::attr(href)').get()
                            id = self.get_id(referer,'/', 3)
                            infringing = self.get_infr(id)
                            #####INSERTA EN BD#####
                            if veri(infringing) == True:
                                if self.c.existe_inf(infringing, self.id_domin) == False:
                                    self.c.inserta_item(titulo, cantante, album, referer, infringing, fecha, self.id_domin)
                            
                        else:
                            id = self.get_id(referer,'/', 3)
                            infringing = self.get_infr(id)
                        self.imprime_datos(titulo, fecha, cantante, album, referer, infringing)
                else:
                    id = self.get_id(referer,'/', 3)
                    infringing = self.get_infr(id)
            else:
                if self.comprueba_refer(referer, '?') == True:
                    infringing = self.get_Mega(referer)
                    
            if band == True:
                #####INSERTA EN BD#####
                if veri(infringing) == True:
                    if self.c.existe_inf(infringing, self.id_domin) == False:
                        self.c.inserta_item(titulo, cantante, album, referer, infringing, fecha, self.id_domin)
    
            self.imprime_datos(titulo, fecha, cantante, album, referer, infringing)
            #referer = None

        self._num_pagina+=1
        try:
            next_page = response.css('a.next.page-numbers ::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, callback= self.parse)
        except:
             print('Hubo un problema al abrir la página siguiente')
        
    
    def comprueba_refer(self, ref, cad):
        if ref.find(cad) != -1:
            return True
        else:
            return False
    
    
    def get_Mega(self,ref):
        driver = abre_navegador()
        driver.get(ref)
        time.sleep(8)
        return driver.current_url
    
    
    def imprime_datos(self, titulo, fecha, cantante, album, referer, infringing):
        #####IMPRIME INFORMACIÓN#####
            print('\n*****************DATOS*****************')
            print('infringing: ' + infringing)
            print('referer: ' + str(referer))
            print('titulo: ' + titulo)
            print('fecha: ' + fecha)
            print('cantante: ' + cantante)
            print('album: ' + album)
            print('***************************************\n')
            
    def get_id(self, id, separador, pos):
        if id is not None:
            n_id = id.split(separador)
            return str(n_id[pos])
        else:
            return ''
    
    def get_infr(self, id):
        if id is not None or id != '0':
            response = requests.get('https://musica.produccionesortega507.com/d.php?id=' + id , stream=True)
            #print (response.headers)
            return str(response.request.url)
        else:
            return ""
