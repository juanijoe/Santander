import os
import shutil
import csv
import sys
from logger_base import log

#declaramos la clase normalizar para tomar los registros y crear el archivo CSV

class normalizar:

    @classmethod
    def to_csv(cls,archivo):
            try:
                if os.path.exists(f'{archivo}'):                #consultamos si existe el directorio del archivo
                    shutil.rmtree(f'{archivo}')                 #en caso de existir previamente se elimina
                os.makedirs(f'{archivo}/', exist_ok=True)       #se crea inmediatamente para contar con el registro actualizado
            except Exception as e:
                log.error(f'Ocurrió un error al crear el directorio: {e}')
            try:
                with open('datos_data_engineer.tsv', 'r',newline='',encoding='utf-16le') as f:                   #abrimos el archivo fuente en cod. UTF-16LE
                    data = csv.reader(f, delimiter='\t')                                                         #indicamos delimitador de campos
                    registros = csv.writer(open(f'{archivo}/{archivo}.csv', 'w',newline='',encoding= 'utf8'))    #abrimos un nuevo archivo CSV
                    rows = []
                    i = 0
                    for row in data:
                        rows.append(row)
                    input(print(f'Cantidad de Registros: {len(rows)}'))             #Registros almacenados en el arreglo
                    j = len(rows)
                    while i < j:                                                    #Quitamos los caracteres especiales tomados como literales
                        linea = str(rows[i]).replace('[','').replace(']','').replace(',','|').replace('\'','').replace('ufeff','').replace('\\','')
                        valor = linea.count('|')                                    #Convertimos a Str y reemplazamos ',' por '|' como delimitador
                        while valor < 4:
                            print(f'Linea incorrecta({i}: {linea}')
                            linea2 = str(rows[i+1]).replace('[','').replace(']','').replace(',','|').replace('\'','').replace(' ','')
                            linea = linea + linea2
                            lin_fix = linea                                         #Reconstruímos en forma recursiva registros mal ingresados
                            valor = linea.count('|')                                #asegurando que todas las lineas cuenten con 5 elementos
                            elem_vacio = list(linea.split('|'))
                            largo = len(elem_vacio)
                            if largo == 5 and len(elem_vacio[largo-1]) < 2 :        #verificamos que el ùltimo elemento añadido no sea nulo por error
                                valor -= 1
                            elif largo == 5 and len(elem_vacio[largo-1]) > 2:
                                lin_fix = list(lin_fix.split('|'))
                                print(f'Linea Reconstruída: {lin_fix}')             #Obtenemos la línea recompuesta
                            i += 1
                        linea = list(linea.split('|'))                              #convertimos a tipo list para añadir al CSV
                        elemento = linea
                        elemento_3 = str(elemento[3])
                        elemento_limpio3 = ''.join(filter(str.isalnum, elemento_3))         #Quitamos caracteres especiales indebidos al número de cuenta
                        registros.writerow([elemento[0],elemento[1],elemento[2],elemento_limpio3,elemento[4]])      #añadimos los registros al archivo
                        i += 1
                print(f'Archivo "{archivo}.csv" creado...')
            except Exception as e:
                log.error(f'Ocurrió un error al leer el archivo de origen: {e}')
                sys.exit()

if __name__ == '__main__':                      #verificación solo ejecutable desde normalizar.py
    normalizar.to_csv('Clientes')