import mvc_exceptions as mvc_exc 

items = list()


def crea_items(app_items):
    global items
    items = app_items
    
    
def crea_item(id, titulo, referer, infringe):
    global items
    resultados = list(filter(lambda x:x['id'] == id, items))
    if resultados:
        raise mvc_exc.ItemExistente('{} ya existe en la BD!'.format(id))
    else:
        items.append({'id': id, 'titulo': titulo,'referer': referer,'infringe': infringe})


def lee_item(id):
    global items
    mis_items = list(filter(lambda x:x['id'] == id, items))
    if mis_items:
        return mis_items[0]
    else:
        raise mvc_exc.ItemNoGuardado('No se puede leer {} porque no existe en la BD!'.format(id))

def lee_items():
    global items
    return [item for item in items]


def update_item(id,titulo,referer,infringe):
    global items
    id_items = list(filter(lambda i_x: i_x[1]['id'] == id, enumerate(items)))
    if id_items:
        i, items_a_update = id_items[0][0], id_items[0][1]
        items[i] = {'id': id,'titulo': titulo,'referer': referer,'infringe': infringe}
    else:
        raise mvc_exc.ItemNoGuardado('No se puede leer {} porque no existe en la BD!'.format(id))
    
def elimina_item(id):
    global items
    id_items = list(filter(lambda i_x: i_x[1]['id'] == id, enumerate(items)))
    if id_items:
        i, items_a_update = id_items[0][0], id_items[0][1]
        del items[i]
    else:
        raise mvc_exc.ItemNoGuardado('No se puede leer {} porque no existe en la BD!'.format(id))
    
'''my_items = [
    {'id': 2747, 'titulo': 'DESCARGAR CD COMPLETO PARA QUE LE HAGO DAnO',
    'referer': 'https://musicapalabanda.org/descargar-cd-completo-para-que-le-hago-dano/',
    'infringe': 'http://adf.ly/7342230/valedoresparaquelehagodao'},
          
    {'id': 2748, 'titulo': 'DESCARGAR CD COMPLETO ?LOS VALEDORES DE LA SIERRA?',
    'referer': 'https://musicapalabanda.org/descargar-cd-completo-los-valedores-de-la-sierra/',
    'infringe': 'http://adf.ly/7342230/valedoresenascenso'}
    ]
     
# CREATE
crea_items(my_items)
crea_item(2749,titulo='DESCARGAR CD COMPLETO GRUPO BRYNDIS',
        referer='https://musicapalabanda.org/descargar-cd-completo-grupo-bryndis/',
        infringe='http://adf.ly/7342230/bryndisadicto2014')
    
# READ
print('LEE items')
print(lee_items())
print('LEE 2749')
print(lee_item(2749))

# DELETE
print('DELETE 2747')
elimina_item(2747)

# READ
print('LEE items')
print(lee_items())'''