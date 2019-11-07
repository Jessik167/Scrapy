# -*- coding: utf-8 -*-
import mysql.connector
from mysql.connector import ProgrammingError, OperationalError, IntegrityError
from bdb import Bdb
import mvc_exceptions as mvc_exc
from cmath import inf

BD_nombre = 'apdif'
#servidor = '192.168.100.9'
servidor = '3.231.20.132'
usuario = 'apdif'
passw = 'K3XyRwLjPtkui6qJ'
#passw = 'TZaJsYQqMjY1lHOK'    
    
'''Conecta a la BD sql. Crea la base de datos si aun no hay una.
       Abre conexion a la BD(puede ser un archivo BD o una en memoria).
       Cuando la base de datos es accesada por multiple conexiones, y uno
       de los procesos modifica la BD, la BD sql se bloquea hasta que la
       transaccion es completada.
       
       
       Parametros
       ----------
       bd: str
           nombre de la BD (sin extencion .db). si no hay una, la crea en memoria.
           
       
       Retorna
       -------
       conexion: sql.connector
                 objeto de conexion
    '''
def conecta_BD(bd=None):
    if bd is None:
        mybd = ':memory:'
        print('Nueva conexion en BD en memoria...')
    else:
        mybd = '{}.db'.format(bd)
        print('Nueva conexion a BD SQL...')
    
    conexion = mysql.connector.connect(host=servidor,
                            database=bd,
                            user=usuario,
                            password=passw)
    #conexion = mydb.cursor()
    #conexion = sqlite3.connect(mybd)
    return conexion

def conecta(func):
    '''Decorador para (re)abrir la conexion de la bd SQL cuando sea necesario.
    
       Una conexion a la BD debe ser abierta cuando queremos realizar una consulta a la Bd
       pero estamos en una de las siguientes situaciones:
       1) no hay una conexion
       2) la conexion esta cerrada
       
       Parametros
       ----------
       func: funcion
          funcion que realiza la consulta de la Bdb
          
       Retorna
       -------
       funcion interna: funcion
       '''
    def funcion_interna(cone, *args, **kwargs):
        try:
            curs = cone.cursor()
            curs.execute("USE {}".format(BD_nombre))
        except (AttributeError, ProgrammingError):
            curs = conecta_BD(BD_nombre)
        return func(cone,*args, **kwargs)
    return funcion_interna

def desconecta_BD(db=None, cone = None):
    if db is not BD_nombre:
        print('UPS! es una BD diferente!')
    if cone is not None:
        cone.close()
        
@conecta
def crea_tabla(cone, nombre_tabla, nombre_trelacion):
    sql = "CREATE TABLE IF NOT EXISTS {} (id INT NOT NULL AUTO_INCREMENT," \
          "PRIMARY KEY (id), titulo VARCHAR(100), cantante VARCHAR(100), album VARCHAR(100)," \
          "referer VARCHAR(255), infringe VARCHAR(255), fecha VARCHAR(100), dominio_id INT," \
          "FOREIGN KEY (dominio_id) REFERENCES {}(dominio_id) ON UPDATE CASCADE ON DELETE CASCADE);".format(nombre_tabla, nombre_trelacion)
    #sql = "CREATE TABLE IF NOT EXISTS {} (id INT NOT NULL AUTO_INCREMENT," \
    #      "PRIMARY KEY (id), titulo VARCHAR(100), cantante VARCHAR(100), album VARCHAR(100), referer VARCHAR(255), infringe VARCHAR(255), fecha VARCHAR(100));".format(nombre_tabla)
    #sql = 'CREATE TABLE {} ' \
    #      '(id INT(11) NOT NULL, titulo VARCHAR(100), referer VARCHAR(255), infringe VARCHAR(255), PRIMARY KEY (id));'.format(nombre_tabla)
    try:
        curs = cone.cursor()
        curs.execute(sql)
    except OperationalError as e:
        print(e)
        
@conecta
def crea_tabla_relacion(cone, nombre_trelacion):
    sql = "CREATE TABLE IF NOT EXISTS {} (dominio_id INT NOT NULL," \
          "PRIMARY KEY (id), dominio VARCHAR(100), fecha VARCHAR(100));".format(nombre_trelacion)
    try:
        curs = cone.cursor()
        curs.execute(sql)
    except OperationalError as e:
        print(e)

@conecta
def elimina_tabla(cone, nombre_tabla):
    sql = 'DROP TABLE {};'.format(nombre_tabla)
    try:
        curs = cone.cursor()
        curs.execute(sql)
    except OperationalError as e:
        print(e)
        
