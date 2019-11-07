# -*- coding: utf-8 -*-
from urllib.parse import unquote
import scrapy
import time
from datetime import date
from selenium import webdriver
from builtins import input
from Selenium import open_adfly
from verifica_link import veri
from controlador_vista import ModelSQLite, View, Controler

class realmmusik(scrapy.Spider):
    name = 'realm-musik'
    _num_pagina = 1
    start_urls = ['https://realm-musik.blogspot.com/']
    
    id_domin = 3
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
        link_inf = []
        
        #####COMENTARIOS#####
        print('\n########Pagina ' + str(self._num_pagina) + '########')
        
        ids = response.xpath('//*[@id="Blog1"]/div/div/div/div/div/meta[3]/@content').extract()
        
        
        for i in range(len(ids)):
            link_inf.append(str(response.xpath('//*[@id="post-body-'+ ids[i]+'"]/div[2]/a/@href').extract_first()))
            print('\nID: ' + str(link_inf[-1]))
        
        #####HACE UN LOOP POR PÁGINA EN BÚSCA DE LOS DATOS#####
        for div in response.css('div.blog-posts.hfeed'):
            for dd in div.css('div.date-outer'):
                fecha = dd.css('span ::text').get()
                i = 0
                for d in dd.css('div.post.hentry'):
                    referer = d.css('h3.post-title.entry-title > a ::attr(href)').get()
                    titulo = d.css('h3.post-title.entry-title > a ::text').get()
                    cantante, album = self.separa(titulo)
                    try:
                        yield scrapy.Request(url= link_inf[i], callback= self.parse_attr, meta= {'fecha': fecha, 'referer': referer, 'titulo': titulo, 'cantante': cantante, 'album': album})
                        i += 1
                    except:
                        pass
                    print('\n')
        
        #####PASA A LA SIGUIENTE PAGINA#####
        self._num_pagina+=1
        try:
            next_page = response.css('a.blog-pager-older-link ::attr(href)').get()
            #print('PAGINA SIGUIENTE:' + next_page)
            if next_page is not None:
                yield response.follow(next_page, callback= self.parse)
        except:
            print('Hubo un problema al abrir la página siguiente')
            
            
    
    
    def parse_attr(self, response):
        url = str(response.url)
        link_mega = open_adfly(url, 'skip_bu2tton')
        if link_mega is not None:
            link_mega = 'mega' + self.separaLink(link_mega)
        #return link_mega
            infringing = str(unquote(link_mega))
            print('\n*****************DATOS*****************')
            print('infringing: ' + infringing)
            print('fecha: ' + response.meta['fecha'])
            print('referer: ' + response.meta['referer'])
            print('titulo: '+ response.meta['titulo'])
            print('cantante: '+ response.meta['cantante'])
            print('album: '+ response.meta['album'])
            print('***************************************\n')
        
        #####INSERTA EN BD#####
            if veri(infringing) == True:
                if c.existe_inf(infringing, self.id_domin) == False:
                    self.c.inserta_item(response.meta['titulo'], response.meta['cantante'], response.meta['album'],response.meta['referer'], infringing, response.meta['fecha'], self.id_domin)
    
    
    def separaLink(self, link):
        #####SEPARA CANTANTE Y ALBUM#####
        separa = link.split('mega')
        return separa[1]
        
    
    def separa(self, titulo):
        #####SEPARA CANTANTE Y ALBUM#####
        separa = titulo.split('Link')
        s = separa[0].split('-')
        try:
            cantante, album = s[0], s[1]
        except:
            cantante = '-'
            album = '-'
        return cantante, album