import backend
import mvc_exceptions as mvc_exc

class ModelBasic(object):
    
    def __init__(self, application_items):
        self._item_type = 'cancion'
        self.crea_items(application_items)
        
    @property
    def item_type(self):
        return self._item_type
    
    @item_type.setter
    def item_type(self, nuevo_item_type):
        self._item_type = nuevo_item_type
        
    
    def crea_item(self,id,titulo,referer,infringe):
        backend.crea_item(id,titulo,referer,infringe)
        
    def crea_items(self,items):
        backend.crea_items(items)
    
    def lee_item(self, id):
        return backend.lee_item(id)
    
    def lee_items(self):
        return backend.lee_items()
    
    def update_item(self, id, titulo, referer, infringe):
        backend.update_item(id,titulo,referer,infringe)
        
    def elimina_item(self, id):
        backend.elimina_item(id)



class View(object):
    
    @staticmethod
    def muestra_bullet_lista(item_type,items):
        print('--- {} LISTA ---'.format(item_type))
        for item in items:
            print('* {}'.format(item))
            
    @staticmethod
    def  muestra_numeros_lista(item_type,items):
        print('--- {} LISTA ---'.format(item_type))
        for i, item in enumerate(items):
            print('{} {}'.format(i+1, item))
            
    @staticmethod
    def muestra_item(item_type, item_info):
        print('/////////////////////////////////////////////////////////')
        print('{} INFO: {}'.format(item_type,item_info))
        print('/////////////////////////////////////////////////////////')
        
    @staticmethod
    def error_falta_item(item, err):
        print('**************************************************************')
        print('el id {} no existe!'.format(item))
        print('{}'.format(err.args[0]))
        print('**************************************************************')
        
    @staticmethod
    def error_existe_item(item, err):
        print('**************************************************************')
        print('el id {} ya existe en la lista!'.format(item))
        print('{}'.format(err.args[0]))
        print('**************************************************************')
        
    @staticmethod
    def error_no_guardado(item, err):
        print('**************************************************************')
        print('el id {} no existe en la lista, primero inserte!'.format(item))
        print('{}'.format(err.args[0]))
        print('**************************************************************')
        
    @staticmethod
    def muestra_item_guardado(item, item_type):
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('{} ha sido agregado a la lista!'.format(item))
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
    @staticmethod
    def muestra_item_cambio(nuevo, viejo):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        print('cambio el tipo de "{}" a "{}"'.format(viejo, nuevo))
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        
    @staticmethod
    def muestra_item_updated(item, v_titulo, v_referer, v_infringe, n_titulo, n_referer, n_infringe):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        print('cambio {} titulo: {} --> {}'
              .format(item, v_titulo, n_titulo))
        print('cambio {} referer: {} --> {}'
              .format(item, v_referer, n_referer))
        print('cambio {} infringe: {} --> {}'
              .format(item, v_infringe, n_infringe))
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        
    @staticmethod
    def muestra_item_eliminado(id):
        print('--------------------------------------------------------------')
        print('{} ha sido removido de la lista'.format(id))
        print('--------------------------------------------------------------')



class Controler(object):
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
    def muestra_items(self, bullet_points = False):
        items = self.model.lee_items()
        item_tipo = self.model.item_type
        if bullet_points:
            self.view.muestra_bullet_lista(item_tipo,items)
        else:
            self.view.muestra_numeros_lista(item_tipo,items)
            
    def muestra_item(self, id_item):
        try:
            item = self.model.lee_item(id_item)
            tipo_item = self.model.item_type
            self.view.muestra_item(tipo_item, item)
        except mvc_exc.ItemNoGuardado as e:
            self.view.error_falta_item(id_item, e)
            
    def inserta_item(self, id, titulo, referer, infringe):
        assert id > 0, 'El id debe ser mayor que cero'
        item_tipo = self.model.item_type
        try:
            self.model.crea_item(id, titulo, referer, infringe)
            self.view.muestra_item_guardado(id, item_tipo)
        except mvc_exc.ItemExistente as e:
            self.view.error_existe_item(id, item_tipo,e)
            
    def update_item(self, id, titulo, referer, infringe):
        assert id > 0, 'El id debe ser mayor que cero'
        item_tipo = self.model.item_type
        try:
            viejo = self.model.lee_item(id)
            self.model.update_item(id, titulo, referer, infringe)
            self.view.muestra_item_updated(id, viejo['titulo'], viejo['referer'], viejo['infringe'],
                                            titulo, referer, infringe)
        except mvc_exc.ItemNoGuardado as e:
            self.view.error_no_guardado(id,e)
            # si el item no es guardado aun y realizamos una actualizacion(update),
            # tenemos dos opciones: hacer nada o llamar a insertar_item y agregarlo.
            # self.inserta_item(id, titulo, referer, infringe
            
    def update_tipo_item(self, nuevo_tipo_item):
        tipo_viejo = self.model.item_type
        self.model.item_type = nuevo_tipo_item
        self.view.muestra_item_cambio(tipo_viejo, nuevo_tipo_item)
        
    def elimina_item(self,id):
        tipo_item = self.model.item_type
        try:
            self.model.elimina_item(id)
            self.view.muestra_item_eliminado(id)
        except mvc_exc.ItemNoGuardado as e:
            self.view.error_no_guardado(id, e)


my_items = [
    {'id': 2747, 'titulo': 'DESCARGAR CD COMPLETO PARA QUE LE HAGO DAnO',
    'referer': 'https://musicapalabanda.org/descargar-cd-completo-para-que-le-hago-dano/',
    'infringe': 'http://adf.ly/7342230/valedoresparaquelehagodao'},
          
    {'id': 2748, 'titulo': 'DESCARGAR CD COMPLETO ?LOS VALEDORES DE LA SIERRA?',
    'referer': 'https://musicapalabanda.org/descargar-cd-completo-los-valedores-de-la-sierra/',
    'infringe': 'http://adf.ly/7342230/valedoresenascenso'}
    ]

c = Controler(ModelBasic(my_items), View())
c.muestra_items()
c.muestra_items(bullet_points=True)
c.muestra_item(1)
c.muestra_item(2748)
c.inserta_item(1, 'Los Herederos de Nuevo Leon', 'https://musicapalabanda.org/los-herederos-de-nuevo', 'https://ouo.io/SFzEtC')
c.update_item(1, 'Los Herederos de Nuevo Leon | El Legado', 'https://musicapalabanda.org/los-herederos-de-nuevo', 'https://ouo.io/SFzEtC')
c.update_item(2,'Leandro Rios ? Sigo de Frente 2018 (Album)','https://musicapalabanda.org/los-herederos-de-nuevo','https://ouo.io/SFzEtC')
c.elimina_item(2)
c.elimina_item(1)