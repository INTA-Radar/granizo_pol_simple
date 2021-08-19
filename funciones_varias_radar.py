# lista de funciones auxiliares para el trabajo
# POWERED BY HUAYRATORO 

def AlturaHaz(radar,sweep):

	# FUNCION PARA CALCULAR LA ALTURA DE UN PPI CONSTANTE
	
	# radar : UN .VOL LEIDO CON EL AUXILIAR DE LECTURA DE PYART
	# sweep : LA ELEVACION QUE SE QUIERA    

	import numpy as np
	ranges = radar.range['data']
	elevation = radar.fixed_angle['data'][sweep]
	radar_height = radar.altitude['data']
	Re = 6371.0 * 1000.0
	p_r = 4.0 * Re / 3.0

	z = radar_height + (ranges ** 2 + p_r ** 2 + 2.0 * ranges * p_r *
		                np.sin(elevation * np.pi / 180.0)) ** 0.5 - p_r

	return z


def get_lonlat(x, y):

	# 	ES UNA FUNCION PARA CONVERTIR UNA GRILLA CARTESIANA EN UNA LAT/LON CON PYPROJ
	# 	x, y  :  SE INGRESAN LAS COORDENADAS CARTESIANAS  
	# 	rad_lon, rad_lat  :  No olvidarse las coord del radar
	
	from pyproj import Proj
	
	p = Proj(proj='aeqd', ellps='WGS84', lon_0 = -60, lat_0 = -31)

	return p(x,y,inverse=True)

def federer(radar, hcero) :

	# esta funcion calcula la probabilidad de que en un pixel del área exita granizo mediante
	# la resta entre la altura de la Z45 y la Hcero grados de un sondeo o reanaisis
	# se ingresa numpy.ndarray y la altura de la isoterma
	# devuelve un masked array que tiene las probabilidades para cada pixel
	# con 1 - 10 (desde 10% - 100% prob de presencia)
	# utiliza la funcion de alturas, que se llama aux.AlturaHaz
	
	import numpy as np
						 
	dif = radar - hcero

	# en funcion de las diferencias se elabora una escala de probabilidades de acuerdo a Foote/Federer
	# prob	10
	prob_10 = (dif >= 1800) & (dif < 1970) 
	prob_10 = prob_10.astype(int)
	# prob	20
	prob_20 = (dif >= 1970) & (dif < 2170) 
	prob_20 = prob_20.astype(int)
	prob_20[prob_20==1]=2
	# prob	30
	prob_30 = (dif >= 2170) & (dif < 2400) 
	prob_30 = prob_30.astype(int)
	prob_30[prob_30==1]=3
	# prob	40
	prob_40 = (dif >= 2400) & (dif < 2700) 
	prob_40 = prob_40.astype(int)
	prob_40[prob_40==1]=4
	# prob	50
	prob_50 = (dif >= 2700) & (dif < 3070) 
	prob_50 = prob_50.astype(int)
	prob_50[prob_50==1]=5
	# prob	60
	prob_60 = (dif >= 3070) & (dif < 3550) 
	prob_60 = prob_60.astype(int)
	prob_60[prob_60==1]=6
	# prob	70
	prob_70 = (dif >= 3550) & (dif < 4200) 
	prob_70 = prob_70.astype(int)
	prob_70[prob_70==1]=7
	# prob	80
	prob_80 = (dif >= 4200) & (dif < 5000) 
	prob_80 = prob_80.astype(int)
	prob_80[prob_80==1]=8
	# prob	90
	prob_90 = (dif >= 5000) & (dif < 5800) 
	prob_90 = prob_90.astype(int)
	prob_90[prob_90==1]=9
	# prob	100
	prob_100 = (dif >= 5800) 
	prob_100 = prob_100.astype(int)
	prob_100[prob_100==1]=10

	mascara = prob_10 + prob_20 + prob_30 + prob_40 + prob_50 + prob_60 + prob_70 + prob_80 + prob_90 + prob_100
	
	return(mascara)

