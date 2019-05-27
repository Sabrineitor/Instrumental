#Usamos la placa Sensor Daq Vernier

import nidaqmx
from nidaqmx import stream_readers
import pyaudio
import math
import matplotlib.pyplot as plt
import time
import numpy as np




N = 100
data1 = np.linspace(0.0, 1.0, N)
#print(data)
rate = 20000

file = 'Daq14'
#creo la serie de tareas
with nidaqmx.Task() as task:
    task.ai_channels.add_ai_voltage_chan("Placa/AI0")  # analog input 0 = pin 11 (sin espacio)
    # task.ai_channels.add_ai_voltage_chan("Placa/AI1") #1 es pin 12
    #print(task.read())
    task.timing.cfg_samp_clk_timing(rate, samps_per_chan=N +24)
    #nidaqmx._task_modules.timing.Timing(task.in_stream).cfg_samp_clk_timing(rate) #,source=u'',active_edge= < Edge.RISING: 10280 >, sample_mode = < AcquisitionType.FINITE: 10178 >, samps_per_chan = 1000)
    stream_readers.AnalogSingleChannelReader(task.in_stream).read_many_sample(data = data1, number_of_samples_per_channel=N, timeout=10.0)

np.savetxt(file + '.txt', data1, delimiter= ";")
#print(data1)
plt.plot(data1)
plt.show()


'''
Esto es muy lento
vector_amplitud = []

n=50
i = 0
while i < n:

    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Placa/AI0")  # analog input 0 = pin 11 (sin espacio)
        # task.ai_channels.add_ai_voltage_chan("Placa/AI1") #1 es pin 12
        print(task.read())
        vector_amplitud.append(task.read())
    i = i+1
plt.plot(vector_amplitud)
plt.show()
'''


