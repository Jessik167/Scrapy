# -*- coding: utf-8 -*-
import scrapy
from datetime import date
from verifica_link import veri, separa_titulo, separa, imprime_datos
from controlador_vista import ModelSQLite, View, Controler
from docutils.nodes import title

class lamusicamp3(scrapy.Spider):
    name = 'lamusicamp3'
    _num_pagina = 1
    start_urls = ['https://lamusicamp3.com/']
    
    id_domin = 9
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
        for a in response.xpath('/html/body/div[1]/a'):
            try:
                titu = a.css('::attr(title)').get()
                if titu is not None and titu != 'Descargar' and titu != 'Ak47Full' and titu != 'iPauta' and titu != 'ElGenero' and titu != 'FlowHot':
                    ref = a.css('::attr(href)').get()
                    hoy = date.today().strftime("%d %B, %Y")
                    cantante, album = separa_titulo(titu, '–')
                    yield scrapy.Request(ref, callback= self.parse_attr, meta= {'referer': ref, 'fecha': hoy, 'titulo': titu, 'cantante': cantante, 'album': album})
            except:
                pass
        self._num_pagina+=1
        try:
            next_page = response.css('a.nextpostslink ::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, callback= self.parse)
        except:
             print('Hubo un problema al abrir la página siguiente')
           
           
    def parse_attr(self, response):
        if response.css('a.btn-dl'):
            infringing = response.css('a.btn-dl ::attr(href)').get()
            imprime_datos(response.meta['titulo'],response.meta['fecha'],response.meta['cantante'],response.meta['album'],response.meta['referer'],infringing)
            #####INSERTA EN BD#####
            if veri(infringing) == True:
                if self.c.existe_inf(infringing, self.id_domin) == False:
                    self.c.inserta_item(response.meta['titulo'], response.meta['cantante'], response.meta['album'], response.meta['referer'], infringing, response.meta['fecha'], self.id_domin)