def max_dbz(ref) :

	## una funcion que con solo ingresarle un archivo .vol devuelve un numpy.ndarray con
	## los valores mas altos de la Z45 para un pixel determinado
	
	#########
	import funciones_varias_radar as aux
	import numpy as np
	
	sweep = 0
	ref_ele=ref.extract_sweeps([sweep])
	alturas = aux.AlturaHaz(ref, sweep)	
		# extraigo la reflectividad
	ZH = ref_ele.fields['reflectivity']['data']
	mask = (ZH >= 42) & (ZH < 52) 
	mask = mask.astype(int)
	alturas = np.array(alturas)
	alturas_0 = np.tile(alturas, (ZH.shape[0],1))
	alturas_0[np.where(mask != 1)] = 'NaN'
	#alturas_0 = alturas_0[0:350,:]
	#########
	sweep = 1
	ref_ele=ref.extract_sweeps([sweep])
	alturas = aux.AlturaHaz(ref, sweep)	
		# extraigo la reflectividad
	ZH = ref_ele.fields['reflectivity']['data']
	mask = (ZH >= 42) & (ZH < 52) 
	mask = mask.astype(int)
	alturas = np.array(alturas)
	alturas_1 = np.tile(alturas, (ZH.shape[0],1))
	alturas_1[np.where(mask != 1)] = 'NaN'
	#alturas_1 = alturas_1[0:350,:]
	#########
	sweep = 2
	ref_ele=ref.extract_sweeps([sweep])
	alturas = aux.AlturaHaz(ref, sweep)	
		# extraigo la reflectividad
	ZH = ref_ele.fields['reflectivity']['data']
	mask = (ZH >= 42) & (ZH < 52) 
	mask = mask.astype(int)
	alturas = np.array(alturas)
	alturas_2 = np.tile(alturas, (ZH.shape[0],1))
	alturas_2[np.where(mask != 1)] = 'NaN'
	#alturas_2 = alturas_2[0:350,:]
	#########
	sweep = 3
	ref_ele=ref.extract_sweeps([sweep])
	alturas = aux.AlturaHaz(ref, sweep)	
		# extraigo la reflectividad
	ZH = ref_ele.fields['reflectivity']['data']
	mask = (ZH >= 42) & (ZH < 52) 
	mask = mask.astype(int)
	alturas = np.array(alturas)
	alturas_3 = np.tile(alturas, (ZH.shape[0],1))
	alturas_3[np.where(mask != 1)] = 'NaN'
	#alturas_3 = alturas_3[0:350,:]
	#########
	sweep = 4
	ref_ele=ref.extract_sweeps([sweep])
	alturas = aux.AlturaHaz(ref, sweep)	
		# extraigo la reflectividad
	ZH = ref_ele.fields['reflectivity']['data']
	mask = (ZH >= 42) & (ZH < 52) 
	mask = mask.astype(int)
	alturas = np.array(alturas)
	alturas_4 = np.tile(alturas, (ZH.shape[0],1))
	alturas_4[np.where(mask != 1)] = 'NaN'
	#alturas_4 = alturas_4[0:350,:]
	#########
	sweep = 5
	ref_ele=ref.extract_sweeps([sweep])
	alturas = aux.AlturaHaz(ref, sweep)	
		# extraigo la reflectividad
	ZH = ref_ele.fields['reflectivity']['data']
	mask = (ZH >= 42) & (ZH < 52) 
	mask = mask.astype(int)
	alturas = np.array(alturas)
	alturas_5 = np.tile(alturas, (ZH.shape[0],1))
	alturas_5[np.where(mask != 1)] = 'NaN'
	#alturas_5 = alturas_5[0:350,:]
	#########
	sweep = 6
	ref_ele=ref.extract_sweeps([sweep])
	alturas = aux.AlturaHaz(ref, sweep)	
		# extraigo la reflectividad
	ZH = ref_ele.fields['reflectivity']['data']
	mask = (ZH >= 42) & (ZH < 52) 
	mask = mask.astype(int)
	alturas = np.array(alturas)
	alturas_6 = np.tile(alturas, (ZH.shape[0],1))
	alturas_6[np.where(mask != 1)] = 'NaN'
	#alturas_6 = alturas_6[0:350,:]
	#########
	sweep = 7
	ref_ele=ref.extract_sweeps([sweep])
	alturas = aux.AlturaHaz(ref, sweep)	
		# extraigo la reflectividad
	ZH = ref_ele.fields['reflectivity']['data']
	mask = (ZH >= 42) & (ZH < 52) 
	mask = mask.astype(int)
	alturas = np.array(alturas)
	alturas_7 = np.tile(alturas, (ZH.shape[0],1))
	alturas_7[np.where(mask != 1)] = 'NaN'
	#alturas_7 = alturas_7[0:350,:]
	#########
	sweep = 8
	ref_ele=ref.extract_sweeps([sweep])
	alturas = aux.AlturaHaz(ref, sweep)	
		# extraigo la reflectividad
	ZH = ref_ele.fields['reflectivity']['data']
	mask = (ZH >= 42) & (ZH < 52) 
	mask = mask.astype(int)
	alturas = np.array(alturas)
	alturas_8 = np.tile(alturas, (ZH.shape[0],1))
	alturas_8[np.where(mask != 1)] = 'NaN'
	#alturas_8 = alturas_8[0:350,:]
	#########
	sweep = 9
	ref_ele=ref.extract_sweeps([sweep])
	alturas = aux.AlturaHaz(ref, sweep)	
		# extraigo la reflectividad
	ZH = ref_ele.fields['reflectivity']['data']
	mask = (ZH >= 42) & (ZH < 52) 
	mask = mask.astype(int)
	alturas = np.array(alturas)
	alturas_9 = np.tile(alturas, (ZH.shape[0],1))
	alturas_9[np.where(mask != 1)] = 'NaN'
	#alturas_9 = alturas_9[0:350,:]
	#########
	sweep = 10
	ref_ele=ref.extract_sweeps([sweep])
	alturas = aux.AlturaHaz(ref, sweep)	
		# extraigo la reflectividad
	ZH = ref_ele.fields['reflectivity']['data']
	mask = (ZH >= 42) & (ZH < 52) 
	mask = mask.astype(int)
	alturas = np.array(alturas)
	alturas_10 = np.tile(alturas, (ZH.shape[0],1))
	alturas_10[np.where(mask != 1)] = 'NaN'
	#alturas_10 = alturas_10[0:350,:]
	#########
	sweep = 11
	ref_ele=ref.extract_sweeps([sweep])
	alturas = aux.AlturaHaz(ref, sweep)	
		# extraigo la reflectividad
	ZH = ref_ele.fields['reflectivity']['data']
	mask = (ZH >= 42) & (ZH < 52) 
	mask = mask.astype(int)
	alturas = np.array(alturas)
	alturas_11 = np.tile(alturas, (ZH.shape[0],1))
	alturas_11[np.where(mask != 1)] = 'NaN'
	#alturas_11 = alturas_11[0:350,:]
	#########

	prueba = np.empty([361, 480])

	for j in range(0, 361) :
		try :
			for i in range(0, 480) : 
			
				M = [alturas_0[j,i],alturas_1[j,i],alturas_2[j,i],alturas_3[j,i],alturas_4[j,i],alturas_5[j,i],alturas_6[j,i],alturas_7[j,i],alturas_8[j,i],alturas_9[j,i],alturas_10[j,i],alturas_11[j,i]]
				
				prueba[j, i] = np.nanmax(M)
		except IndexError :
			continue
		
			
	return prueba
	
