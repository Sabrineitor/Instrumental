"""""
Consultar: 
1) el for que hice abajo esta bien? siento que derrape 
2) como sigo con lo del sweep? Porque no entiendo como darle al osci cada frecuencia que agarro
3) la libreria de urge donde esta? porque no sé si volts esta bien
""""


from lantz import MessageBasedDriver, Feat, ureg
from lantz.core import mfeats
import numpy as np
import time

class Osc(MessageBasedDriver):
    MANUFACTURER_ID = '0x0699'
    MODEL_CODE = '0x0363'

    @Feat(read_once=True)
    def idn(self):
        return self.query('*IDN?')

    set_query = MessageBasedDriver.write
    timebase = mfeats.QuantityFeat('HOR:MAIN:SCA?', 'HOR:DEL:SCA {}', units='s', limits=(0.01, 100))

    @Feat(units='Hz')
    def frec(self):
        return self.query('MEASU:MEAS{}:VAL?'.format(2)) #Esto devuelve la frec HAY UN DOS PORQUE ES LA MED DOS

    #Para probar. Esto es teoria deberia poder settear el voltaje
    @Feat(units='Volts')
    def voltaje(self):
        return self.query('CH1:VOLts {}')

class Gen(MessageBasedDriver):
    MANUFACTURER_ID = '0x0699'
    MODEL_CODE = '0x0346'

    @Feat(read_once=True)
    def idn(self):
        return self.query('*IDN?')

    # frecuencia = mfeats.QuantityFeat('SOUR{1}:FUNC:FREQ?'.format(1),'SOUR{}:FREQ{}'.format(1,),units = 'Hz', limits = (1,1E6))
    set_query = MessageBasedDriver.write
    frec_gen = mfeats.QuantityFeat('SOUR1:FUNC:FREQ?', 'SOUR1:FREQ{}', units='Hz', limits=(1, 1E6))

    #Para probar: esto deberia poner la amplitud
    amplitud_gen = mfeats.QuantityFeat('SOUR1:VOLTage:LEVel:IMMediate:AMPLitude {}', 'SOUR1:VOLT:LEV:IMMediate:AMPLitude?',units = 'Volts')

    #Para probar. Copia del grupo 4. un sweep en frec
    def freq_sweep(self, freq_inicial, freq_final, step, stop=1, channel=1):
        # Hace un barrido de frecuencias desde freq_inicial hasta freq_final con un step.
        # Entre cada cambio de frecuencia dejamos 1 segundo de stop.
        frecuencias = np.arange(freq_inicial, freq_final, step)
        for elemento in frecuencias:
            self.write('SOUR{}:FREQ:FIX {}'.format(channel, elemento))
            time.sleep(stop)



# freq_inicial = 1000
# freq_final = 5000
# step = 1000




# with Gen.via_usb('C034166') as gene:
#     print(gene.idn)
#     gene.frecgen = 1000
#     Asi lo hace estilo swepp
#     gene.freq_sweep(freq_inicial, freq_final, step)

# with Osc.via_usb('C108011') as osci:
#     print(osci.idn)
#     print(osci.timebase)
#     # osci.timebase = 0.5 *ureg.seconds
#     #print(osci.frec)
# Para probar con el sweep:



#Esto es lo que quiero que haga el programa:
# Programa:
#
# -generar un array 1 10 100
#
# - en un loop:
#       -Setear generador a f1 y V1 y meter en vector las frec
#
#     -Setear Osci a partir de f1 y V1
#
#     - Lea la frec y la meto en vector

frec_array = np.arange(10,100, 20) #empieza en 10khz termina en 100 khz y el paso es de 20
voltaje_leido = []
for i in range(frec_array):
    with Gen.via_usb('C034166') as gene:
        gene.frecgen = frec_array[i] #asi seteo la frec que quiero
        gene.amplitud_gen = V1 #esto setea la amplitud del gen en V1 (la toma el osci despues creo)
        with Osc.via_usb('C108011') as osci:
            osci.voltaje = gene.amplitud_gen #ASI ESTA BIEN?
            osci.timebase = 5 * (1/gene.frec_gen) * ureg.seconds  #Esto toma 5 picos de la senal del generador 
            # y esta 1/.. porque asi es es la frec  
            voltaje_leido.append(osci.frec)
            #Lo que no me termina de quedar claro es que la señal del gen no se me vaya de la pantalla del osci !!!


