# -*- coding: utf-8 -*-
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from importlib.resources import contents
from selenium.webdriver.support.ui import WebDriverWait

def proxy_request():
    try:
        r = requests.get('http://gimmeproxy.com/api/getProxy?country=US')
        
        contents = str(r.content)
        contents = contents.split(',')
        IP = contents[2]
        PORT = contents[3]
        
        IP = IP.replace(':','')
        IP = IP.replace('"','')
        IP = IP.replace(' ','')
        IP = IP.replace('\n','')
        IP = IP.replace('ip','')
        
        PORT = PORT.replace(':','')
        PORT = PORT.replace('"','')
        PORT = PORT.replace(' ','')
        PORT = PORT.replace('\n','')
        PORT = PORT.replace('port','')
        string_proxy = IP + ':' + PORT
        #print('PROXY: ' + string_proxy)
        
        f = open('proxy_file.txt','w')
        f.write(string_proxy)
        f.close()
    except:
        print('----------------------Error al recibir el proxy----------------------')
        f = open('proxy_file.txt','w')
        f.write('0')
        f.close()

def abre_navegador():
    try:
        proxy_request()
        f = open('proxy_file.txt','r')
        proxy_ip = f.read()
        f.close()
        if len(proxy_ip) <=1:
            print('----------------------No se usará ningún proxy----------------------')
            #driver = webdriver.PhantomJS()
            driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
        else:
            #print('----------------------Usando proxy: ' + proxy_ip + '----------------------')
            PROXY = proxy_ip
            #service_arg = ['--proxy=' + proxy_ip + ':9999', '--proxy-type=socks5']
            #driver = webdriver.PhantomJS(service_args=service_arg)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--proxy-server={}'.format(PROXY))
            driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe', options= chrome_options)
    except:
        print('----------------------Ningún proxy será usado----------------------')
        #driver = webdriver.PhantomJS()
        driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
    driver.implicitly_wait(300)
    driver.set_page_load_timeout(300)
    return driver


def open_adfly(url, n_comp):
    driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')  # Optional argument, if not specified will search path.
    driver.get(url)
    current_window = driver.current_window_handle
    #time.sleep(6) # Let the user actually see something!
    #driver.find_element_by_id(n_comp).get_attribute('href').click()
    try:
        driver.find_element_by_css_selector('body.skip-add').click()
        time.sleep(2)
        driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'W')
        driver.switch_to.window(current_window)
        WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.CSS_SELECTOR, n_comp))).click()
        #element = driver.find_element_by_css(n_comp)
        #driver.execute_script("arguments[0].click();", element)
        #driver.find_element_by_xpath(n_comp).click()
        #search_box.send_keys('ChromeDriver')
        #search_box.submit()
        #time.sleep(5) # Let the user actually see something!
        time.sleep(3)
        url = driver.current_url
        driver.quit()
        return str(url)
    except:
        pass


def open_notRobot(url):
    driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')  # Optional argument, if not specified will search path.
    driver.get(url);
    time.sleep(3) # Let the user actually see something!
    search_box = driver.find_elements_by_xpath('//*[@id="recaptcha-anchor"]/div[1]')
    search_box.click()
    #search_box.send_keys('ChromeDriver')
    #search_box.submit()
    #time.sleep(5) # Let the user actually see something!
    driver.quit()
    return str(search_box)
   
#print(open_adfly('http://www.google.com', 'link'))
#open_notRobot('https://ouo.io/DpLre4')
#scroll('http://gimmeproxy.com/api/getProxy?country=US')