def el_reloj_federer(array, hcero) :

	# esta funcion calcula la probabilidad de que en un pixel del área exita granizo mediante
	# la resta entre la altura de la Z45 y la Hcero grados de un sondeo o reanaisis
	# se ingresa numpy.ndarray y la altura de la isoterma
	# devuelve un masked array que tiene las probabilidades para cada pixel
	# con 1 - 10 (desde 10% - 100% prob de presencia)
	# utiliza la funcion de alturas, que se llama aux.AlturaHaz
	
	import numpy as np
						 
	dif = array - hcero

	# en funcion de las diferencias se elabora una escala de probabilidades de acuerdo a Foote/Federer
	# prob	10
	prob_10 = (dif >= 1800) & (dif < 1900) 
	prob_10 = prob_10.astype(int)
	# prob	20
	prob_20 = (dif >= 1970) & (dif < 1980) 
	prob_20 = prob_20.astype(int)
	prob_20[prob_20==1]=2
	# prob	30
	prob_30 = (dif >= 2170) & (dif < 2180) 
	prob_30 = prob_30.astype(int)
	prob_30[prob_30==1]=3
	# prob	40
	prob_40 = (dif >= 2400) & (dif < 2410) 
	prob_40 = prob_40.astype(int)
	prob_40[prob_40==1]=4
	# prob	50
	prob_50 = (dif >= 2700) & (dif < 2800) 
	prob_50 = prob_50.astype(int)
	prob_50[prob_50==1]=5
	# prob	60
	prob_60 = (dif >= 3070) & (dif < 3170) 
	prob_60 = prob_60.astype(int)
	prob_60[prob_60==1]=6
	# prob	70
	prob_70 = (dif >= 3550) & (dif < 3650) 
	prob_70 = prob_70.astype(int)
	prob_70[prob_70==1]=7
	# prob	80
	prob_80 = (dif >= 4200) & (dif < 4300) 
	prob_80 = prob_80.astype(int)
	prob_80[prob_80==1]=8
	# prob	90
	prob_90 = (dif >= 5000) & (dif < 5100) 
	prob_90 = prob_90.astype(int)
	prob_90[prob_90==1]=9
	# prob	100
	prob_100 = (dif >= 5800) 
	prob_100 = prob_100.astype(int)
	prob_100[prob_100==1]=10

	mascara = prob_10 + prob_20 + prob_30 + prob_40 + prob_50 + prob_60 + prob_70 + prob_80 + prob_90 + prob_100
	
	return(mascara)
	
