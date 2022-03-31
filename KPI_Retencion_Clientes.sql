------------------------------------------------- KPI RETENCIÓN DE CLIENTES ---------------------------------------------------------------

;WITH Sesiones_Consecutivas as (			        ----------- Filtramos los Usuarios que poseen Actividad con Sesiones durante 2 días Consecutivos
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
					WHERE EVENT_ID in (1, 2)		----------- Filtramos los Usuarios con Sesiones Extensas. Para ello tomamos el tiempo de cada
					GROUP BY USER_ID, SESSION_ID	----------- Sesión como la diferencia entre el tiempo de Login con el tiempo de Logout registrado
													----------- Además utilizamos el mismo particionado para obtener la Cantidad de Sesiones
					),
	Diferente_Login as(								----------- Filtramos los Usuarios con actividad de sesión diferente al Login
					SELECT DISTINCT USER_ID, 
					COUNT(EVENT_ID) OVER (PARTITION BY SESSION_ID)as CANTIDAD 
					FROM Actividades_Usuarios  DL			
					),								----------- El valor CANTIDAD evidencia actividad diferente si supera el valor de 2(Login + Logout)
		   Totales as(
					SELECT USER_ID, MAX(USER_ID) AS Total_Usuarios
					FROM Usuarios							
					GROUP BY USER_ID				----------- Se agrega el valor máximo de usuarios en forma dinámica, no como parámetro estático
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
		

		--------------------------------- SOLUCION ALTERNATIVA AL KPI -------------------------------------


					--INTO #Filtrado_Final
					
--;WITH Resultado as(
--	 SELECT(SELECT COUNT(DISTINCT USER_ID) as Condiciones 	
--			FROM #Filtrado_Final) Usuarios_Condiciones,
--			(SELECT COUNT(USER_ID) as Totales
--			FROM Usuarios) Usuarios_Totales)
--	SELECT *,CONVERT(varchar(4),CONVERT(numeric(10,2),Usuarios_Condiciones*100.00/Usuarios_Totales))+'%' as Porcentaje_Usuarios
--	FROM Resultado
--	DROP TABLE #Filtrado_Final   

					
		----------------- las sentencias comentadas aquí proponen como solución alternativa obtener el mismo resultado esperado, pero recurriendo
		----------------- al recurso de tabla temporal '#Filtrado' para almacenar el resultado deputado de la secuencia de CTE enlazados 
		----------------- y vincularlo con el número de usuarios. De esta manera se logra el mismo resultado

		