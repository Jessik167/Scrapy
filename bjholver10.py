# -*- coding: utf-8 -*-
import scrapy
import requests
from datetime import date
from verifica_link import veri, separa_titulo, separa, imprime_datos
from controlador_vista import ModelSQLite, View, Controler

class bjholver10(scrapy.Spider):
    name = 'bjholver10'
    _num_pagina = 1
    start_urls = ['https://bjholver10.blogspot.com/2019/07/descarga-tu-musica-y-regueton-espero.html']
    
    id_domin = 8
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
        titulo = []
        cantante = []
        album = []
        referer = []
        infringing = []
        fecha = date.today().strftime("%B %d, %Y")
        #####COMENTARIOS#####
        print('\n########Pagina ' + str(self._num_pagina) + '########')
        #prueba = response.css("[style = 'text-align: center; outline: rgb(33, 198, 243) none 0px;'] > span").get()
        for span in response.css('div#post-body-5669324029259817671 > div > div'):
            text = span.css('span ::text').get()
            #print(str(text))
            if text is not None:
                if text != 'DESCARGAR' and text[0] != '0':
                    titulo.append(text)
                    can, alb = separa_titulo(titulo[-1], '-')
                    if can == '-':
                        can, alb = separa_titulo(titulo[-1], '–')
                    cantante.append(can)
                    album.append(alb)
                    #print('agrega titulo: ' + titulo[-1])
                    #print('agrega cantante: ' + cantante[-1])
                    #print('agrega album: ' + album[-1])
                text_des = span.css('span > a ::text').get()
                text_des1 = span.css('a ::text').get()
                if text_des == 'DESCARGAR' or text_des1 == 'DESCARGAR':
                    #print(str(span.css('span > a ::attr(href)').get()))
                    if span.css('span > a ::attr(href)').get() is not None:
                        referer.append(str(span.css('span > a ::attr(href)').get()))
                    elif span.css('a ::attr(href)').get() is not None:
                        referer.append(str(span.css('a ::attr(href)').get()))
                    if referer is not None:
                        infringing.append(self.get_inf(referer[-1]))
                    #print('agrega referer: ' + referer[-1])
                    #print('agrega infringing: ' + infringing[-1])
                    
        self.get_datos(titulo, fecha, cantante, album, referer, infringing)
        
        
    def get_datos(self, titulo, fecha, cantante, album, referer, infringing):
        #print('LEN: ' + str(len(titulo)))
        #print('LEN: ' + str(len(infringing)))
        #print('LEN: ' + str(len(referer)))
        #print('LEN: ' + str(len(cantante)))
        #print('LEN: ' + str(len(album)))
        #print('titulo: ' + titulo[-1])
        for i in range(len(infringing)):
            print('\n*****************DATOS*****************')
            print('infringing: ' + infringing[i])
            print('referer: ' + referer[i])
            print('titulo: ' + titulo[i])
            print('fecha: ' + fecha)
            print('cantante: ' + cantante[i])
            print('album: ' + album[i])
            print('***************************************\n')
            #####INSERTA EN BD#####
            if veri(infringing[i]) == True:
                if self.c.existe_inf(infringing[i], self.id_domin) == False:
                    self.c.inserta_item(titulo[i], cantante[i], album[i], referer[i], infringing[i], fecha, self.id_domin)
            
    
    def get_inf(self, url):
        response = requests.get(url)
        return str(response.request.url)