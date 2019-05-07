from lantz import MessageBasedDriver, Feat, ureg
from lantz.core import mfeats
#import time
import pyaudio
import wave
import numpy as np
from scipy.optimize import curve_fit
#import matplotlib.pyplot as plt



def Seno(t,A,B,W):
    return A * np.sin(t*W) + B

class Generador(MessageBasedDriver):
    
    MANUFACTURER_ID = '0x0699'
    MODEL_CODE = '0x0346'
    
    set_query = MessageBasedDriver.write
    
    @Feat(read_once=True)
    def i_generador(self):
        return self.query('*IDN?')
    
    f_generador = mfeats.QuantityFeat('SOUR1:FUNC:FREQ?', 'SOUR1:FREQ{}', units='hertz', limits=(1, 1E6)) #Get-Set Frecuencia

    a_generador = mfeats.QuantityFeat('SOUR1:VOLTage:AMPLitude?', 'SOUR1:VOLT:AMPLitude {}',units = 'volt') #Get-Set Amplitud
    
    
    
class Osciloscopio(MessageBasedDriver):
    
    @Feat(read_once=True)
    def i_osciloscopio(self):
        return self.query('*IDN?')
    
    bt_osciloscopio = mfeats.QuantityFeat('HOR:MAIN:SCA?','HOR:DEL:SCA {}',units = 's', limits = (0.01,100))
    
    @Feat(units = 'Hz')
    def get_frec(self):
        return self.query('MEASU:MEAS{}:VAL?'.format(2))
    
    @Feat(units = 'volts')
    def set_scale(self):
        self.write('CH1:SCA {}') #No sé si es así, preg desp!!!
    
    
Fs = [1000, 10000]    

A = 0.5

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 5
#WAVE_OUTPUT_FILENAME = 'SenalRecibida.wav'

Fenv = []
Fsal = []

for k in range(len(Fs)):
    
    with Generador.via_usb('C034165') as G:
        
        G.f_generador= Fs[k] * ureg.hertz 
        G.a_generador= A * ureg.volt
        
       
    Fenv.append(Fs[k])
    print('Hola')
    WAVE_OUTPUT_FILENAME = 'SenalRecibida.wav'
    print('Hola')
    p = pyaudio.PyAudio()
    print('Hola')
    stream = p.open(format=FORMAT,
                    channels=CHANNELS, 
                    rate=RATE, 
                    input=True, 
                    frames_per_buffer=CHUNK)

    print("Grabando...")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Se ha grabado el audio con exito")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    
#Ahora voy a sacar los parametros:

    file = 'SeñalRecibida.wav'

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
    deinterleaved = [signal[idx::wav_file.getnchannels()] for idx in range(wav_file.getnchannels())] #Creo que aca esta la información de todos los channels, voy a agarrar el primero, pero puede ser que este mal 

#Get time from indices
    fs = wav_file.getframerate()
    DominioAudio=np.linspace(0, len(signal)/wav_file.getnchannels()/fs, num=len(signal)/wav_file.getnchannels())    
    
    
#Voy a savcar los parametros de la señal recibida: 

    p0 = [A,Fs[i],0.]

    popt,pcov = curve_fit(Seno, DominioAudio, deinterleaved[1] , p0=p0, absolute_sigma=True, sigma= 0.002)
    perr = np.sqrt(np.diag(pcov))    
    
    Fsal.append(popt[1])    
    
    
    
    
    
    
    