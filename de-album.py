# -*- coding: utf-8 -*-
import scrapy
import time
from selenium import webdriver
from datetime import date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from verifica_link import veri, separa_titulo, separa, strip_accents, imprime_datos
from controlador_vista import ModelSQLite, View, Controler

class de_album(scrapy.Spider):
    name = 'de-album'
    _num_pagina = 1
    start_urls = ['https://de-album.blogspot.com/']
    
    id_domin = 11
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
        
        for h3 in response.css('h3.post-title') or response.css('h3.post-title.entry-title'):
            #####RECOLECTA LOS DATOS DE LA PÁGINA#####
            referer = h3.css('a ::attr(href)').get()
            titulo = h3.css('a ::text').get()
            #####SEPARA CANTANTE Y ALBUM#####
            cantante, album = separa_titulo(titulo,'-')
            #####LLAMA AL REFERER#####
            yield scrapy.Request(referer, callback= self.parse_attr, meta= {'referer': referer,'titulo': titulo, 'cantante': cantante,'album': album})
        
        self._num_pagina+=1
        try:
            next_page = response.css('a.blog-pager-older-link.flat-button.ripple ::attr(href)').get()
            if next_page is not None:
                yield response.follow(next_page, callback= self.parse)
        except:
             print('Hubo un problema al abrir la página siguiente')
    
    
    def parse_attr(self, response):
        #####TOMA LA FECHA#####
        fecha = response.css('time.published ::text').get().strip()
        
        #####BÚSCA LA PALABRA DOWNLOAD#####
        link = response.xpath('//*/div[28]/b/span/a/@href').extract_first()
        if link is None:
            link = response.css('div > b > span > a ::attr(href)').get()
        if link is None:
            link = response.xpath('//*/div[2]/div/div[13]/a/@href').extract_first()
                
        prev_inf = link
        #####IMPRIME INFORMACIÓN#####
        imprime_datos(response.meta['titulo'],fecha,response.meta['cantante'],response.meta['album'],response.meta['referer'],prev_inf)
        #####INSERTA EN BD#####
        self.inserta_BD(response, fecha, prev_inf)
        #####LLAMA AL REFERER#####
        infringing = self.Abre_pag(prev_inf)
        imprime_datos(response.meta['titulo'],fecha,response.meta['cantante'],response.meta['album'],response.meta['referer'],infringing)
        #####INSERTA EN BD#####
        self.inserta_BD(response, fecha, infringing)
        
    
    
    def inserta_BD(self, response, fecha, inf):
        if self.c.existe_inf(inf, self.id_domin) == False:
                if veri(inf) == True:
                    self.c.inserta_item(response.meta['titulo'], response.meta['cantante'], response.meta['album'], response.meta['referer'], inf, fecha, self.id_domin)
    
    
    
    def Abre_pag(self, url):
        #####ABRE NAVEGADOR#####
        driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
        driver.get(url)
        time.sleep(1)
        #####HACE CLICK EN EL BOTON#####
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#btn-main"))).click()
        time.sleep(2)
        driver.switch_to.window(window_name=driver.window_handles[1])
        
        #####HACE CLICK EN EL BOTON#####
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button#btn-main"))).click()
        except:
            pass
        
        element = driver.find_element_by_xpath("/html")
        #####ABRE LOS POP UPS#####
        for i in range(10):
            ActionChains(driver).move_to_element(element).click().perform()
            time.sleep(3)
            driver.switch_to.window(window_name=driver.window_handles[1])
        
        #####HACE CLICK EN EL BOTON#####
        driver.switch_to.window(window_name=driver.window_handles[1])
        time.sleep(10)
        element = driver.find_element_by_css_selector("button#btn-main")
        ActionChains(driver).move_to_element(element).click().perform()
        time.sleep(3)
        #####TOMA EL LINK MEGA#####
        url = driver.current_url
        #print('URL1: ' + url)
        driver.quit()
        return url