# Santander
Challenge Data Engineer Programming Test

Bienvenido al repositorio de resolución del challenge. Dentro del mismo se encentran todos los archivos abocados a lo solicitado. Para tener en cuenta:

Los archivos de Python:
    
   * normalizar.py : contiene el código fuente para transformar el archivo 'datos_data_engineer.tsv' en el .CSV solicitado, reparando los registros incorrectos
   * logger_base.py : archivo estándar utilizado para aplicar el modo debug en el manejo de errores, implementado en ciclos try-except
   * conexion_db.py : contiene las clases y los métodos para establecer la conexión con la base de datos, la creación de tablas y actualización de registros
   * DBAPI.py : archivo principal de ejecución para simulación del proceso de sesión de usuario. Actualiza con eventos ficticios la tabla principal para fines prácticos
   
Los archivos de SQL:

   * KPI_Retencion_Clientes: archivo .sql que posee el código listo para ser ejecutado como Query. Resuelve la consulta del Ejercicio 2
   * KPI_TOP10_Usuarios: archivo .sql contiene el código para ser ejecutado como Query. Resuelve la consulta del Ejercicio 3
   * Clientes: archivo .csv creado en Python que almacena la lista de clientes brindada

Además se encuentra el contenido de imágenes de cada fragmento de Query en particular para cada función, ejecutados con un extracto del resultado obtenido por tabla, a modo de muestra.

Todos los archivos involucrados se encuentran internamente comentados para poder guiar su lógica y funcionamiento.

Gracias por su atención
