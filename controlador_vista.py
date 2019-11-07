# -*- coding: utf-8 -*-
import mysql_backend
import mvc_exceptions as mvc_exc

class ModelSQLite(object):
    
    def __init__(self):#, items_aplicacion):
        self._tipo_item = 'prueba'
        self._conexion = mysql_backend.conecta_BD(bd=mysql_backend.BD_nombre)
        #self.crea_items(items_aplicacion)
        
    @property
    def conexion(self):
        return self._conexion
    
    @property
    def tipo_item(self):
        return self._tipo_item
    
    @tipo_item.setter
    def tipo_item(self, nuevo_tipo_item):
        self._tipo_item = nuevo_tipo_item
    
    def existe(self, id, nombre_tabla):
        return mysql_backend.existe(self.conexion, id, nombre_tabla)
    
    def existe_inf(self, inf, id_dominio):
        return mysql_backend.existe_inf(self.conexion, inf, self._tipo_item, id_dominio)
    
    def ultimo_id(self, nombre_tabla):
        mysql_backend.ultimo_id(self.conexion, nombre_tabla)
    
    def crea_tabla(self, nombre_tabla, nombre_trelacion):
        mysql_backend.crea_tabla(self.conexion, nombre_tabla, nombre_trelacion)
        
    def crea_tabla_relacion(self, nombre_trelacion):
        mysql_backend.crea_tabla_relacion(self.conexion, nombre_trelacion)
    
    def crea_item(self, titulo, cantante, album, referer, infringe, fecha, id_domin):
        mysql_backend.inserta_uno(self.conexion, titulo, cantante, album, referer, infringe, fecha, id_domin, nombre_tabla= self._tipo_item)
        
    def crea_item_relacional(self, id, dominio, fecha, nombre_tabla):
        mysql_backend.inserta_uno_relacional(self.conexion, id, dominio, fecha, nombre_tabla= nombre_tabla)
    
    def crea_items(self, items):
        mysql_backend.insertar_varios(self.conexion, items, nombre_tabla= self._tipo_item)
        
    def lee_item(self, id):
        return mysql_backend.selecciona_uno(self.conexion, id, nombre_tabla= self._tipo_item)
    
    def lee_items(self):
        return mysql_backend.selecciona_todos(self.conexion, self._tipo_item)
    
    def actualiza_item(self, id, titulo, referer, infringe, fecha):
        mysql_backend.Actualiza_uno(self.conexion, id, titulo, referer, infringe, fecha, nombre_tabla= self._tipo_item)
        
    def elimina_item(self, id):
        mysql_backend.elimina_uno(self.conexion,id, nombre_tabla=self._tipo_item)
        
    def cierra_bd(self, id):
        mysql_backend.desconecta_BD(mysql_backend.BD_nombre,self._conexion)
        
        
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
    def muestra_item_guardado(item_type):
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('{} ha sido agregado a la lista!'.format(item_type))
        print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        
    @staticmethod
    def muestra_item_cambio(nuevo, viejo):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        print('cambio el tipo de "{}" a "{}"'.format(viejo, nuevo))
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        
    @staticmethod
    def muestra_item_updated(item, v_titulo, v_referer, v_infringe, v_fecha, n_titulo, n_referer, n_infringe, n_fecha):
        print('---   ---   ---   ---   ---   ---   ---   ---   ---   ---   --')
        print('cambio {} titulo: {} --> {}'
              .format(item, v_titulo, n_titulo))
        print('cambio {} referer: {} --> {}'
              .format(item, v_referer, n_referer))
        print('cambio {} infringe: {} --> {}'
              .format(item, v_infringe, n_infringe))
        print('cambio {} fecha: {} --> {}'
              .format(item, v_fecha, n_fecha))
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
        
    def existe_id(self, id, nombre_tabla):
        return self.model.existe(id, nombre_tabla)
    
    def existe_inf(self, inf, id_dominio):
        return self.model.existe_inf(inf, id_dominio)
    
    def ultimo_id(self, nombre_tabla):
        self.model.ultimo_id(nombre_tabla)
        
    def crea_tabla(self, nombre_trelacion):
        item_tipo = self.model._tipo_item
        self.model.crea_tabla(item_tipo, nombre_trelacion)
        
    def crea_tabla_relacion(self, nombre_trelacion):
        #item_tipo = self.model._tipo_item
        self.model.crea_tabla_relacion(nombre_trelacion)
            
    def muestra_items(self, bullet_points = False):
        items = self.model.lee_items()
        item_tipo = self.model._tipo_item
        if bullet_points:
            self.view.muestra_bullet_lista(item_tipo,items)
        else:
            self.view.muestra_numeros_lista(item_tipo,items)
            
    def muestra_item(self, id_item):
        try:
            item = self.model.lee_item(id_item)
            tipo_item = self.model._tipo_item
            self.view.muestra_item(tipo_item, item)
        except mvc_exc.ItemNoGuardado as e:
            self.view.error_falta_item(id_item, e)
            
    def inserta_item(self, titulo, cantante, album, referer, infringe, fecha, id_domin):
        #print('titulo:' + titulo + ' referer:' + referer + ' infringe:' + infringe + ' fecha:' + fecha)
        #assert id > 0, 'El id debe ser mayor que cero'
        item_tipo = self.model._tipo_item
        try:
            self.model.crea_item(titulo, cantante, album, referer, infringe, fecha, id_domin)
            self.view.muestra_item_guardado(item_tipo)
        except mvc_exc.ItemExistente as e:
            self.view.error_existe_item(item_tipo,e)
            
    def inserta_item_relacional(self, id, dominio, fecha, nombre_tabla):
        print('dominio: ' + dominio + 'fecha: ' + fecha)
        item_tipo = self.model._tipo_item
        try:
            self.model.crea_item_relacional(id, dominio, fecha, nombre_tabla)
            self.view.muestra_item_guardado(item_tipo)
        except mvc_exc.ItemExistente as e:
            self.view.error_existe_item(item_tipo,e)
           
            
    def update_item(self, id, titulo, referer, infringe):
        assert id > 0, 'El id debe ser mayor que cero'
        item_tipo = self.model._tipo_item
        try:
            viejo = self.model.lee_item(id)
            self.model.actualiza_item(id, titulo, referer, infringe, fecha)
            self.view.muestra_item_updated(id, viejo['titulo'], viejo['referer'], viejo['infringe'], viejo['fecha'],
                                            titulo, referer, infringe, fecha)
        except mvc_exc.ItemNoGuardado as e:
            self.view.error_no_guardado(id,e)
            # si el item no es guardado aun y realizamos una actualizacion(update),
            # tenemos dos opciones: hacer nada o llamar a insertar_item y agregarlo.
            # self.inserta_item(id, titulo, referer, infringe
            
    def update_tipo_item(self, nuevo_tipo_item):
        tipo_viejo = self.model._tipo_item
        self.model._tipo_item = nuevo_tipo_item
        self.view.muestra_item_cambio(tipo_viejo, nuevo_tipo_item)
        
    def elimina_item(self,id):
        tipo_item = self.model._tipo_item
        try:
            self.model.elimina_item(id)
            self.view.muestra_item_eliminado(id)
        except mvc_exc.ItemNoGuardado as e:
            self.view.error_no_guardado(id, e)