def cuartiles(array, hcero) :

	# esta funcion calcula la probabilidad de que en un pixel del área exita granizo mediante
	# la resta entre la altura de la Z45 y la Hcero grados de un sondeo o reanaisis
	# se ingresa numpy.ndarray y la altura de la isoterma
	# devuelve un masked array que tiene las probabilidades para cada pixel
	# con 1 - 10 (desde 10% - 100% prob de presencia)
	# utiliza la funcion de alturas, que se llama aux.AlturaHaz
	
	import numpy as np
						 
	dif = array - hcero

	# en funcion de las diferencias se elabora una escala de probabilidades de acuerdo a Foote/Federer
	# prob	10
	prob_25 = (dif >= 1619) & (dif < 3653) 
	prob_25 = prob_25.astype(int)
	# prob	20
	prob_50 = (dif >= 3653) & (dif < 6206) 
	prob_50 = prob_50.astype(int)
	prob_50[prob_50==1]=2
	# prob	30
	prob_75 = (dif >= 6206) & (dif < 8329) 
	prob_75 = prob_75.astype(int)
	prob_75[prob_75==1]=3
	# prob	40
	prob_100 = (dif >= 8329)  
	prob_100 = prob_100.astype(int)
	prob_100[prob_100==1]=4
	# prob	50

	mascara = prob_25 + prob_50 + prob_75 + prob_100 
	
	return(mascara)

def percentiles(array, hcero) :

	# esta funcion calcula la probabilidad de que en un pixel del área exita granizo mediante
	# la resta entre la altura de la Z45 y la Hcero grados de un sondeo o reanaisis
	# se ingresa numpy.ndarray y la altura de la isoterma
	# devuelve un masked array que tiene las probabilidades para cada pixel
	# con 1 - 10 (desde 10% - 100% prob de presencia)
	# utiliza la funcion de alturas, que se llama aux.AlturaHaz
	
	import numpy as np
						 
	dif = array - hcero

	# en funcion de las diferencias se elabora una escala de probabilidades de acuerdo a Foote/Federer
	# prob	10
	prob_10 = (dif >= 239) & (dif < 1275) 
	prob_10 = prob_10.astype(int)
	# prob	20
	prob_20 = (dif >= 1275) & (dif < 1807) 
	prob_20 = prob_20.astype(int)
	prob_20[prob_20==1]=2
	# prob	30
	prob_30 = (dif >= 1807) & (dif < 2742) 
	prob_30 = prob_30.astype(int)
	prob_30[prob_30==1]=3
	# prob	40
	prob_40 = (dif >= 2742) & (dif < 3653) 
	prob_40 = prob_40.astype(int)
	prob_40[prob_40==1]=4
	# prob	50
	prob_50 = (dif >= 3653) & (dif < 4358) 
	prob_50 = prob_50.astype(int)
	prob_50[prob_50==1]=5
	# prob	60
	prob_60 = (dif >= 4358) & (dif < 5774) 
	prob_60 = prob_60.astype(int)
	prob_60[prob_60==1]=6
	# prob	70
	prob_70 = (dif >= 5774) & (dif < 6409) 
	prob_70 = prob_70.astype(int)
	prob_70[prob_70==1]=7
	# prob	80
	prob_80 = (dif >= 6409) & (dif < 7485) 
	prob_80 = prob_80.astype(int)
	prob_80[prob_80==1]=8
	# prob	90
	prob_90 = (dif >= 7485) & (dif < 8329) 
	prob_90 = prob_90.astype(int)
	prob_90[prob_90==1]=9
	# prob	100
	prob_100 = (dif >= 8329) 
	prob_100 = prob_100.astype(int)
	prob_100[prob_100==1]=10

	mascara = prob_10 + prob_20 + prob_30 + prob_40 + prob_50 + prob_60 + prob_70 + prob_80 + prob_90 + prob_100
	
	return(mascara)	
