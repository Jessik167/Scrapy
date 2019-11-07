# -*- coding: utf-8 -*-
import time
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from verifica_link import veri, separa_titulo, separa, strip_spaces, imprime_datos
from controlador_vista import ModelSQLite, View, Controler

name = 'softarchive'
_num_pagina = 1
start_urls = ['https://softarchive.unblocked.ltda/music/']

id_domin = 13
nombre_trelacion = 'dominios'
#####CREA OBJETO#####
c = Controler(ModelSQLite(), View())

#####CREA TABLA#####
c.crea_tabla(nombre_trelacion)
if c.existe_id(id_domin, nombre_trelacion) == False:
#####TOMA LA FECHA ACTUAL#####
    hoy = date.today().strftime("%d %B, %Y")
#####INSERTA EN LA TABLA RELACIONAL#####
    c.inserta_item_relacional(id_domin, start_urls[0], hoy, nombre_trelacion)

#####COMENTARIOS#####
print('\n########Pagina ' + str(_num_pagina) + '########')
#####ABRE NAVEGADOR SELENIUM#####
driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
driver.get(start_urls[0])
#####ESPERA A QUE CARGUE LA PÁGINA#####
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "h2 > a")))
#####GUARDA LA PÁGINA PRINCIPAL#####
main_window = driver.current_window_handle
#####TOMA EL HREF DE LA PÁGINA SIGUIENTE#####
next_page = driver.find_element_by_css_selector('a.sa.sa-nextpage.tip').get_attribute('href')
#####RECORRE TODAS LAS PÁGINAS#####
while next_page is not None: 
    #####TOMA LOS DATOS#####
    for a in driver.find_elements_by_css_selector("h2 > a"):
        referer = a.get_attribute('href')
        titulo = a.find_element_by_css_selector('span').text
        cantante, album = separa_titulo(titulo, '-')
        fecha = date.today().strftime("%B %d, %Y")
        #####ABRE UNA NUEVA PESTAÑA#####
        driver.execute_script("window.open(arguments[0]);", referer)
        driver.switch_to.window(driver.window_handles[1])
        infringing = driver.find_element_by_xpath('//*[@id="shell"]/section/div[1]/div[2]/article/section/center/a').get_attribute('href')
        imprime_datos(titulo, fecha, cantante, album, referer, infringing)
        if c.existe_inf(infringing, id_domin) == False:
                if veri(infringing) == True:
                    c.inserta_item(titulo, cantante, album, referer, infringing, fecha, id_domin)
        #####CIERRA LA PESTAÑA#####
        driver.close()
        #####CAMBIA A LA PÁGINA PRINCIPAL#####
        driver.switch_to.window(main_window)
    #####ABRE LA SIGUIENTE PÁGINA#####
    driver.get(next_page)
    #####TOMA EL HREF DE LA PÁGINA SIGUIENTE#####
    next_page = driver.find_element_by_css_selector('a.sa.sa-nextpage.tip').get_attribute('href')
driver.quit()