import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        for title in response.css('.post-header>h2'):
            yield {'title': title.css('a ::text').get()}

        for next_page in response.css('a.next-posts-link'):
            yield response.follow(next_page, self.parse)
            
            '''def __init__(self, name=None, **kwargs):
        #####CREA OBJETO#####
        c = Controler(ModelSQLite(), View())
        #####CREA TABLA#####
        c.crea_tabla(self.sql_tabla, self.nombre_trelacion)
        #####TOMA LA FECHA ACTUAL#####
        hoy = date.today().strftime("%d %B, %Y")
        #####INSERTA EN LA TABLA RELACIONAL#####
        c.inserta_item_relacional(self.start_urls[0], hoy, self.nombre_trelacion)
        scrapy.Spider.__init__(self, name=name, **kwargs)
    '''  
            
            
            '''
    def parse_attr(self, response):
        #####VARIABLE#####
        found = 0
        item = response.meta['item']
        post_id = response.meta['id_post']
        item['fecha'] = response.meta['fecha']
        c = response.meta['controler']
        
        #####RECOLECTA LOS DATOS DE LA PÁGINA#####
        item['titulo'] = response.xpath('//*[@id="' + post_id + '"]/div/header/h1/text()').extract()[0]
        item['href'] = response.url
        
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
        c.inserta_item(str(item['titulo']), cantante, album, str(item['href']), str(item['infringing']), str(item['fecha']), self.id_domin)
        return item
        '''