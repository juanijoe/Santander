# Data Engineer Programming Test

### SQL

Para este test hemos creado un entorno inventado que simula situaciones de nuestra arquitectura actual. El candidato debe suponer que es un empleado del banco Santander y debe resolver una situación planteada por un área de negocio.

En este escenario, los datos de logueo de los usuarios del Santander se encuentran en una única tabla sobre BigQuery. En esta table se guarda toda la información referente a las actividades realizan los usuarios cuando ingresan al Home Banking de Santander. La estructura de dicha tabla se pueden ver a continuación:

![image](https://user-images.githubusercontent.com/62435760/127665003-e3aad47b-616d-44aa-af21-c25249e11123.png)

Basado en esa tabla, el área de la banca privada del banco desea que se arme un modelo dimensional en donde se contemplen dos tablas principales:

●	La primera vez que el usuario se logueo al Home Banking. Asumiendo que dicha situación es un tipo de evento.

●	La actividad diaria de cada usuario.

Tenga en cuenta las siguientes consideraciones técnicas:

1.	La table de origen contiene mil millones de registros.
2.	El modelo a construer debe poder ejecutarse tanto en consolas SQL o en herramientas de BI.
3.	Uno de los KPIs mas importantes que tiene la organización es la de retención de clientes. Dicho KPI es el porcentaje de usuarios que realizaron una actividad diferente al login durante 2 dos días consecutivos y cuya sesión haya durando al menos 5 minutos.

### Pregunta 1
Como resolvería este tipo de petición? Explique detalladamente el proceso de limpieza y transformación del modelo inicial. Que tecnologías utilizaría y por que?

R: Para resolver el tipo de petición requerido por el KPI, primero definimos la Base de Datos que vamos a utilizar sobre la cual requerir las consultar adecuadas.

En este sentido, seleccionamos la plataforma SQL Server 2019 como motor y gestor de la base de datos. La razón de dicha elección se fundamenta en la solidez de rendimiento y la agilidad de uso, con herramientas intuitivas aplicadas a la construcción de las consultas.

Para iniciar el proceso de limpieza y transformación de la información, primeramente se crean las tablas necesarias en la base de datos. Para ello hacemos uso de Python como soporte de programación.
A fin de vincular al programa con la base de datos, recurrimos a la librería 'pyodbc'

Se determinan las tablas Actividades_Usuarios y Primer_Sesion como el soporte principal de la actividad a ser analizada. Se añaden las tablas Usuarios, Segmentos y Eventos como soporte de datos complementarios.

A partir de las tablas mencionadas, haciendo foco en la consigna, se define atender a cada una de las condiciones planteadas en forma no concurrente, para luego enlazar todos aquellos registros en común que cumplan los requisitos. De esta manera se definen tres modelos de Consulta:

Sesiones_Consecutivas: CTE que nos marca aquellos usuarios que han efectuado sesiones por al menos dos días consecutivos

    ![Sesiones_Consecutivas](https://user-images.githubusercontent.com/101049711/161111306-a7ba0898-f155-458f-aa3d-5e43bdb583cf.jpg)

Sesiones_Extensas: CTE que señala los usuarios cuyas sesiones igualan o superan los 5 minutos de actividad

    ![Sesiones_Extensas](https://user-images.githubusercontent.com/101049711/161111409-5c370bb9-5e77-499b-bd06-db8b099d48fd.jpg)

Diferente_Login: CTE que individualiza los usuarios con actividad en sesiones diferente al login

    ![Diferente_Login](https://user-images.githubusercontent.com/101049711/161111462-bce3b77b-a206-4b40-b80e-81dddc859428.jpg)

Con estos datos señalados, podemos obtener las vistas gráficas de cada consulta. A continuación, sumamos la información de la tabla Usuarios, que contiene la totalidad de usuarios registrados.

    ![Porcentaje_Condiciones](https://user-images.githubusercontent.com/101049711/161111531-ff0f0274-69e1-4447-8c83-8571fa561e56.jpg)

Finalmente vinculando este dato, con el filtrado por la sumatoria de condicionales aplicados como el total de usuarios que cumplen los requisitos, podemos obtener el porcentaje de los mismos, respecto al total de usuarios. Esto se realiza en forma dinámica, es decir, atendiendo a que ambos datos depurados pueden verse modificados como consecuencia de la actividad

### Ejercicio 1
Realice el DER que de soporte al modelo dimensional solicitado por la banca privada.

![image](https://github.com/juanijoe/Santander/blob/main/Modelo_DER.jpg)

### Ejercicio 2 
Escriba las queries necesarias partiendo de la tabla inicial y que de como resultado el modelo planteado en el ejercicio anterior.

R: a continuación se muestra el modelo de Queries necesarios para llevar a cabo la consulta planteada

![KPI_Retencion_Clientes](https://user-images.githubusercontent.com/101049711/161111633-5e53059c-77c1-45c5-b161-4558e45c4101.jpg)


### Ejercicio 3
Escriba la consulta necesaria para obtener el KPI de retención de clientes para los 10 clientes que mas veces se hayan logueado en el último mes.

R: a continuación se muestra el modelo de Queries necesarios para la KPI solicitada:

![KPI_Top10_Usuarios](https://user-images.githubusercontent.com/101049711/161111679-cb4985c5-eb2b-499e-9746-efb72fb961d5.jpg)


### Python 
(Para hacerlo interesante, usar Python 2.7)

Se deberá escribir un script que transforme el archivo datos_data_engineer.tsv en un archivo CSV que pueda ser insertado en una base de datos, y/o interpretado por cualquier parser estándar de archivos delimitados, de la manera más sencilla posible.

El archivo resultante debe tener las siguientes características:
* Cada row contiene la misma cantidad de campos
* Los campos se separan con un pipe |
* Se deben poder leer correctamente los caracteres especiales que estén presentes en los campos actuales del archivo. 
* El encoding del archivo final debe ser UTF-8 (datos_de_santander.tsv es un archivo UTF-16LE)

R: El ejercicio planteado para Python se encuentra resuelto en el archivo normalizar.py
