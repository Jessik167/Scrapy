# -*- coding: utf-8 -*-
import scrapy
from datetime import date
from verifica_link import veri, separa_titulo, separa, imprime_datos
from controlador_vista import ModelSQLite, View, Controler

class lvumusic(scrapy.Spider):
    name = 'lvumusic'
    _num_pagina = 1
    start_urls = ['https://www.lvumusic.net']
    
    id_domin = 7
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
        for art in response.css('div.article-container > article'):
            href = art.css('div.featured-image > a ::attr(href)').get()
            titulo = art.css('div.featured-image > a ::attr(title)').get()
            cantante, album = separa_titulo(titulo, '–')
            fecha = art.css('div.below-entry-meta > span > a > time ::text').get()
            yield scrapy.Request(href, callback= self.parse_attr, meta= {'fecha': fecha, 'titulo': titulo, 'cantante': cantante, 'album': album})    
            #break
        self._num_pagina+=1
        try:
            next_page = response.css('li.previous > a ::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, callback= self.parse)
        except:
             print('Hubo un problema al abrir la página siguiente')
        
        
    def parse_attr(self, response):
        href = response.css('div.entry-content.clearfix > center > a ::attr(href)').get()
        yield scrapy.Request(href, callback= self.parse_attr2, meta= {'fecha': response.meta['fecha'], 'titulo': response.meta['titulo'], 'cantante': response.meta['cantante'], 'album': response.meta['album']})
    
    
    def parse_attr2(self, response):
        referer = response.url
        infringing = response.css('div.post-body.entry-content > center > table > tbody > tr > td > center > a ::attr(href)').get()
        imprime_datos(response.meta['titulo'], response.meta['fecha'], response.meta['cantante'], response.meta['album'], referer, infringing)
        #####INSERTA EN BD#####
        if veri(infringing) == True:
            if self.c.existe_inf(infringing, self.id_domin) == False:
                self.c.inserta_item(response.meta['titulo'], response.meta['cantante'], response.meta['album'], referer, infringing, response.meta['fecha'], self.id_domin)     