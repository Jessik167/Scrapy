# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from cssselect.parser import parse_attrib
from Spiders.items import SpidersItem
from datetime import date
from verifica_link import veri
from controlador_vista import ModelSQLite, View, Controler


class TonyextraSpider(scrapy.Spider):
    name = 'Tonyextra'
    _num_pagina = 1
    start_urls = ['http://tonyextra.co//']
    
    id_domin = 1
    #nombre_tabla = 'links'
    nombre_trelacion = 'dominios'
          
    def __init__(self, name=None, **kwargs):
        #####CREA OBJETO#####
        c = Controler(ModelSQLite(), View())
        #####CREA TABLAS#####
        c.crea_tabla(self.nombre_trelacion)
        #c.crea_tabla(self.nombre_tabla, self.nombre_trelacion)
        if c.existe_id(self.id_domin, self.nombre_trelacion) == False:
            #####TOMA LA FECHA ACTUAL#####
            hoy = date.today().strftime("%d %B, %Y")
            #####INSERTA EN LA TABLA RELACIONAL#####
            c.inserta_item_relacional(self.id_domin, self.start_urls[0], hoy, self.nombre_trelacion)
    
    
    def parse(self, response):
        #####VARIABLE#####
        te_item = SpidersItem()
        c = Controler(ModelSQLite(), View())
        
        #####COMENTARIOS#####
        print('\n########Pagina ' + str(self._num_pagina) + '########')
        
        #####HACE UN LOOP POR PÁGINA EN BÚSCA DE LOS DATOS#####
        for art in response.css('article.post.excerpt'):
        #####IMPRIME LOS RESULTADOS####
            yield scrapy.Request(art.css('a ::attr(href)').get(), callback=self.parse_attr, meta={'item': te_item, 'controler': c})
            #break
        print('')
        
        self._num_pagina+=1
        
        for next_page in response.css('a.next.page-numbers'):
            yield response.follow(next_page, self.parse)
        
        
    def parse_attr(self, response):
        #####VARIABLE#####
        found = 0
        item = response.meta['item']
        c = response.meta['controler']
        
        #####TOMA EL ID DE LA PÁGINA#####
        post_id = response.xpath('//*[@id="page"]/div/article/div/@id').extract()[0]
        
        #####RECOLECTA LOS DATOS DE LA PÁGINA#####
        item['titulo'] = response.xpath('//*[@id="' + post_id + '"]/div/header/h1/text()').extract()[0]
        item['href'] = response.url
        item['fecha'] = response.xpath('//*[@id="'+ post_id + '"]/div/header/div/text()').extract()[0]
        
        #####SEPARA CANTANTE Y ALBUM#####
        separacion = str(item['titulo']).split('–')
        cantante, album = separacion[0], separacion[1]
        
        #####BÚSCA LA PALABRA DOWNLOAD#####
        for link in response.xpath('//a[text()="DOWNLOAD AUDIO"]/@href').extract():
            found = 1
            item['infringing'] = link
        if found == 0:
            for link in response.xpath('//a[text()="DOWNLOAD ZIP"]/@href').extract():
                item['infringing'] = link
                
        #####INSERTA EN BD#####
        if veri(item['infringing']) == True:
            if c.existe_inf(item['infringing'], self.id_domin) == False:
                c.inserta_item(str(item['titulo']), cantante, album, str(item['href']), str(item['infringing']), str(item['fecha']), self.id_domin)
        return item