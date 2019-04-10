# ejmplo canónico de python. 
# supongamos que queremos poder agarrar muchas formas y con ellas calcular cosas

from math import pi

# observar que hay cosas que pueden repetirse, entonces uso la herencia. Algo que puedo hacer que varios puedan usar

class Forma: #esta es la clase padre

    def ratio(self):
        return self.area() / self.perimetro()

class Circulo(Forma): #acá círculo hereda propiedades de forma. Puede hacer derecho el ratio

    def __init__(self, radio):
        self.radio = radio

    def area(self):
        return pi * self.radio * self.radio
    
    def perimetro(self):
        return pi * 2 * self.radio



class Cuadrado(Forma):

    def _init_(self, lado):
        self.lado = lado
    def area(self):
        return self.lado * self.lado

    def permeter(self):
        return pi * 2 self.radio

# que tal si quiere calcular una métrica
    def ratio(self):
        return 4 * self.lado



cuad = Circulo(3)
print(cuad.area(), cuad.perimetro(), cuad.ratio())
#===================================================================================================
#===================================================================================================
#===================================================================================================
# ejemplo programación python del osciloscopio por HGrecco

import visa

rm = visa.ResourceManager()

class Instrumento:

    def idn(self):
        return self.inst.query('*IDN?') 


class OsciloscopioTDS1002b(Instrumento):

    def __init__(self, serialno):
        self.serialno = serialno   # así asigno al argumento el número de serie
        self.inst = rm.open_resource('USB0::nroMarca::modelo::{}::INSTR',format(serialno)) # constructor de la funcion, creo el inst
        self.parametros = None

    def set_timebase(self, seconds):
        self.inst.write('HOR:DEL:SCA {}'.format(seconds))


        

        return tiempo, voltajes

class GeneradorFunciones(Instrumento):
# 
    def __init__(self, serialno):
        self.serialno = serialno   # así asigno al argumento el número de serie
        self.inst = rm.open_resource('USB0::nroMarca::modelo::{}::INSTR',format(serialno))





osci = Osciloscopio() #meter en el argumento el número de serie
print(osci.idn()) # quién sos
osci.set_timebase() #setear escala de tiempo
osci.set_scale(10) # amplitud máxima
out = osci.get_channel(1)

gen = Generador() # meter en el argumento el número de serie
print(gen.idn())
gen.set_shape('sin')
gen.set_amplitude(5)
gen.set_frequency(15)