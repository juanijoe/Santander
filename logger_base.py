import logging as log

log.basicConfig(level=log.DEBUG,    #seleccionamos el nivel, por default siempre se muestra a nivel de WARNING en adelante
                format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
                datefmt='%I:%M:%S %p',   #declaramos estos parámetros para que nos indique que archivo está comunicando, el tiempo
                handlers = [               #y el nivel de logging, número de linea y mensaje
                   log.FileHandler('datos_log.log'),   #agrega la información a un archivo creado
                   log.StreamHandler()
                ])

if __name__ == '__main__':

    input(print('Archivo soporte "logger_base"'))

    #log.debug('mensaje a nivel debug')
    #log.info('mensaje a nivel info')
    #log.warning('mensaje a nivel warning')
    #log.error('mensaje a nivel error')
    #log.critical('mensaje a nivel critical')