@conecta
def existe(cone, id, nombre_tabla):
    #scrub(id)
    sql = 'SELECT dominio_id FROM {} WHERE dominio_id = {};'.format(nombre_tabla, id)
    try:
        curs = cone.cursor()
        curs.execute(sql)
        resultado = curs.fetchone()
        if resultado is not None:
            return True
        else:
            return False
    except OperationalError as e:
        print(e)
        
@conecta
def existe_inf(cone, inf, nombre_tabla, id_dominio):
    scrub(nombre_tabla)
    sql = 'SELECT infringe FROM {} WHERE dominio_id = {};'.format(nombre_tabla, id_dominio)
    try:
        curs = cone.cursor()
        curs.execute(sql)
        resultado = curs.fetchall()
        for res in resultado:
            if res[0] == inf:
                return True
        return False
    except OperationalError as e:
        print(e)
       
       
@conecta
def ultimo_id(cone, nombre_tabla):
    scrub(nombre_tabla)
    sql = 'SELECT max(id) FROM {};'.format(nombre_tabla)
    try:
        curs = cone.cursor()
        curs.execute(sql)
        resultado = curs.fetchone()
        print(resultado)
        if resultado is not None:
            return resultado
    except OperationalError as e:
        print(e)
        
         
def scrub(cadena_entrada):
    '''Limpia la cadena de entrada (para prevenir SQL injection).
    
       Parametros
       ----------
       cadena_entrada: str
       
       Retorna
       -------
       str
    '''
    return ''.join(k for k in cadena_entrada if k.isalnum())

@conecta
def inserta_uno(cone, titulo, cantante, album, referer, infringe, fecha, id_domin, nombre_tabla):
    nombre_tabla = scrub(nombre_tabla)
    sql = "INSERT INTO {} (titulo, cantante, album, referer, infringe, fecha, dominio_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"\
        .format(nombre_tabla)
    try:
        curs = cone.cursor()
        curs.execute(sql, (titulo,cantante, album, referer,infringe, fecha, id_domin))
        cone.commit()
    except IntegrityError as e:
        raise mvc_exc.ItemExistente('{}: "{}" ya existe en la tabla "{}"'.format(e, name, nombre_tabla))
    print('El dato ha sido insertado en la BD...')
    
@conecta
def inserta_uno_relacional(cone, id, dominio, fecha , nombre_tabla):
    nombre_tabla = scrub(nombre_tabla)
    sql = "INSERT INTO {} (dominio_id, dominio, fecha) VALUES (%s, %s, %s)"\
        .format(nombre_tabla)
    try:
        curs = cone.cursor()
        curs.execute(sql, (id, dominio, fecha))
        cone.commit()
    except IntegrityError as e:
        raise mvc_exc.ItemExistente('{}: "{}" ya existe en la tabla "{}"'.format(e, name, nombre_tabla))
    print('El dato ha sido insertado en la BD...')

@conecta
def insertar_varios(cone, items, nombre_tabla):
    nombre_tabla = scrub(nombre_tabla)
    sql = "INSERT INTO {} (titulo, referer, infringe, fecha) VALUES (%s, %s, %s, %s)"\
        .format(nombre_tabla)
    entradas = list()
    for x in items:
        entradas.append((x['titulo'],x['referer'],x['infringe'], x['fecha']))
    try:
        curs = cone.cursor()
        curs.executemany(sql, entradas)
        cone.commit()
    except IntegrityError as e:
        print('{}: almenos uno en {} ya fue insertado en la tabla "{}"'
              .format(e, [x['titulo'] for x in items], nombre_tabla))
    print('Los datos han sido insertados en la BD...')
        
def tupla_a_dic(mitupla):
    midic = dict()
    midic['id'] = mitupla[0]
    midic['titulo'] = mitupla[1]
    midic['cantante'] = mitupla[2]
    midic['album'] = mitupla[3]
    midic['referer'] = mitupla[4]
    midic['infringe'] = mitupla[5]
    midic['fecha'] = mitupla[6]
    return midic

@conecta
def selecciona_uno(cone, id_item, nombre_tabla):
    nombre_tabla = scrub(nombre_tabla)
    #id_item = scrub(id_item)
    sql = 'SELECT * FROM {} WHERE id = {}'.format(nombre_tabla,id_item)
    curs = cone.cursor()
    curs.execute(sql)
    resultado = curs.fetchone()
    if resultado is not None:
        return tupla_a_dic(resultado)
    else:
        raise mvc_exc.ItemNoGuardado('No puede leer "{}" porque no existe en la tabla "{}"'
            .format(id_item, nombre_tabla))
        
