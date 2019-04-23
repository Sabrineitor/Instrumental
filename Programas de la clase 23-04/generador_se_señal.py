import math        #import needed modules
import numpy as np
import pyaudio     #sudo apt-get install python-pyaudio



#Le pasamos esta señal al osci
PyAudio = pyaudio.PyAudio     #initialize pyaudio

#See https://en.wikipedia.org/wiki/Bit_rate#Audio
BITRATE = 44100  #number of frames per second/frameset.

FREQUENCY = 10000     #Hz, waves per second, 261.63=C4-note.
LENGTH = 10     #seconds to play sound

if FREQUENCY > BITRATE:
    BITRATE = FREQUENCY+100

NUMBEROFFRAMES = int(BITRATE * LENGTH)
RESTFRAMES = NUMBEROFFRAMES % BITRATE #% es el resto son los frames donde no hace nda
WAVEDATA = ''

#generating wawes
for x in range(NUMBEROFFRAMES):
 WAVEDATA = WAVEDATA+chr(int(math.sin(x/((BITRATE/FREQUENCY)/math.pi))*127+128))

for x in range(RESTFRAMES):
 WAVEDATA = WAVEDATA+chr(128)

p = PyAudio()

array = np.arange(0,20,1)
for i in array:
    stream = p.open(format = p.get_format_from_width(1),
                channels = 1,
                rate = BITRATE,
                output = True)

    stream.write(WAVEDATA)
    stream.stop_stream()
    stream.close()

p.terminate()