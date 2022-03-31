import csv
import sys
import random
from logger_base import log
import pyodbc                   #utilizamos la librería pyodbc que nos permite gestionar la conexión con SQL Server

_SQL_USER = 'sa'
_SQL_PASSWD = 'Joe040887'
_SQL_HOSTNAME = 'JUANI\SQLSERVER'       #definimos la credenciales por defecto para la conexión a la base de datos 'Santander'
_SQL_DB = 'Santander'

class Conec:                    #engloba la creación del objeto conexión y los métodos para el intercambio de datos de las tablas

    @classmethod
    def conectar(cls):                      #método conectar crea el objeto de conexión con las credenciales para utilizarlo por el objeto cursor
        try:
            conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=' + _SQL_HOSTNAME + ';DATABASE=' + _SQL_DB + ';Trusted_Connection=yes;UID=' + _SQL_USER + ';PWD=' + _SQL_PASSWD)
            conexion.autocommit = True
        except Exception as e:
            log.debug(f'Falló la conexión a la base de datos {_SQL_DB} de SQL Server: {e}')        #log en modo debug para especificar errores de conexión
            sys.exit()
        if __name__ == '__main__':
            print(f'Conexión exitosa a la base de datos {_SQL_DB} de SQL Server')
        return conexion

    @classmethod
    def get_user_name(cls,ID_USER):                                                             #Seleccionamos el nombre del usuario ingresado
        cursor = Conec.conectar().cursor()
        first_name = cursor.execute('SELECT First_Name FROM Usuarios WHERE USER_ID = ?',ID_USER).fetchval()
        return first_name

    @classmethod
    def get_user_lname(cls, ID_USER):                                                           #Seleccionamos el apellido del usuario ingresado
        cursor = Conec.conectar().cursor()
        last_name = cursor.execute('SELECT Last_Name FROM Usuarios WHERE USER_ID = ?', ID_USER).fetchval()
        return last_name

    @classmethod
    def get_session_id(cls):                                                                    #Seleccionamos el último SESSION_ID e incrementamos en 1
        cursor = Conec.conectar().cursor()
        session_id = cursor.execute('SELECT MAX(SESSION_ID) FROM Actividades_Usuarios').fetchval()
        session_id += 1                                                                         #NOTA: SESSION_ID no puede ser un campo declarado como
        return session_id                                                                       # Identity, ya que si bien es único por cada sesión
                                                                                                # se repite cada vez en el registro por cada EVENT_ID
    @classmethod
    def define_system(cls,random):
        os = ['Win7','Win8','Win10','Win11','Andro','IOS']                                      #datos de OS generados aleatoriamente
        system = os[random]
        return system

    @classmethod
    def define_browser(cls,random):                                                             #datos de Browser generados aleatoriamente
        browser = ['APP','Chrome','Firefox','Edge']
        naveg = browser[random]
        return naveg

    @classmethod
    def define_device(cls,random):
        device = ['Galaxy A2','Galaxy A5','Galaxy A7','Galaxy A12','Huawei','Xiaomi','LG KP','Moto E20','Moto E40','Iphone 10','Iphone 12','PC AMD Ryzen','PC Core I7','HP Note','Sony Vaio','Dell Lat','Lenovo','Acer','Asus']
        disp = device[random]
        return disp                                                                             #datos del dispositivo seleccionados aleatoriamente

    @classmethod
    def get_segment(cls):
        cursor = Conec.conectar().cursor()                                                      #segmento del usuario seleccionado aleatoriamente
        id = random.randrange(100,1100,100)
        seg = cursor.execute('SELECT SEGMENT_DESCRIPTION FROM Segmentos WHERE SEGMENT_ID = ?',id).fetchval()
        return id,seg

    @classmethod
    def get_city(cls):
        ciudad = ['Buenos Aires','CABA','Catamarca','Chaco','Chubut','Córdoba','Corrientes','Entre Ríos','Formosa','Jujuy','La Pampa','La Rioja','Mendoza','Misiones','Neuquén','Río Negro','Salta','San Juan','San Luis','Santa Cruz','Santa Fe','Santiago del Estero','Tierra del Fuego']
        city = ciudad[random.randrange(1,23,1)]
        return city                                                                             #ciudad del usuario seleccionada aleatoriamente

    @classmethod
    def get_event(cls,id):                                                                      #descripción del EVENT_ID seleccionado
        cursor = Conec.conectar().cursor()
        event = cursor.execute('SELECT EVENT_DESCRIPTION FROM Eventos WHERE EVENT_ID = ?',id).fetchval()
        return event

    @classmethod                                                                                #método para crear las tablas en la base de datos
    def crear_tablas(cls):
        try:
            cursor = Conec.conectar().cursor()

            cursor.execute('CREATE TABLE Actividades_Usuarios('                                 #Tabla de hechos Actividades_Usuarios
                           'USER_ID NUMERIC(38,0) NOT NULL,'
                           'SESSION_ID NUMERIC(38,0) NOT NULL,'
                           'SEGMENT_ID NUMERIC(38,0) NOT NULL,'
                           'SEGMENT_DESCRIPTION VARCHAR(100),'
                           'USER_CITY VARCHAR(50),'
                           'SERVER_TIME TIMESTAMP,'
                           'DEVICE_BROWSER VARCHAR(10),'
                           'DEVICE_OS VARCHAR(5),'
                           'DEVICE_MOBILE VARCHAR(10),'
                           'TIME_SPENT NUMERIC(38,0),'
                           'EVENT_TIME DATETIME NOT NULL,'          
                           'EVENT_ID NUMERIC(38,0),'
                           'EVENT_DESCRIPTION VARCHAR(50),'
                           'CRASH_DETECTION VARCHAR(100))')

            print('tabla Actividades_Usuarios creada...')

            cursor.execute('CREATE TABLE Primer_Sesion('                                        # Tabla de hechos Primer_Sesion
                           'USER_ID NUMERIC(38,0) NOT NULL,'
                           'SESSION_ID NUMERIC(38,0) NOT NULL,'
                           'EVENT_TIME DATETIME NOT NULL,'
                           'EVENT_ID NUMERIC(38,0),'
                           'EVENT_DESCRIPTION VARCHAR(50),')

            print('tabla Primer_Sesion creada...')

            cursor.execute('CREATE TABLE Usuarios('                                             #Tabla de dimensión Usuarios
                       'USER_ID INT NOT NULL PRIMARY KEY, '
                       'First_Name VARCHAR(50) NOT NULL, '
                       'Last_Name VARCHAR(50) NOT NULL, '
                       'Account_Number BIGINT NOT NULL, '
                       'Email VARCHAR(100) NOT NULL)')

            print('tabla Usuarios creada...')

            cursor.execute('CREATE TABLE Segmentos('                                            #Tabla de dimensión Segmentos
                           'SEGMENT_ID NUMERIC( NOT NULL PRIMARY KEY, '
                           'EVENT_DESCRIPTION VARCHAR(50) NOT NULL)')

            print('tabla Eventos creada...')

            cursor.execute('CREATE TABLE Eventos('                                              #Tabla de dimensión Eventos
                           'EVENT_ID INT NOT NULL PRIMARY KEY, '
                           'EVENT_DESCRIPTION VARCHAR(50) NOT NULL)')

            print('tabla Eventos creada...')

        except Exception as e:
            print(f'falló la conexión al crear las tablas para la base de datos de SQL Server: {_SQL_DB} error: {e}')

