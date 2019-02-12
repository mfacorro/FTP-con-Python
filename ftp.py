#! /usr/bin/python

#ESPECIFICO CODIFICACION DEL CODIGO FUENTE
# - * -coding: utf - 8 - * -


#IMPORTO EL OBJETO FTP
import ftplib, os, sys

def imprimirInfo():
	print('+-----------------------------------------------------------------------------+')
	print('|*               Autor:  Martin Facorro <mfacorro@gco.com.ar>                *|')
	print('|*           Creado el:  Lunes 04 de Febrero de 2019                         *|')
	print('|*     Modificador por:  Martin Facorro <mfacorro@gco.com.ar>                *|')
	print('|* Ultima modificacion:  Lunes 11 de Febrero de 2019                         *|')
	print('+-----------------------------------------------------------------------------+')
	print()

def crearCarpetaLocal(pNombreDirectorio):
	if not(os.path.exists(pNombreDirectorio)):
		os.mkdir(pNombreDirectorio)


imprimirInfo()

print("Inicio de la aplicacion")

#DEFINO VARIABLES PARA LA CONEXION FTP
#UTILIZO NOTACION HUNGARA PARA EL NOMBRE DE LAS VARIABLES
#POR LO QUE LA PRIMERA LETRA INDICA EL TIPO DE VALOR
#EJEMPLO sHost --> STRING; iContadorArchivos --> INTEGER

sHost='##.##.##.##' #IP
sUser='usuario'
sPasswd='clave'

#METODO PARA RELACIONAR AL CONSTRUCTOR CON EL CUAL SE HARA LA CONEXION
try:
	ftp = ftplib.FTP(sHost)
	ftp.login(sUser, sPasswd)
except Exception, error:
	print(error)
else:

	print("Conexion al FTP establecida")

	#CAMBIO AL DIRECTORIO REMOTO  DONDE SE ESTAN LOS ARCHIVOS DE IMPRESORAS
	sDirFTP = ('/home/dirFTP/')
	ftp.cwd(sDirFTP)

	#CAMBIO AL DIRECTORIO LOCAL DONDE SE GUARDARAN LOS ARCHIVOS
	sDirectorioLocal = ('/home/dirLOCAL/')
	os.chdir(sDirectorioLocal)
				
	#CREO DOS LISTAS VACIAS
	listDirectorios = []
	listArchivos = []

	#LLENO LA LISTA CON LO QUE DEVUELVE EL la <funcion> DIR DEL OBJETO ftp
	ftp.dir(listDirectorios.append)	

	#CREO UNA LISTA, EN DONDE DECLARO LAS EXTENSIONES QUE NO QUIERO LISTAR
	#DE ESTA MANERA SOLO ME MUESTRA LOS DIRECTORIOS CONTENIDOS EN /home/etr/etrans/afip
	listExtensionesOmitidasEnListadoDir = ['gz','zip','rar','tar','bz2','xz',]

	#CADA LINEA ES GUARDA EN sLineas
	for sLineas in listDirectorios:
		
		#EN EL IF SE VERIFICA LA EXTENSION DE LOS ARCHIVOS
		if sLineas.split('.')[-1] not in listExtensionesOmitidasEnListadoDir:
			
			#OBTENGO EL NOMBRE DE LOS DIRECTORIOS QUE QUIERO RECORRER
			crearCarpetaLocal(sLineas[-6:]) #CREO DIRECTORIO LOCAL
			os.chdir(sLineas[-6:]) #         ENTRO AL DIRECTORIO LOCAL
			ftp.cwd(sLineas[-6:]) #          CAMBIO AL DIRECTORIO APUNTADO EN EL FTP
			ftp.dir(listArchivos.append) #   LISTO TODOS LOS ARCHIVOS EN EL FTP

			for sArchivo in listArchivos:
				print('   Descargando : ' + os.getcwd() + str(sArchivo[-34:])) #IMPRIMO DIRECTORIO ACTUAL (LOCAL)
				oArchivoFTP = open(sArchivo[-34:],"wb") # ABRO EL ARCHIVO REMOTO
				ftp.retrbinary("RETR " +  sArchivo[-34:], oArchivoFTP.write) # GUARDO EL ARCHIVO EN DIREC. LOCAL
				oArchivoFTP.close() #CIERRO EL ARCHIVO LOCAL

		os.chdir(sDirectorioLocal) # VUELVO AL DIRECTORIO LOCAL
		ftp.cwd(sDirFTP) # VUELVO AL DIRECTORIO FTP
		listArchivos = [] # VACIO LA LISTA DE ARCHIVOS
	
	
	ftp.close() # CIERRO CONEXION FTP


# FIN DE ARCHIVO

