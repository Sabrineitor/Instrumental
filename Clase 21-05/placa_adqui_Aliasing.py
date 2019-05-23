#Usamos la placa Sensor Daq Vernier

import nidaqmx
import pyaudio
import math
import matplotlib.pyplot as plt
import time
import numpy


class ToneGenerator(object):

    def __init__(self, samplerate=44100, frames_per_buffer=4410):
        self.p = pyaudio.PyAudio()
        self.samplerate = samplerate
        self.frames_per_buffer = frames_per_buffer
        self.streamOpen = False

    def sinewave(self):
        if self.buffer_offset + self.frames_per_buffer - 1 > self.x_max:
            # We don't need a full buffer or audio so pad the end with 0's
            xs = numpy.arange(self.buffer_offset,
                              self.x_max)
            tmp = self.amplitude * numpy.sin(xs * self.omega)
            out = numpy.append(tmp,
                               numpy.zeros(self.frames_per_buffer - len(tmp)))
        else:
            xs = numpy.arange(self.buffer_offset,
                              self.buffer_offset + self.frames_per_buffer)
            out = self.amplitude * numpy.sin(xs * self.omega)
        self.buffer_offset += self.frames_per_buffer
        return out

    def callback(self, in_data, frame_count, time_info, status):
        if self.buffer_offset < self.x_max:
            data = self.sinewave().astype(numpy.float32)
            return (data.tostring(), pyaudio.paContinue)
        else:
            return (None, pyaudio.paComplete)

    def is_playing(self):
        if self.stream.is_active():
            return True
        else:
            if self.streamOpen:
                self.stream.stop_stream()
                self.stream.close()
                self.streamOpen = False
            return False

    def play(self, frequency, duration, amplitude):
        self.omega = float(frequency) * (math.pi * 2) / self.samplerate
        self.amplitude = amplitude
        self.buffer_offset = 0
        self.streamOpen = True
        self.x_max = math.ceil(self.samplerate * duration) - 1
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.samplerate,
                                  output=True,
                                  frames_per_buffer=self.frames_per_buffer,
                                  stream_callback=self.callback)


generator = ToneGenerator()

frequency_start = 1000  # Frequency to start the sweep from
frequency_end = 20000  # Frequency to end the sweep at
num_frequencies = 1 # Number of frequencies in the sweep
amplitude = 1.0  # Amplitude of the waveform
file = 'probando'
file2 = 'probando1'
step_duration = 1.0  # Time (seconds) to play at each step



vector_señal_voltaje = []
for frequency in numpy.logspace(math.log(frequency_start, 10),
                                math.log(frequency_end, 10),
                                num_frequencies):

    generator.play(frequency, step_duration, amplitude)
    #time.sleep(0.51)
    while generator.is_playing():
        print("estoy sonando" + str(frequency))
        with nidaqmx.Task() as task:
            task.ai_channels.add_ai_voltage_chan("Placa/AI0")  # analog input 0 = pin 11 (sin espacio)
            #task.ai_channels.add_ai_voltage_chan("Placa/AI1") #1 es pin 12
            vector_señal_voltaje.append(task.read())

            #print(task.read())
            #task.ai_channels.d
plt.plot()