class Insertar:                         #abarca las acciones de insersión de datos, tanto de los registros del archivo fuente, como la tabla de hechos

    INSERT_User = 'INSERT INTO Usuarios (USER_ID,First_Name,Last_Name,Account_Number,Email) VALUES (?,?,?,?,?)'
    INSERT_Actividad = 'INSERT INTO Actividades_Usuarios(USER_ID,SESSION_ID,SEGMENT_ID,SEGMENT_DESCRIPTION,' \
                       'USER_CITY,DEVICE_BROWSER,DEVICE_OS,DEVICE_MOBILE,EVENT_TIME,EVENT_ID,EVENT_DESCRIPTION) ' \
                       'VALUES (?,?,?,?,?,?,?,?,getdate(),?,?)'
    GET_TIME = 'WITH Up_Time as(SELECT USER_ID,SESSION_ID, DATEDIFF(mi,min(CASE WHEN EVENT_ID = 1 THEN EVENT_TIME END), min(CASE WHEN EVENT_ID = 2 THEN EVENT_TIME END)) as TIME_SESSION ' \
               'FROM Actividades_Usuarios ' \
               'WHERE EVENT_ID in (1, 2) ' \
               'GROUP BY USER_ID, SESSION_ID) SELECT TIME_SESSION FROM Up_Time WHERE SESSION_ID = ?'
    UPDATE_TS = 'UPDATE Actividades_Usuarios SET TIME_SPENT = ? WHERE SESSION_ID = ?'

    @classmethod
    def obtener_registros(cls,archivo):
        info = open(f'{archivo}/{archivo}.csv','r',newline='')
        lectura = csv.reader(info)
        next(lectura)                                                       #obtenemos los registros del archivo CSV creado y los inserta en la
        cursor = Conec.conectar().cursor()                                  #tabla Usuarios
        rows = []
        i = 0
        for row in lectura:
            rows.append(row)
            cursor.execute(cls.INSERT_User,rows[i])
            i += 1
        print('Registros insertados en la tabla Usuarios')
        info.close()
                                                                            #método update actualiza todos los movimientos por sesión en tabla Actividades
    @classmethod
    def update_event(cls,ID_USER,ID_SESSION,ID_SEGMENT,SEGMENT_DESCRIPTION,USER_CITY,DEVICE_BROWSER,DEVICE_OS,DEVICE_MOBILE,EVENT_ID,EVENT_DESCRIPTION):
        cursor = Conec.conectar().cursor()
        cursor.execute(cls.INSERT_Actividad,ID_USER,ID_SESSION,ID_SEGMENT,SEGMENT_DESCRIPTION,USER_CITY,DEVICE_BROWSER,DEVICE_OS,DEVICE_MOBILE,EVENT_ID,EVENT_DESCRIPTION)


    @classmethod                                                            #método que calcula y actualiza el campo TIME_SPENT para la sesión realizada
    def time_session(cls,ID_SESSION):
        cursor = Conec.conectar().cursor()
        t_sesion = cursor.execute(cls.GET_TIME,ID_SESSION).fetchval()
        cursor.execute(cls.UPDATE_TS,t_sesion,ID_SESSION)
        return t_sesion


if __name__ == '__main__':

 input(print('Archivo de soporte "Conexion_db"'))

 # Conec.conectar()
 # Conec.crear_tablas()
 #  tiempo_sesion = Insertar.time_session(1079)
 #  input(print(tiempo_sesion))
 #  segmen = Conec.get_segment()
 #  segmen = list(segmen)
 #  ciudad = Conec.get_city()
 #  evento = Conec.get_event(3)
 #  nombre = Conec.get_user_name(25)
 #  apellido = Conec.get_user_lname(25)
 #  sesion = Conec.get_session_id()
 #  sistema = Conec.define_system(random.randrange(0, 6, 1))
 #  navegador = Conec.define_browser(random.randrange(0, 4, 1))
 #  device = Conec.define_device(random.randrange(0,19,1))
 #  print(f'{segmen[0]} {segmen[1]}')
 #  print(f'{nombre} {apellido} {ciudad} {sesion} {sistema} {navegador} {device} {evento}')
 #  Insertar.update_event(78, sesion, segmen[0], segmen[1], ciudad, navegador, sistema, device, 1, 'Login')
