"""
ETL:
Extraccion de informacion de celulares de la pagina web de mercadolibre en Colombia
Autor: OSCAR AYALA
Version 23-MAY-2021
"""

from scrapy.item import Field
from scrapy.item import Item
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup

class Articulo(Item):
    titulo = Field()
    precio = Field()
    marca = Field()
    linea = Field()
    modelo = Field()
    volumen = Field()
    calif = Field()
    opiniones = Field()
    memoriaInt = Field()
    tit_opinion = Field()
    ubicacion = Field()


class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadoLibre'

    custom_settings = {
      'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36',
      'CLOSESPIDER_PAGECOUNT': 10 # Numero maximo de paginas
    }

    # Dominios permitidos para hacer la extraccion.
    allowed_domains = ['mercadolibre.com.co', 'listado.mercadolibre.com.co', 'celulares.mercadolibre.com.co/']

    start_urls = ['https://celulares.mercadolibre.com.co']

    download_delay = 1

    # Tupla de reglas
    rules = (
        Rule(  # REGLA #1 => HORIZONTALIDAD POR PAGINACION
            LinkExtractor(
                allow=r'/_Desde_\d+'
                # Patron en donde se utiliza "\d+", expresion que puede tomar el valor de cualquier combinacion de numeros
            ), follow=True),
        Rule(  # REGLA #2 => VERTICALIDAD AL DETALLE DE LOS PRODUCTOS
            LinkExtractor(
                allow=['category:MCO1055', '/MCO']

            ), follow=True, callback='parse_items'),
        # Al entrar al detalle de los productos, se llama al callback con la respuesta al requerimiento
    )

    def parse_items(self, response):

        item = ItemLoader(Articulo(), response)
        
        # Utilizo Map Compose
        item.add_xpath('titulo', '//h1/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        #item.add_xpath('descripcion', '//div[@class="item-description__text"]/p/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))

        item.add_xpath('marca', '// *[ @ id = "highlighted-specs"] / div[4] / div / div / div / div[1] / div[1] / table / tbody / tr[1] / td / span/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('linea', '//*[@id="highlighted-specs"]/div[4]/div/div/div/div[1]/div[1]/table/tbody/tr[2]/td/span/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('modelo', '//*[@id="highlighted-specs"]/div[4]/div/div/div/div[1]/div[1]/table/tbody/tr[3]/td/span/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))
        item.add_xpath('memoriaInt', '// *[ @ id = "highlighted-specs"] / div[4] / div / div / div / div[2] / div[2] / table / tbody / tr[1] / td / span/text()', MapCompose(lambda i: i.replace('\n', ' ').replace('\r', ' ').strip()))



        soup = BeautifulSoup(response.body)
        precio = soup.find(class_="price-tag-fraction")
        precio_completo = precio.text.replace('\n', ' ').replace('\r', ' ').replace(' ', '')
        item.add_value('precio', precio_completo)

        volumen = soup.find(class_="ui-pdp-subtitle")
        volumen_completo = volumen.text.replace('\n', ' ').replace('\r', ' ').replace(' ', '').replace('vendidos', '')
        item.add_value('volumen', volumen_completo)

        opiniones = soup.find(class_="ui-pdp-review__amount")
        opiniones_completo = opiniones.text.replace('\n', ' ').replace('\r', ' ').replace(' ', '').replace('opiniones', '')
        item.add_value('opiniones', opiniones_completo)

        calif = soup.find(class_="ui-pdp-reviews__rating__summary__average")
        calif_completo = calif.text.replace('\n', ' ').replace('\r', ' ').replace(' ', '')
        item.add_value('calif', calif_completo)

        tit_opinion = soup.find(class_="ui-pdp-reviews__comments__review-comment__title")
        tit_opinion_completo = tit_opinion.text.replace('\n', ' ').replace('\r', ' ').replace(' ', '')
        item.add_value('tit_opinion', tit_opinion_completo)

        ubicacion = soup.find(class_="ui-seller-info__status-info__subtitle")
        ubicacion_completo = ubicacion.text.replace('\n', ' ').replace('\r', ' ').replace(' ', '')
        item.add_value('ubicacion', ubicacion_completo)


        yield item.load_item()

# EJECUCION en el CMD del prompt
# scrapy runspider 2_mercadolibre.py -o mercadolibre.csv -t csv