# -*- coding: utf-8 -*-
import scrapy
import time
from datetime import date
from verifica_link import veri, separa_titulo, separa
from controlador_vista import ModelSQLite, View, Controler

class manuelturizoadn(scrapy.Spider):
    name = 'manuelturizoadn'
    _num_pagina = 1
    start_urls = ['https://downloadmanuelturizoadn.wordpress.com']
    
    id_domin = 5
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
        #####TOMA LOS DATOS DE LA PÁGINA#####
        titulo = response.css('h1.entry-title ::text').get()
        referer = response.css('figure > a ::attr(href)').get()
        fecha = response.css('time.entry-date.published.updated ::text').get()
        cantante, album = separa_titulo(titulo, '–')
        album = separa(album,' ', 1)
        
        #####LLAMA AL REFERER#####
        yield scrapy.Request(referer, callback= self.parse_attr, meta= {'fecha': fecha, 'referer': referer, 'titulo': titulo, 'cantante': cantante, 'album': album})
        
        
    def parse_attr(self, response):
        inf = response.css('button#download-btn ::attr(onclick)').get()
        infringing = separa(inf, "'", 1)
        
        for tb in response.css('td.column-title ::text'):
            titulo = tb.get()
            print('\n*****************DATOS*****************')
            print('infringing: ' + infringing)
            print('referer: ' + response.meta['referer'])
            print('titulo: ' + titulo)
            print('fecha: ' + response.meta['fecha'])
            print('cantante: ' + response.meta['cantante'])
            print('album: ' + response.meta['album'])
            print('***************************************\n')
            
            #####INSERTA EN BD#####
            if veri(infringing) == True:
                self.c.inserta_item(titulo, response.meta['cantante'], response.meta['album'],response.meta['referer'], infringing, response.meta['fecha'], self.id_domin)