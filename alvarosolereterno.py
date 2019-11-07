# -*- coding: utf-8 -*-
import scrapy
from datetime import date
from verifica_link import veri, separa, imprime_datos
from controlador_vista import ModelSQLite, View, Controler

class alvarosolereterno(scrapy.Spider):
    name = 'alvarosolereterno'
    _num_pagina = 1
    start_urls = ['https://alvarosolereternoagostoalbummp3.wordpress.com/']
    
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
        referer = response.css('figure > a ::attr(href)').get()
        yield scrapy.Request(referer, callback= self.parse_attr)
        
        
    def parse_attr(self, response):
        Referer = response.url
        Artista = response.xpath('/html/body/div/div[2]/div/div[2]/span[2]/text()').extract_first()
        Album = response.xpath('/html/body/div/div[2]/div/div[2]/span[4]/text()').extract_first()
        Fecha = response.xpath('/html/body/div/div[2]/div/div[2]/span[6]/text()').extract_first()
        Infringing = response.css('div#download-btn-div :nth-child(4) ::attr(onclick)').get()
        Infringing = separa(Infringing, '"', 1)
        
        for tr in response.css('tbody > tr :nth-child(1)'):
            Cancion = tr.css('::text').get()
            #####IMPRIME INFORMACIÓN#####
            imprime_datos(Cancion, Fecha, Artista, Album, Referer, Infringing)
            #####INSERTA EN BD#####
            if self.c.existe_inf(Infringing, self.id_domin) == False:
                if veri(Infringing) == True:
                    self.c.inserta_item(Cancion, Artista, Album, Referer, Infringing, Fecha, self.id_domin)