@conecta
def selecciona_todos(cone, nombre_tabla):
    nombre_tabla = scrub(nombre_tabla)
    sql = 'SELECT * FROM {}'.format(nombre_tabla)
    curs = cone.cursor()
    curs.execute(sql)
    resultados = curs.fetchall()
    return list(map(lambda x: tupla_a_dic(x),resultados))        

@conecta
def Actualiza_uno(cone, id, titulo, referer, infringe, fecha, nombre_tabla):
    nombre_tabla = scrub(nombre_tabla)
    #sql_check = 'SELECT EXISTS(SELECT 1 FROM {} WHERE titulo=? LIMIT 1)'\
    #    .format(nombre_tabla)
    sql_actualiza = 'UPDATE {} SET titulo=%s, referer=%s, infringe=%s, fecha=%s WHERE id=%s'\
        .format(nombre_tabla)
    #c = cone.execute(sql_check, (titulo,))    # es necesaria la coma
    try:
        curs = cone.cursor()
        curs.execute(sql_actualiza, (titulo,referer,infringe,id))
        cone.commit()
    #resultados = c.fetch_one()
    #if result[0]:
    #    c.execute(sql_actualiza, (titulo,referer,infringe,id))
    #    cone.commit()
    except:
        raise mvc_exc.ItemNoGuardado('No se puede actualizar "{}" porque no existe en la tabla "{}"'
            .format(id, nombre_tabla))
        
@conecta
def elimina_uno(cone, id, nombre_tabla):
    nombre_tabla = scrub(nombre_tabla)
    #sql_check = 'SELECT EXISTS(SELECT 1 FROM {} WHERE titulo=? LIMIT 1)'\
    #    .format(nombre_tabla)
    #nombre_tabla = scrub(nombre_tabla)
    sql_elimina = 'DELETE FROM {} WHERE id=%s'.format(nombre_tabla)
    #c = cone.execute(sql_check, (titulo,)) # es necesaria la coma
    #resultados = c.fetch_one()
    try:
        curs = cone.cursor()
        curs.execute(sql_elimina, (id,))
        cone.commit()
    #if resultados[0]:
    #    c.execute(sql_elimina, (id,))
    #    cone.commit()
    #else:
    except:
        raise mvc_exc.ItemNoGuardado('No se puede eliminar "{}" porque no existe en la tabla "{}"'
            .format(name, nombre_tabla))
        
@conecta
def elimina_todo(cone, nombre_tabla):
    nombre_tabla = scrub(nombre_tabla)
    sql_elimina = 'DELETE FROM {}'.format(nombre_tabla)
    try:
        curs = cone.cursor()
        curs.execute(sql_elimina)
        cone.commit()
    except:
        raise mvc_exc.ItemNoGuardado('La tabla "{}" ya se encuentra vacia...'
            .format(nombre_tabla))
        
        
def main():
    '''
    nombre_tabla = 'Jess'
    cone = conecta_BD(BD_nombre)
    
    # CREA TABLA
    #crea_tabla(cone, nombre_tabla)
    # ELIMINA TABLA
    #elimina_tabla(cone, nombre_tabla)
    
    my_items = [
    {'id': 1,
    'titulo': 'DESCARGAR CD COMPLETO PARA QUE LE HAGO DAnO',
    'referer': 'https://musicapalabanda.org/descargar-cd-completo-para-que-le-hago-dano/',
    'infringe': 'http://adf.ly/7342230/valedoresparaquelehagodao'},
          
    {'id': 2,
    'titulo': 'DESCARGAR CD COMPLETO ?LOS VALEDORES DE LA SIERRA?',
    'referer': 'https://musicapalabanda.org/descargar-cd-completo-los-valedores-de-la-sierra/',
    'infringe': 'http://adf.ly/7342230/valedoresenascenso'}
    ]
    
    # CREA
    #insertar_varios(cone, my_items, nombre_tabla)
    
    # ACTUALIZA
    #Actualiza_uno(cone, 2, 'Hola', 'https://musicapalabanda.org/descargar-cd-completo-','http://adf.ly/7342230/valedoresenascens', nombre_tabla)
    
    
    # READ
    print('SELECT 1')
    print(selecciona_uno(cone, 1, nombre_tabla=nombre_tabla))
    print('SELECT todos')
    print(selecciona_todos(cone, nombre_tabla=nombre_tabla))
    
    # DELETE
    print('DELETE 1')
    elimina_uno(cone, 1, nombre_tabla=nombre_tabla)
    print(selecciona_todos(cone, nombre_tabla=nombre_tabla))

    # DELETE
    #print('DELETE todo')
    #elimina_todo(cone, nombre_tabla=nombre_tabla)
    
    # CIERRA CONEXION
    #cone.close()
    '''
