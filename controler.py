import backend
import mvc_exceptions as mvc_exc

class ModelBasic(object):
    
    def __init__(self, application_items):
        self._item_type = 'producto'
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