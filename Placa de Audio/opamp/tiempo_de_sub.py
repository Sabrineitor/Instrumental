#por las, pongo el codigo que usamos para ver el tiepo de subida y bajada del opamp
# OJO: la señal se la mandamos con un gen porque a la compu no le da el tiempo

import pyaudio
import mathy 
from lantz import MessageBasedDriver, Feat, ureg
import matplotlib.pyplot as plt
from lantz.core import mfeats
import time
import numpy
from lantz import Action

numero = 'C108011'


class Oscilo(MessageBasedDriver):
    MANUFACTURER_ID = '0x0699'
    MODEL_CODE = '0x0363'

    @Feat(read_once=True)
    def i_osciloscopio(self):
        return self.query('*IDN?')

    set_query = MessageBasedDriver.write

    @Feat(limits=(1, 2))
    def datasource(self):
        """ Retrieves the data source from which data is going to be taken.
            TDS1002B has 2 channels
        """
        return self.query('DAT:SOU?')

    @datasource.setter
    def datasource(self, value):
        """ Sets the data source for the acquisition of data.
        """
        self.write('DAT:SOU CH{}'.format(value))

    bt_osciloscopio = mfeats.QuantityFeat('HOR:MAIN:SCA?', 'HOR:SCA {}', units='s', limits=(0.00001, 1000000))

    @Feat(units='Hz')
    def get_frec(self):
        return self.query('MEASU:MEAS{}:VAL?'.format(2))

    @Action()
    def acquire_parameters(self):
        """ Acquire parameters of the osciloscope.
            It is intended for adjusting the values obtained in acquire_curve
        """
        values = 'XZE?;XIN?;PT_OF?;YZE?;YMU?;YOF?;'
        answer = self.query('WFMP:{}'.format(values))
        parameters = {}
        for v, j in zip(values.split('?;'), answer.split(';')):
            parameters[v] = float(j)
        return parameters

    @Action()
    def data_setup(self):
        """ Sets the way data is going to be encoded for sending.
        """
        self.write('DAT:ENC ASCI')
        self.write('DAT:WID 1')  # ASCII is the least efficient way, but
        # couldn't make the binary mode to work

    @Action()
    def acquire_curve(self, start=1, stop=2500):
        """ Gets data from the oscilloscope. It accepts setting the start and
            stop points of the acquisition (by default the entire range).
        """
        self.data_setup()
        parameters = self.acquire_parameters()

        self.write('DAT:STAR {}'.format(start))
        self.write('DAT:STOP {}'.format(stop))
        data = self.query('CURV?')
        data = data.split(',')
        data = numpy.array(list(map(float, data)))
        voltaje = (data - parameters['YOF']) * parameters['YMU']+ parameters['YZE']
        tiempo = numpy.arange(len(data)) * parameters['XIN'] + parameters['XZE']
        return list(tiempo), list(voltaje)
        #return data

#el gene esta a 1khz y 1vpp

file = 'Out_tiemposubidada0.45'
file2 = 'In_tiemposubida0.45'
with Oscilo.via_usb(numero) as O:
    O.datasource = 2
    print(O.acquire_parameters())
    #y = O.acquire_curve()
    x, y = O.acquire_curve()
    x = numpy.array(x)
    y = numpy.array(y)
    data = numpy.array([x, y])
    data = data.T #estoy bastante segura que tiene que estar
    numpy.savetxt(file  +  '.txt', data, delimiter= " ")
    plt.figure(1)
    plt.plot(x,y)
    O.datasource = 1
    print(O.acquire_parameters())
    #y = O.acquire_curve()
    x1, y1 = O.acquire_curve()
    x1 = numpy.array(x1)
    y1 = numpy.array(y1)
    data1 = numpy.array([x1, y1])
    data1 = data1.T #estoy bastante segura que tiene que estar
    numpy.savetxt(file2 + '.txt', data1, delimiter= " ")
    plt.figure(2)
    plt.plot(x1,y1)

plt.show()
