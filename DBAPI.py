import os
from conexion_db import Conec
from conexion_db import Insertar
import sys
import random

#inicia menú principal de sesiones...

clearConsole = lambda: os.system('cls')
if __name__ == '__main__':
    while (True):
        clearConsole()
        print('''
            BIENVENIDO AL HOMEBANKING DE SANTANDER
            
            Ingrese su Número de ID de Cliente (1 a 1000) para Comenzar
            
            
            o presione 0 para salir...
            ''')
        try:
            ID_USER = int(input(f'ID Cliente: '))                           #Solo usuarios del listado, otro valor es rechazado
            if ID_USER == 0:
                sys.exit()
            elif 1 > ID_USER or ID_USER > 1000:
                print('Valor Incorrecto, intente nuevamente...')
            elif 0 < ID_USER < 1001:                                        #Traemos los datos del usuario ingresado de la tabla Usuarios
                first_name = Conec.get_user_name(ID_USER)
                last_name = Conec.get_user_lname(ID_USER)
                print(f'Bienvenido {first_name} {last_name}'.center(60, '-'))
                ID_SESSION = Conec.get_session_id()
                sistema = Conec.define_system(random.randrange(0, 6, 1))
                navegador = Conec.define_browser(random.randrange(0, 4, 1))
                device = Conec.define_device(random.randrange(0, 19, 1))
                segmen = Conec.get_segment()
                segmen = list(segmen)
                ciudad = Conec.get_city()
                Insertar.update_event(ID_USER, ID_SESSION, segmen[0], segmen[1], ciudad, navegador, sistema, device, 1,'Login')
                while(True):
                    print('''
                            1)Consultar Caja de Ahorros
                            2)Consultar Cuenta Corriente
                            3)Consultar Préstamos
                            4)Consultar Tarjeta de Crédito
                            5)Consultar Alta de Servicio
                            6)Consultar Baja de Servicio
                            7)Consultar Seguros
                            8)Consultar Fondos de Inversión
                            9)Alta Plazo Fijo
                            10)Consultar Plazo Fijo
                            11)Compra/Venta de Moneda Extranjera
                            12)Configuración Datos Personales
                            13)Consultar Términos y Condiciones
                            14)Consultar Promociones y Descuentos
                            15)Transferencias
                            16)Consultar Pedidos y Reclamos
                            17)Gestionar Claves y Token
                            18)Movimientos Históricos de Cuentas
                            19)Cerrar Sesión
                                ''')
                    opcion = int(input(f'Elige una opción: '))
                    if 0 > opcion or opcion > 19:
                        print(f'Valor ingresado incorrecto, elige una opción...')
                    elif 1 <= opcion <= 18:
                        clearConsole()
                        evento = Conec.get_event(opcion + 2)
                        Insertar.update_event(ID_USER,ID_SESSION,segmen[0],segmen[1],ciudad,navegador,sistema,device,opcion + 2,evento)
                        input(print(f'Menú {evento}...'))
                    elif opcion == 19:
                        clearConsole()
                        Insertar.update_event(ID_USER, ID_SESSION, segmen[0], segmen[1], ciudad, navegador, sistema,device, 2, 'Logout')
                        Insertar.time_session(ID_SESSION)
                        input(print(f'Sesión Finalizada'))
                        break
        except Exception as e:
            print(input('\nOcurrió un Error, Intente otro valor'))
            clearConsole = lambda: os.system('cls')
            clearConsole()