#No se si no funciona porque esta mal el pid o porque estan mal los parametros. 


import lantz
from time import gmtime, strftime
from lantz.ino import INODriver, QuantityFeat, BoolFeat 
import numpy as np
import time 
import keyboard
import numpy as np

#Aca defino lo que voy a usar. Tengo como variable el angulo del arduino y la intensidad del sensor. 
class servo_sensor2(INODriver):       
    angulo = QuantityFeat('Angulo', setter = True)
    intensidad = QuantityFeat('Brillo', getter=True)
    tiempo = QuantityFeat('Tiempo', getter=True)

#defino las variables 
inicio = True
angulo_previo = 10 
angulo_actual = 15
valor = 1
#2.7 y ki 1 pareciera que va
# 3, 1 , 7 muy inestable 
kp =  0.001 #pareciera que da bien con 6
kd = 0.0007 #velocidad?
ki = 0.0005

tiempo_espera = 1

proporcional_pid = []
derivada_pid = []
integral_pid = []
inte = []
tiempo_pid = []
resultado_angulo = []

proporcional_pid.append(0)
proporcional_pid.append(0)
integral_pid.append(0)
integral_pid.append(0)
derivada_pid.append(0)
derivada_pid.append(0)

#para que queden todos del mismo tamañano


"""
#defino la funcion que nos dijo damian que hagamos por si la necesitamos 
def get_intensity(brillos):
	# brillos es dev.brillo
	resultado_sensor = 0
    for i in range(32): #promedio 32 veces para eliminar ruido. El 32 viene de 32 bits
    	resultado_sensor += brillos /32
    return resultado_sensor
"""
if __name__ == '__main__':
	with servo_sensor2.via_packfile('servo_sensor2.pack.yaml') as dev:
		#este while es para que no corte el programa 
		while valor ==1:
			#seteo las cosas iniciales  
			if inicio == True:
				print('ESTOY EMPEZANDO')
				integral=0
				errorPrevio=0

				#previo
				dev.angulo = angulo_previo
				intensidad_previa = float(dev.intensidad) #get_intensity(dev.brillo) falta time sleep
				tiempo_previo = 0
				tiempo_pid.append(tiempo_previo)
				inte.append(intensidad_previa)
				resultado_angulo.append(angulo_previo)
				#print('I1   ' + str(intensidad_previa))
				
				#ahora
				dev.angulo = angulo_actual
				intensidad_ahora = float(dev.intensidad)
				resultado_angulo.append(angulo_actual)
				inte.append(intensidad_ahora)
				tiempo_ahora =  float(dev.tiempo)
				tiempo_pid.append(tiempo_ahora)
				#print('I2    ' + str(intensidad_ahora))
				inicio = False

			#empieza el pid 
			dTiempo = tiempo_ahora - tiempo_previo
			dAngulo = angulo_actual - angulo_previo  #OJO porque esto no puede ser cero
			print('dt: ' +str(dTiempo))
			#esto no se si esta bien
			if dAngulo == 0:
				dAngulo = 1


			
			error = (float(intensidad_ahora) - float(intensidad_previa)) /(dAngulo) #esto es lo que queremos minimizar, que busque el maximo y que llegue a cero
			
			integral += error * dTiempo 
			derivada = (error - errorPrevio) /dTiempo

			angulo = kp*error + ki * integral + kd*derivada 
			print('angulo pid-----> ' + str(angulo))

		  	#para no pasarme de los limites del servo 
			if angulo > 180:
				angulo = 10
				inicio = True
			elif angulo < 0 :
				angulo = 10
				inicio = True
			else:
				print('-----Otro loop-----')

		  	# me muevo el resultado del pid y mido la intensidad
			dev.angulo = angulo
			intensidad_prov = float(dev.intensidad)
			tiempo_prov = float(dev.tiempo)
			#print('intesidad prov' + str(intensidad_prov))

			#no se si esta bien esto, creo que es hacer trampa. 
			#if intensidad_prov == intensidad_ahora:
			#	dev.angulo = 150

			# 2=1
			intensidad_previa = (intensidad_ahora)
			intensidad_ahora = (intensidad_prov) 
			
			tiempo_previo = tiempo_ahora
			tiempo_ahora = tiempo_prov

			angulo_previo = angulo_actual  
			angulo_actual =  angulo 


			errorPrevio = error


			print('                         ')
			#falta guardar intensidad
			tiempo_pid.append(tiempo_ahora)
			proporcional_pid.append(error)
			integral_pid.append(integral)
			derivada_pid.append(derivada)
			resultado_angulo.append(angulo)
			inte.append(intensidad_ahora)
			#print('termine pid')
			#print('intensidad_previa ', intensidad_previa)
			#print('intensidad ahora ', intensidad_ahora)

			#print(inte)
		    
			if keyboard.is_pressed('a'): # hay que apretar varias veces 
				with open('data_pid9.txt','w') as f:
				    lis=[tiempo_pid,proporcional_pid,derivada_pid,integral_pid,resultado_angulo,inte]
				    for x in zip(*lis):
				        f.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(*x))
				break
			if keyboard.is_pressed('n'):# apretando n (varias veces) renueva medicion desde cero
				inicio=True

			time.sleep(tiempo_espera)
