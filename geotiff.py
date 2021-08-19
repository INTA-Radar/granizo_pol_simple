### SCRIPT PARA GUARDAR GEOTIFF CON LOS ALGORITMOS DE WITT, PERCENTILES Y CUARTILES DE LA POH ###
#
# PARA CORRER EL SCRIPT HAY QUE INDICARLE EL RADAR, LA ALTURA DE LA ISOTERMA DE CERO GRADOS Y EL NOMBRE DE LA CARPETA CON LOS .vol
# CORRER EN UN BASH CON > python geotiff.py radar iso_cero nom_carpeta 
# solo funciona para PER
# cambiar la url donde estan los vols (linea 37) !!!!
# tambien cambiar la ruta donde se guardan los geotiff
#
###
### REALIZADO POR EL GRUPO DE RADAR INTA-CASTELAR ###
import os
import matplotlib as mpl
from matplotlib import pyplot as plt
from matplotlib import colors
import numpy as np
import pyart
from pyart import aux_io
from pyart import graph
from os import listdir
import datetime
import pandas as pd  
from sys import argv
## se importan las librerias que deben estar en la misma carpeta ## 
import funciones_varias_radar as aux
from funciones_varias_radar import federer as fed
from funciones_varias_radar import percentiles as perc
from funciones_varias_radar import cuartiles as cuart
from funciones_varias_radar import max_dbz as max_dbz

#### INICIO ####

rad = 'PER'	# (solo funciona para PER)
iso = int(argv[1])	# isoterma cero
sit = argv[2]	# fecha

# url donde estan los vols
url = '/home/martin/Documentos/TRABAJO_RADAR/tiff/'+sit+'/vols/'+rad+'/'

# se ordenan los archivos por fecha
vols = listdir(url)
vols = sorted(vols)

# una vez cargados los archivos, se aplican los algoritmos

interruptor = 'on'

#### ALGORITMO DE WITT 

if interruptor == 'on' :	# si no se quiere computar un algoritmo se pone off aqui 

	for i in range(0,len(vols)) :	# len(vols)

		radar = pyart.aux_io.read_rainbow_wrl(url + vols[i])

		a = max_dbz(radar)
		mascara = fed(a, iso)
		
		shapes = np.array([radar.extract_sweeps([0]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([1]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([2]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([3]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([4]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([5]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([6]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([7]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([8]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([9]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([10]).fields['reflectivity']['data'].shape[0], radar.extract_sweeps([11]).fields['reflectivity']['data'].shape[0]])
		
		try :
			elevacion = np.where(shapes == 360)[0][0]
		except IndexError :
			print('NO HAY ELEVACIONES CON 360 AZIMUTS EN ' + vols[i] + ' SE SALTEA AL MISMO')
			continue
		try : 
			radar=radar.extract_sweeps([elevacion])
			radar.add_field_like('reflectivity','MASCARA', mascara)
		except ValueError : 
			print('NO HAY ELEVACIONES CON 360 AZIMUTS')
			continue

		time = radar.time['units'][13:]

		# con los limites 200 - 200 puedo graficar toda el area del centro de la figura
		# ya no queda ese circulo gigante con cero datos en el medio  
		
		grid = pyart.map.grid_from_radars(
		    (radar,) ,
		    grid_shape=(1, 500, 500),
		    grid_limits=((200, 200), (-253000.0, 253000.0), (-253000.0, 253000.0)),
		    fields = ['MASCARA'], gridding_algo = 'map_gates_to_grid')
		    
		pyart.io.write_grid_geotiff(grid, '/home/martin/Documentos/TRABAJO_RADAR/tiff/'+sit+'/tiff/ROGER/'+rad+'/'+time+'_fed_'+rad+'.tiff','MASCARA')

### ALGORITMO DE CUARTILES

if interruptor == 'on' :

	for i in range(0,len(vols)) :	# len(vols)

		radar = pyart.aux_io.read_rainbow_wrl(url + vols[i])

		a = max_dbz(radar)
		mascara = cuart(a, iso)
		
		shapes = np.array([radar.extract_sweeps([0]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([1]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([2]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([3]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([4]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([5]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([6]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([7]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([8]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([9]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([10]).fields['reflectivity']['data'].shape[0], radar.extract_sweeps([11]).fields['reflectivity']['data'].shape[0]])
		
		try :
			elevacion = np.where(shapes == 360)[0][0]
		except IndexError :
			print('NO HAY ELEVACIONES CON 360 AZIMUTS EN ' + vols[i] + ' SE SALTEA AL MISMO')
			continue
		try : 
			radar=radar.extract_sweeps([elevacion])
			radar.add_field_like('reflectivity','MASCARA', mascara)
		except ValueError : 
			print('NO HAY ELEVACIONES CON 360 AZIMUTS')
			continue

		time = radar.time['units'][13:]

		grid = pyart.map.grid_from_radars(
		    (radar,) ,
		    grid_shape=(1, 500, 500),
		    grid_limits=((200, 200), (-253000.0, 253000.0), (-253000.0, 253000.0)),
		    fields = ['MASCARA'], gridding_algo = 'map_gates_to_grid')
		    
		pyart.io.write_grid_geotiff(grid, '/home/martin/Documentos/TRABAJO_RADAR/tiff/'+sit+'/tiff/CUARTILES/'+rad+'/'+time+'_cuart_'+rad+'.tiff','MASCARA')

### ALGORITMO DE PERCENTILES

if interruptor == 'on' :

	for i in range(0,len(vols)) :	# len(vols)

		radar = pyart.aux_io.read_rainbow_wrl(url + vols[i])

		a = max_dbz(radar)
		mascara = perc(a, iso)
		
		shapes = np.array([radar.extract_sweeps([0]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([1]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([2]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([3]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([4]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([5]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([6]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([7]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([8]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([9]).fields['reflectivity']['data'].shape[0],radar.extract_sweeps([10]).fields['reflectivity']['data'].shape[0], radar.extract_sweeps([11]).fields['reflectivity']['data'].shape[0]])
		
		try :
			elevacion = np.where(shapes == 360)[0][0]
		except IndexError :
			print('NO HAY ELEVACIONES CON 360 AZIMUTS EN ' + vols[i] + ' SE SALTEA AL MISMO')
			continue
		try : 
			radar=radar.extract_sweeps([elevacion])
			radar.add_field_like('reflectivity','MASCARA', mascara)
		except ValueError : 
			print('NO HAY ELEVACIONES CON 360 AZIMUTS')
			continue

		time = radar.time['units'][13:]

		# con los limites 200 - 200 puedo graficar toda el area del centro de la figura
		# ya no queda ese circulo gigante con cero datos en el medio  
		
		grid = pyart.map.grid_from_radars(
		    (radar,) ,
		    grid_shape=(1, 500, 500),
		    grid_limits=((200, 200), (-253000.0, 253000.0), (-253000.0, 253000.0)),
		    fields = ['MASCARA'], gridding_algo = 'map_gates_to_grid')
		    
		#print(np.nanmax(grid.fields['MASCARA']['data']))
		#print(np.nanmin(grid.fields['MASCARA']['data']))

		#grid.add_field_like('reflectivity','MASCARA', mascara)
		pyart.io.write_grid_geotiff(grid, '/home/martin/Documentos/TRABAJO_RADAR/tiff/'+sit+'/tiff/PERCENTILES/'+rad+'/'+time+'_perc_'+rad+'.tiff','MASCARA')

  
