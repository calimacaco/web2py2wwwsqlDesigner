#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 10/12/2014
archproc@author: Marco Antonio Castro
@organization: simplesoft.com ltda
@license:GLP v 2
@contact:soportesimplesoft@gmail.com
@version=1
@date=10/Dic/2014
@title=Convertir
@descripcion=Sube archivo echo en Web2py a www sql Desiner
'''

archentrada= open('db.py','r')
archsalida= open ('salida.xml','w')



archsalida.write('''<?xml version="1.0" encoding="utf-8" ?>
<!-- SQL XML created by WWW SQL Designer, http://code.google.com/p/wwwsqldesigner/ -->
<!-- Active URL: file:///home/marco/desarrollo/Tools%20paginas%20web/wwwsqldesigner-2.7/index.html -->
<sql>
<datatypes db="web2py">
	<group label="Numeric" color="rgb(238,238,170)">
		<type label="Integer" length="1" sql="integer" re="INTEGER" quote=""/>
		<type label="Double precision" length="1" sql="double" re="DOUBLE" quote=""/>
	</group>
	<group label="Character" color="rgb(255,200,200)">
		<type label="String" length="1" sql="string" quote="'"/>
		<type label="Text" length="1" sql="text" quote="'"/>
		<type label="BLOB" length="1" sql="blob" quote="'"/>
	</group>
	<group label="Date &amp; Time" color="rgb(200,255,200)">
		<type label="Time" length="0" sql="time" quote="'"/>
		<type label="Date" length="0" sql="date" quote="'"/>
		<type label="Datetime" length="0" sql="datetime" quote="'"/>
	</group>
	<group label="Miscellaneous" color="rgb(200,200,255)">
		<type label="Boolean" length="0" sql="boolean" quote=""/>
		<type label="Upload" length="0" sql="upload" quote=""/>
		<type label="Password" length="0" sql="password" quote=""/>
	</group>
</datatypes>
''')

camposactivo=False
x=10
y=10
for linea in archentrada.readlines():
	#archsalida.write('lectura' + linea)
	if linea.find('db.define_table')==0 and not camposactivo:
		linea=linea[17:linea.find('"',17)]
		salida= '<table x="%s" y="%s" name="%s">\n<row name="id" null="1" autoincrement="1">\n<datatype>integer</datatype>\n<default>NULL</default></row>\n' % (x,y,linea)
		archsalida.write(salida)
		x+=100
		y+=100
		if y>800:
			y=10
			
		camposactivo=True
	elif camposactivo:
		print linea.find('Field("')
		buscar=linea.find('Field("')
		if buscar <0:
			archsalida.write('<key type="PRIMARY" name="">\n<part>id</part>\n</key><comment></comment>\n</table>\n')
			camposactivo=False
		else:
			linea=linea[buscar + 7:]
			linea=linea.replace('"','')
			linea=linea.replace("'",'')

			buscar=linea.find(",")
			salida = '<row name="%s" null="1" autoincrement="0">\n' % (linea[:buscar])

			if linea.find('integer')>-1:
				salida += '<datatype>integer</datatype>\n<default>NULL</default>\n</row>\n'
			elif linea.find('string')>-1:
				salida += '<datatype>string</datatype>\n<default>NULL</default>\n</row>\n'
			elif linea.find('double')>-1:
				salida += '<datatype>double</datatype>\n<default>NULL</default>\n</row>\n'
			elif linea.find('upload')>-1:
				salida += '<datatype>upload</datatype>\n<default>NULL</default>\n</row>\n'
			elif linea.find('date')>-1:
				salida += '<datatype>date</datatype>\n<default>NULL</default>\n</row>\n'
			elif linea.find('datetime')>-1:
				salida += '<datatype>datetime</datatype>\n<default>NULL</default>\n</row>\n'
			else:
				buscar =linea.find('db.')
				if buscar>-1:
					linea=linea[buscar + 3 : linea.find(',',buscar)]
					salida += '<datatype>integer</datatype>\n<default>NULL</default><relation table="%s" row="id" />\n</row>\n' %(linea)

				else:
					salida += '<datatype>integer</datatype>\n<default>NULL</default>\n</row>\n'

			archsalida.write(salida)


archsalida.write('</table>\n</sql>\n')

archentrada.close()
archsalida.close()
