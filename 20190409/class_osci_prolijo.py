import numpy as np
import visa  
import matplotlib.pyplot as plt


rm = visa.ResourceManager()
misinstrumentos= rm.list_resources()

class Osciloscopio():
    
    
    def __init__(self,instru):
        self.instru= instru
        self.parametros = None
            
    def identidad(self):
        return self.instru.query("*IDN?")

        
    def get_unidades(self):
        return self.instru.query("MEASU?")
    
    def get_parametros(self):
        return self.instru.query_ascii_values('WFMPRE:XZE?;XIN?;YZE?;YMU?;YOFF?;', separator=';')

    def curva(self):
        self.instru.write('DAT:ENC RPB') 
        self.instru.write('DAT:WID 1')
        data = self.instru.query_binary_values('CURV?', 'B', is_big_endian=True)

        if self.parametros is None:
            self.parametros = self.get_parametros()

        xze, xin, yze, ymu, yoff = self.parametros

        tiempo = xze + np.arange(len(data)) * xin
        voltajes = (np.array(data) - 127) * ymu + yoff

        return tiempo, voltajes

    def set_timebase(self, seconds):
        self.instru.write('HOR:DEL:SCA {}'.format(seconds)) # set la escala de tiempo
               

    def set_scale(self, canal, volts):
        self.instru.write('CH{}:SCA {}'.format(canal,volts)) # set la escala vertical de tensión

    def get_scale_cursor_unidades(self):
        return self.instru.query('CURS:HBA:UNI?')



print(misinstrumentos)
osci = Osciloscopio(rm.open_resource(misinstrumentos[0])) #meter en el argumento el número de serie

print(osci.identidad())  # quién sos
osci.set_timebase(0.01) #setear escala de tiempo
osci.set_scale(1,1.0E0) # canal, amplitud máxima en volts
#print(osci.get_scale_cursor_unidades()) #Return vertical distance between horizontal bar cursors


tiempo, voltaje = osci.curva()
plt.plot(tiempo, voltaje)

        
        
        
        
        
        
"""
Si necesitamos los datos en ascii       
    def curva_ascii(self):
        self.instru.write('DAT:ENC ASCI') 
        self.instru.write('DAT:WID 1')
        data = self.instru.query_ascii_values('CURV?', container=np.array)
        if self.parametros is None:
            self.parametros = self.get_parametros()

        xze, xin, yze, ymu, yoff = self.parametros

        tiempo = xze + np.arange(len(data)) * xin

        return tiempo, data
"""