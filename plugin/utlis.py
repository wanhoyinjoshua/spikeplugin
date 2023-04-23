import numpy as np
import time

def TEOCONVERT(signal):
    signal=np.abs(signal)
    sorted_indices = np.argsort(signal)

# Get the last two indices (corresponding to the maximum values)
    max_indices = sorted_indices[-2:]
    print(max_indices)
    
    signal=signal+1
    # Get the maximum values from the array using the max_indices
    max_values = signal[max_indices]
   
    
    energy = np.power(signal[1:-1],100) - signal[:-2]*signal[2:]

# Zero-pad the energy signal to match the length of the input signal
    energy = np.concatenate(([0], energy, [0]))
    return energy

    
    #if max 2 signal in the array >1 the +1 if not let it be 

    
    
    