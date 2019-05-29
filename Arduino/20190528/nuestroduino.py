# -*- coding: utf-8 -*-
"""
Created on Tue May 28 18:58:19 2019

@author: realm
"""

import lantz.ino as ino

class nuestroIno(ino.INODriver):
    
    light = ino.BoolFeat() 
    #// desde pyton puedo crear un prog que le manda un 
    #// comando al arduino y le puedo consultar el estado del arguidno. Qué hace el 
    #// LIGHT lo tengo que programar yo.
    


li = nuestroIno.light

print(li)
