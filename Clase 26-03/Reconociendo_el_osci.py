import numpy as np
import visa  
import matplotlib.pyplot as plt
from clase_osciloscopio import Osciloscopio 


rm = visa.ResourceManager()
rm.list_resources() 
print (rm.list_resources())

inst = rm.open_resource('USB0::0x0699::0x0363::C065089::INSTR')
print(inst.query("*IDN?"))

dirTek = 'USB0::0x0699::0x0363::C065089::INSTR'

osci = Osciloscopio(dirTek) 

osci.setTiempo(2.5E-6)

osci.setCanal(1, 0.02) 

osci.getCanal(1)
n = 1


Data = np.zeros((n,2, 2500))
for i in range(n):
    
    Data[i, : , :] = osci.getVentana(1)
    
    plt.plot(Data[i,0], Data[i,1])

    
print(Data)     
type(Data)
np.shape(Data)

plt.show()
