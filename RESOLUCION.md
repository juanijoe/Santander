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

    * Sesiones_Consecutivas: CTE que nos marca aquellos usuarios que han efectuado sesiones por al menos dos días consecutivos

    ![image](https://github.com/juanijoe/Respaldo/blob/main/Sesiones_Consecutivas.jpg)
    
    * Sesiones_Extensas: CTE que señala los usuarios cuyas sesiones igualan o superan los 5 minutos de actividad

    ![image](https://github.com/juanijoe/Respaldo/blob/main/Sesiones_Extensas.jpg)

    * Diferente_Login: CTE que individualiza los usuarios con actividad en sesiones diferente al login

    ![image](https://github.com/juanijoe/Respaldo/blob/main/Diferente_Login.jpg)

Con estos datos señalados, podemos obtener las vistas gráficas de cada consulta. A continuación, sumamos la información de la tabla Usuarios, que contiene la totalidad de usuarios registrados.

    ![image](https://github.com/juanijoe/Respaldo/blob/main/Porcentaje_Condiciones.jpg)

Finalmente vinculando este dato, con el filtrado por la sumatoria de condicionales aplicados como el total de usuarios que cumplen los requisitos, podemos obtener el porcentaje de los mismos, respecto al total de usuarios. Esto se realiza en forma dinámica, es decir, atendiendo a que ambos datos depurados pueden verse modificados como consecuencia de la actividad

### Ejercicio 1
Realice el DER que de soporte al modelo dimensional solicitado por la banca privada.

![image](https://github.com/juanijoe/Santander/blob/main/Modelo_DER.jpg)

### Ejercicio 2 
Escriba las queries necesarias partiendo de la tabla inicial y que de como resultado el modelo planteado en el ejercicio anterior.

R: a continuación se muestra el modelo de Queries necesarios para llevar a cabo la consulta planteada

------------------------------------------------- KPI RETENCIÓN DE CLIENTES ---------------------------------------------------------------

;WITH Sesiones_Consecutivas as (			        -- Filtramos los Usuarios que poseen Actividad con Sesiones durante 2 días Consecutivos
					SELECT USER_ID,SESSION_ID,
					DATEDIFF(day,SERVER_TIME,LAG(SERVER_TIME) OVER (ORDER BY USER_ID,SESSION_ID)) as RESULT
				    FROM Actividades_Usuarios SC
					WHERE EVENT_ID = 1				----------- De la vista obtenida, se concluye que los usuarios que cumplen la condición,
					),								----------- son aquellos cuyo resultado es al menos una vez '-1' y poseen más de un SESSION_ID
	 Sesiones_Largas as(
					SELECT USER_ID, SESSION_ID,							
						min(CASE WHEN EVENT_ID = 1 THEN SERVER_TIME END) AS START_TIME_SESSION,
						min(CASE WHEN EVENT_ID = 2 THEN SERVER_TIME END) AS END_TIME_SESSION,
						DATEDIFF(mi,min(CASE WHEN EVENT_ID = 1 THEN SERVER_TIME END), min(CASE WHEN EVENT_ID = 2 THEN SERVER_TIME END)) as TIME_SESSION,
						COUNT(SESSION_ID) OVER (PARTITION BY USER_ID) as CANTIDAD_SESIONES	
					FROM Actividades_Usuarios SL
					WHERE EVENT_ID in (1, 2)		------- Filtramos los Usuarios con Sesiones Extensas. Para ello tomamos el tiempo de cada
					GROUP BY USER_ID, SESSION_ID	------- Sesión como la diferencia entre el tiempo de Login con el tiempo de Logout registrado
													------- Además utilizamos el mismo particionado para obtener la Cantidad de Sesiones
					),
	Diferente_Login as(								------- Filtramos los Usuarios con actividad de sesión diferente al Login
					SELECT DISTINCT USER_ID, 
					COUNT(EVENT_ID) OVER (PARTITION BY SESSION_ID)as CANTIDAD 
					FROM Actividades_Usuarios  DL			
					),								-- El valor CANTIDAD evidencia actividad diferente si supera el valor de 2(Login + Logout)
		   Totales as(
					SELECT USER_ID, MAX(USER_ID) AS Total_Usuarios
					FROM Usuarios							
					GROUP BY USER_ID				----- Se agrega el valor máximo de usuarios en forma dinámica, no como parámetro estático
					)
					SELECT MAX(Total_Usuarios) 'USUARIOS/TOTAL USUARIOS',
						   MAX(Total_Usuarios) * 100.00 / MAX(Total_USuarios) 'PORCENTAJE CONDICIONES' FROM Totales
					UNION
					SELECT COUNT(DISTINCT Sesiones_Largas.USER_ID) as USUARIOS, 
						   CONVERT(numeric(38, 2), (COUNT(DISTINCT Diferente_Login.USER_ID)) * 100.00 / MAX(Total_Usuarios)) AS Porcentaje_Usuarios
					FROM Sesiones_Consecutivas 
					INNER JOIN
                    Diferente_Login ON Diferente_Login.USER_ID = Sesiones_Consecutivas.USER_ID 
					INNER JOIN
                    Sesiones_Largas ON Sesiones_Largas.USER_ID = Sesiones_Consecutivas.USER_ID 
					INNER JOIN
                    Totales ON Sesiones_Largas.USER_ID = Totales.USER_ID
					WHERE Diferente_Login.CANTIDAD > 2 AND Sesiones_Largas.TIME_SESSION >= 5 
					AND Sesiones_Consecutivas.RESULT = - 1 AND Sesiones_Largas.CANTIDAD_SESIONES > 1
					
		---------------- Finalmente, la aplicación de las claúsulas mencionadas en las anteriores CTE, permite obtener la cantidad
		---------------- y el porcentaje de usuarios que complen las condiciones solicitadas, respecto del total de usuarios

### Ejercicio 3
Escriba la consulta necesaria para obtener el KPI de retención de clientes para los 10 clientes que mas veces se hayan logueado en el último mes.

R: a continuación se muestra el modelo de Queries necesarios para la KPI solicitada:

------------------------------------------------- KPI TOP 10 USUARIOS MAS LOGIN ULTIMO MES ------------------------------------------------

											------- El siguiente Query nos permite obtener el listado de usuarios con mayor cantidad de logins
;WITH TOP10_Usuarios as(					------- Durante el último mes calendario (30 últimos días desde la fecha) 
	   SELECT DISTINCT USER_ID,				
			COUNT(SESSION_ID) OVER (PARTITION BY USER_ID) as Cantidad_Login,
			MIN(EVENT_TIME) OVER (PARTITION BY USER_ID) as Primer_Login,
		    MAX(EVENT_TIME) OVER (PARTITION BY USER_ID) as Ultimo_Login
			FROM Primer_Sesion
			WHERE EXISTS (SELECT EVENT_TIME FROM Actividades_Usuarios WHERE EVENT_TIME<=GETDATE() AND EVENT_TIME>=DATEADD(day,-30,getdate()))
			)
	   SELECT DISTINCT TOP 10 U.USER_ID,Cantidad_Login,Primer_Login,Ultimo_Login,U.First_Name,U.Last_Name,U.Account_Number,U.Email 
	   FROM TOP10_Usuarios TP
	   INNER JOIN Usuarios U				-------- Uniendo el filtrado de la cantidad de logins en forma vincular con los datos de la tabla
	   ON U.USER_ID = TP.USER_ID		    -------- Usuarios, podemos obtener la información buscada, restringiendo a los 10 usuarios que
	   ORDER BY Cantidad_Login DESC			-------- cumplen lo solicitado

### Python 
(Para hacerlo interesante, usar Python 2.7)

Se deberá escribir un script que transforme el archivo datos_data_engineer.tsv en un archivo CSV que pueda ser insertado en una base de datos, y/o interpretado por cualquier parser estándar de archivos delimitados, de la manera más sencilla posible.

El archivo resultante debe tener las siguientes características:
* Cada row contiene la misma cantidad de campos
* Los campos se separan con un pipe |
* Se deben poder leer correctamente los caracteres especiales que estén presentes en los campos actuales del archivo. 
* El encoding del archivo final debe ser UTF-8 (datos_de_santander.tsv es un archivo UTF-16LE)

R: El ejercicio planteado para Python se encuentra resuelto en el archivo normalizar.py
