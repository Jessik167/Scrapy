# -*- coding: utf-8 -*-
import scrapy
import time
from datetime import date
from verifica_link import veri, separa_titulo, separa, strip_accents
from controlador_vista import ModelSQLite, View, Controler

class ngleakers(scrapy.Spider):
    name = 'ngleakers'
    _num_pagina = 1
    start_urls = ['http://ngleakers.com/']
    
    id_domin = 4
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
        #####COMENTARIOS#####
        print('\n########Pagina ' + str(self._num_pagina) + '########')
        
        for art in response.css('div#main-content > article'):
            titulo = art.css('a ::attr(title)').get()
            referer = art.css('a ::attr(href)').get()
            fecha = art.css('span.mh-meta-date updated ::text').get()
            cantante, album = separa_titulo(titulo, '–')
            
            #####LLAMA AL REFERER#####
            yield scrapy.Request(referer, callback= self.parse_attr, meta= {'fecha': fecha, 'referer': referer, 'titulo': titulo, 'cantante': cantante, 'album': album})
            #break
        self._num_pagina+=1
        try:
            next_page = response.css('div.nav-previous > a ::attr(href)').get()
            #print('PAGINA SIGUIENTE:' + next_page)
            if next_page is not None:
                yield response.follow(next_page, callback= self.parse)
        except:
             print('Hubo un problema al abrir la página siguiente')
    
    
    
    def parse_attr(self, response):     
        infringing = response.css('h3 > a ::attr(href)').get()
        
        print('\n*****************DATOS*****************')
        print('infringing: ' + infringing)
        print('referer: ' + response.meta['referer'])
        print('titulo: ' + response.meta['titulo'])
        print('fecha: ' + str(response.meta['fecha']))
        print('cantante: ' + response.meta['cantante'])
        print('album: ' + response.meta['album'])
        print('***************************************\n')
        
        #####INSERTA EN BD#####
        if veri(infringing) == True:
            if self.c.existe_inf(infringing, self.id_domin) == False:
                self.c.inserta_item(response.meta['titulo'], response.meta['cantante'], response.meta['album'],response.meta['referer'], infringing, response.meta['fecha'], self.id_domin)