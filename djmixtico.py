# -*- coding: utf-8 -*-
import scrapy
import time
from datetime import date
from verifica_link import veri, separa_titulo, separa, strip_spaces, imprime_datos
from controlador_vista import ModelSQLite, View, Controler


class djmixtico(scrapy.Spider):
    name = 'djmixtico'
    _num_pagina = 1
    start_urls = ['https://djmixtico.blogia.com/']
    
    id_domin = 12
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
        
        for a in response.css('h2 > a'):
            ref = a.css('::attr(href)').get()
            #####LLAMA AL REFERER#####
            yield scrapy.Request(ref, callback= self.parse_attr, meta= {'referer': ref})
        
        self._num_pagina+=1
        try:
            next_page = response.xpath('/html/body/main/nav[2]/ul/li[2]/a/@href').get()
            if next_page is None:
                next_page = response.xpath('/html/body/main/nav/ul/li[2]/a/@href').get()
            #print('NEXT PAGE: ' + str(next_page))
            if next_page is not None:
                yield response.follow(next_page, callback= self.parse)
        except:
             print('Hubo un problema al abrir la página siguiente')
    
    
    def parse_attr(self, response):
        titulo = response.css('h1 > a ::text').get()
        cantante, album = separa_titulo(titulo, '-')
        fecha = response.css('time > a ::text').get()
        fecha = strip_spaces(fecha)
        fecha = separa(fecha, '-', 0)
        infringing = response.css('div.post__content > p > a ::attr(href)').get()
        try:
            if infringing.find('images') > 0:
                infringing = response.xpath('//*[@id="post"]/div[2]/p/a[2]/@href').get()
            if infringing is not None or infringing.find('megaupload') > 0:
                if veri(infringing) == True:
                    imprime_datos(titulo, fecha, cantante, album, response.meta['referer'], infringing)
                    if self.c.existe_inf(infringing, self.id_domin) == False:
                        self.c.inserta_item(titulo, cantante, album, response.meta['referer'], infringing, fecha, self.id_domin)
        except:
            pass