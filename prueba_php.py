import mysql.connector
from mysql.connector import Error
from twisted.conch.test.test_connection import connection

class MyBD:
    
    try:
        connection = mysql.connector.connect(host='192.168.100.9',
                                             database='apdif',
                                             user='apdif',
                                             password='TZaJsYQqMjY1lHOK')
        if connection.is_connected():
            sql_select_Query = "select * from mplb"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
                
            for row in records:
                print("id = ", row[0], )
                print("titulo = ", row[1])
                print("referer  = ", row[2])
                print("infringe  = ", row[3], "\n")
    except Error as e:
        print("Error al conectarse a MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("La conexion a MySQL fue cerrada")
    
    def conecta_BD(self):
        try:
            connection = mysql.connector.connect(host='192.168.100.9',
                                             database='apdif',
                                             user='apdif',
                                             password='TZaJsYQqMjY1lHOK')
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Conectado al servidor de MySQL version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("Estas conectado a la base de datos: ", record)
                
                '''db_Info = connection.get_server_info()
                print("Conectado al servidor de MySQL version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("Estas conectado a la base de datos: ", record)'''
                #return connection        
        except Error as e:
            print("Error al conectarse a MySQL", e)
        finally:
            if (connection.is_connected()):
                cursor.close()
                connection.close()
                print("La conexion a MySQL fue cerrada")
    
    
    def cierra_BD(self, connection):
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("La conexion a MySQL fue cerrada")
        
            
    def consulta(self, tabla):
        sql_select_Query = "select * from " + tabla
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        self.imprime_tabla(records)
        
        
        
    def imprime_tabla(self, records):
        for row in records:
            print("id = ", row[0], )
            print("titulo = ", row[1])
            print("referer  = ", row[2])
            print("infringe  = ", row[3], "\n")
            
            
            
#BD = MyBD()
#conector = BD.conecta_BD()
#BD.conecta_BD()
#BD.consulta('mplb')
#BD.cierra_BD(conector)