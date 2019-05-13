import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile as wf
import os
import subprocess
from tkinter import filedialog # tkinter package is to be able to open windows to interact w/user.
import tkinter as tk
import pyaudio
import wave


# select file to open
dirpath = os.getcwd() # get current directory
root = tk.Tk() 
root.filename = filedialog.askopenfilename(initialdir = dirpath,title = "Select file",filetypes = (("wave files","*.wav"),("all files","*.*")))
filename = root.filename

# read the wav file
rate, data = wf.read(filename)
print(filename)  #to check the right file has been open
#the sample rate is the number of bits of infomration recorded per second
print('rate = ' , rate)
print('data = ' , data)

#wav bit type the amount of information recorded in each bit often 8, 16 or 32 bit
data.dtype
#wav length
data.shape[0] / rate
#wav number of channels mono/stereo 
nbrchannels = data.shape[1]
#if stereo grab both channels
signal_1 = data[:,0] #left 
signal_2 = data[:,1] #right

# Plotting -----------------------------------------
fig2, (ax2, ax3) = plt.subplots(nrows=2, ncols=1) # two axes on figure
ax2.plot(signal_1)
ax3.plot(signal_2, 'm-')
ax2.set_title('Axis 2 title')
ax3.set_title('axis 3 title')
plt.show()
# ---------------------------------------------------
