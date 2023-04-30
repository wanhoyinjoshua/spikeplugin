import numpy as np
import time
from itertools import groupby

def TEOCONVERT(signal):
    signal=np.abs(signal)
    sorted_indices = np.argsort(signal)

# Get the last two indices (corresponding to the maximum values)
    max_indices = sorted_indices[-2:]
    print(max_indices)
    
    signal=signal+1
    # Get the maximum values from the array using the max_indices
    max_values = signal[max_indices]
   
    
    energy = np.power(signal[1:-1],200) - signal[:-2]*signal[2:]

# Zero-pad the energy signal to match the length of the input signal
    energy = np.concatenate(([0], energy, [0]))
    return energy

    
    #if max 2 signal in the array >1 the +1 if not let it be 

def Group_Individual_Pulses(pickledtarget):
    #now is a lsit of obejct, need to return a object with fields intensity, pulses (list )
    ###{intensity:"10",pulses:[dataclass,....]}
    
    ###
    print(pickledtarget)
    individualpulses= pickledtarget
    for i in individualpulses:
        i.intensity=round(i.intensity)
    individualpulses.sort(key=lambda x: x.intensity)
    groups = []
    for key, group in groupby(individualpulses, key=lambda x: x.intensity):
        groups.append(list(group))
    pickledtarget=groups
    return pickledtarget




    
    