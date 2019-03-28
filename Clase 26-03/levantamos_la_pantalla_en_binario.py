# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 18:17:37 2019

@author: Sabrina
"""

import numpy as np
import visa  
import matplotlib.pyplot as plt


rm = visa.ResourceManager()
rm.list_resources('?*') 
print(rm.list_resources())

misinstrumentos = rm.list_resources('?*') 

osci = rm.open_resource(misinstrumentos[0]) 
osci.write('DAT:ENC RPB') # Recordar que esto puede depender del instrumental usado y de su sintaxis
osci.write('DAT:WID 2') #determina cuantos bytes estamos seteando


xze, xin, yze, ymu, yoff = osci.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')
#xze offset
#xin intervalo horizontal de sampleo
#yze factor de conversion de la forma de onda 
#ymu factor de escala vertical 
#yoff offset vertical
print(xze, xin, yze, ymu, yoff)



#ahora me lo pasa en binario (depende de lo que este en datatype)
data = osci.query_binary_values('CURV?',datatype='b', container=np.array) #meter al final como entran y salen los datos
#cuando el osciloc lo da te lo da de adelante para atras o al reves 
#datatype hay que buscarlo en la tabla del struct del pyvisa
print(len(data))
tiempo = xze + np.arange(len(data)) * xin



plt.plot(tiempo, data )

plt.show()
"""
data = osci.query_ascii_values('CURV?', container=np.array)
print(len(data))

tiempo = xze + np.arange(len(data)) * xin

plt.plot(tiempo, data)
"""

