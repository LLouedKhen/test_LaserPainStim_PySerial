#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 16 14:50:50 2019

@author: loued
"""
import fakeSerial1 as serial
import time
from random import randint
import numpy as np
from datetime import datetime

#El En receives stuff in code
#eg for laser pulse duration, code is x ms -1; so for 4 ms, it should be 3
#Then the code for energy is ix([0.5:0.25:2]== xJ; for instance 0.5 J == 1
#watch out for 0 indexing if in python
#Then the spot size is the the size in mm -4; so for 4 mm, it is 0. 

LaserFootPulse = 4; # ms not clear at all 
LaserFootSpotsize =4 ; # mm
LaserFootPulseCode = LaserFootPulse - 1;
LaserFootSpotsizeCode = LaserFootSpotsize - 4;
#  The following values are temporary, average  
high = 1.75
medium =  1.5
low = 1.25
thresh = 1

pain =[]
times = np.zeros([10,6])

ser = serial.Serial()  # open first serial port
print( ser.name )       # check which port was really used
ser.baudrate = 9600 #set baudrate to 9600 as in Manual p.47

startThis = input('Start laser (1/0)?')
if startThis == '1':
    print('\n Start connection...Switch to Serial NOW!')
    
    t0=time.time();
    #L111 means the laser is ON state
    ser.write(str([str(204).encode('utf-8') +str('L111').encode('utf-8') + str(185).encode('utf-8')]))
    print('\n Laser on...')
    t1=time.time() - t0

    #H111 means the diode is ON state
    ser.write(str([str(204).encode('utf-8') + str('H111').encode('utf-8')+ str(185).encode('utf-8')]))
    print('\n Diode on...')
    t2=time.time() - t0
    
    #O111 means the operate is ON state, that is the letter O, not zero
    ser.write(str([str(204).encode('utf-8') + str('O111').encode('utf-8')+ str(185).encode('utf-8')]))
    print('\n Operate on...')
    t3=time.time() - t0
    #all three checks must be on for system to fire$
        
for i in range(1,2):
    pain =int(input('How much pain would you like? '))
    print(pain)
    if pain == 4:
        LaserFootEnergy = high;
    elif pain == 3:
        LaserFootEnergy = medium;
    elif pain == 2:
        LaserFootEnergy = low;
    elif pain == 1:
        LaserFootEnergy = thresh;
    
    LaserFootEnergyCode = int((LaserFootEnergy/0.25)-1);
    
    if pain > 0:
     #C is to calibrate, followed by pulse parameter d (1ms * d +1), and e, energy (which is the c parameter of the P command, from 1 to 59)
        times[i,0] = time.time() 
        ser.write(str([str(204).encode('utf-8') + str('C').encode('utf-8') + str(LaserFootPulseCode).encode('utf-8') + str(LaserFootEnergyCode).encode('utf-8') + str(1).encode('utf-8') + str(185).encode('utf-8')]))
        print('\n Calibrating...')
        times[i,1] = time.time()
        time.sleep(7)
        #P, set parameters {abc}, pulse parameter (1ms * (a + 1)), energy parameter b, (0.25 * (b +1)), spot size c in mm (diameter)
        times[i,2] = time.time()
        ser.write(str([str(204).encode('utf-8') + str('P').encode('utf-8') + str(LaserFootPulseCode).encode('utf-8') + str(LaserFootEnergyCode).encode('utf-8') + str(LaserFootSpotsizeCode).encode('utf-8') + str(185).encode('utf-8')]))
        print('\n Set Parameters...')
        times[i,3] = time.time()
        print('Press the laser foot pedal NOW !!!!!!\n')
        times[i,4] = time.time()
        #Now G is the most relevant. It is th1e pain delivery
        print('\n FIRE.')
        ser.write(str([str(204).encode('utf-8') + str('G111').encode('utf-8')  + str(185).encode('utf-8')]))
        
        times[i,5] = time.time() 
        time.sleep(0.1)
        #ser.flush()
        print('Release Laser Foot Pedal NOW!\n');
        #ser.flush()
        time.sleep(6)
        
     #L000 means the laser is OFF state
    ser.write(str([str(204).encode('utf-8') +str('L000').encode('utf-8') + str(185).encode('utf-8')]))

    #H000 means the diode is OFF state
    ser.write(str([str(204).encode('utf-8') + str('H000').encode('utf-8')+ str(185).encode('utf-8')]))

    #O000 means the operate is OFF state, that is the letter O, not zero
    ser.write(str([str(204).encode('utf-8') + str('O000').encode('utf-8')+ str(185).encode('utf-8')]))


ser.close()