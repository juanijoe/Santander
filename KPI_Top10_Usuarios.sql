------------------------------------------------- KPI TOP 10 USUARIOS MAS LOGIN ULTIMO MES ------------------------------------------------

											----------- El siguiente Query nos permite obtener el listado de usuarios con mayor cantidad de logins
;WITH TOP10_Usuarios as(					----------- Durante el último mes calendario (30 últimos días desde la fecha) 
	   SELECT DISTINCT USER_ID,				
			COUNT(SESSION_ID) OVER (PARTITION BY USER_ID) as Cantidad_Login,
			MIN(EVENT_TIME) OVER (PARTITION BY USER_ID) as Primer_Login,
		    MAX(EVENT_TIME) OVER (PARTITION BY USER_ID) as Ultimo_Login
			FROM Primer_Sesion
			WHERE EXISTS (SELECT EVENT_TIME FROM Actividades_Usuarios WHERE EVENT_TIME<=GETDATE() AND EVENT_TIME>=DATEADD(day,-30,getdate()))
			)
	   SELECT DISTINCT TOP 10 U.USER_ID,Cantidad_Login,Primer_Login,Ultimo_Login,U.First_Name,U.Last_Name,U.Account_Number,U.Email 
	   FROM TOP10_Usuarios TP
	   INNER JOIN Usuarios U				----------- Uniendo el filtrado de la cantidad de logins en forma vincular con los datos de la tabla
	   ON U.USER_ID = TP.USER_ID		    ----------- Usuarios, podemos obtener la información buscada, restringiendo a los 10 usuarios que
	   ORDER BY Cantidad_Login DESC			----------- cumplen lo solicitado


	 