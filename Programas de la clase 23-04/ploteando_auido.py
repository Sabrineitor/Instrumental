"""
import matplotlib.pyplot as plt
import numpy as np
import wave
import sys


spf = wave.open('voice.wav','r')

#Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, 'Int16')
fs = spf.getframerate()

#If Stereo
if spf.getnchannels() == 2:
    print('Just mono files')
    sys.exit(0)


Time=np.linspace(0, len(signal)/fs, num=len(signal))

plt.figure(1)
plt.title('Signal Wave...')
plt.plot(Time,signal)
plt.show()
"""
import matplotlib.pyplot as plt
import numpy as np
import wave

file = 'probando_laseñaldelgen12.wav'

wav_file = wave.open(file,'r')

#Extract Raw Audio from Wav File
signal = wav_file.readframes(-1)
if wav_file.getsampwidth() == 1:
    signal = np.array(np.frombuffer(signal, dtype='UInt8')-128, dtype='Int8')
elif wav_file.getsampwidth() == 2:
    signal = np.frombuffer(signal, dtype='Int16')
else:
    raise RuntimeError("Unsupported sample width")

# http://schlameel.com/2017/06/09/interleaving-and-de-interleaving-data-with-python/
deinterleaved = [signal[idx::wav_file.getnchannels()] for idx in range(wav_file.getnchannels())]

#Get time from indices
fs = wav_file.getframerate()
Time=np.linspace(0, len(signal)/wav_file.getnchannels()/fs, num=len(signal)/wav_file.getnchannels())

#Plot
plt.figure(1)
plt.title('Signal Wave...')
for channel in deinterleaved:
    plt.plot(Time,channel)
plt.show()