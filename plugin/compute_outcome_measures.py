 
from spike2py.trial import TrialInfo, Trial
from tqdm import tqdm

import scipy
import matplotlib.pyplot as plt
import numpy as np
import  pywt

from dataclasses import dataclass

def _calculate_waveform_stats(waveform, start, end,triggerindex,times,baselinesd,baselineavg):
        
        data_for_stats = waveform[start:end]
        peak_to_peak = np.ptp(data_for_stats)
        dx = 0.1  # Spacing of integration points along axis of x
        area = scipy.integrate.simpson(abs(data_for_stats), dx=dx)
        #onsettime= calculateonset(waveform,triggerindex,start,end)
        #baselinesd= np.std([abs(num) for num in waveform[start:triggerindex]])
        #baselineavg=np.average([abs(num) for num in waveform[start:triggerindex]])
        
        onsetindex = findonset(waveform[triggerindex:end],baselinesd,baselineavg)
        #onsetindex=wavelet_onset_detection(np.array(waveform[triggerindex+20:end]))
        try:
            if onsetindex==None:
                onsettime=None
            else:
                onsettime=times[onsetindex+triggerindex]
               
        except:
            pass

        
        return peak_to_peak, area,onsettime
 

def plot(signal):
    wavelet = 'db4'  # Choose a wavelet
    level = 5# Choose a decomposition level
    coeffs = pywt.wavedec(signal, wavelet, level=level)
    print(coeffs)
    reconstructed_signal = pywt.waverec(coeffs[:level], wavelet)
    # Plot the different levels of the decomposition
    fig, axs = plt.subplots(2, 1, figsize=(10, 6))
    axs[0].plot(signal)
    axs[0].set_title("Original Signal")
    axs[1].plot(reconstructed_signal)
    axs[1].set_title(f"{level}-Level Reconstructed Signal")
    plt.tight_layout()
   

def findonset(evokedspan,baselinesdnew,baselineavg):
    onset=0
    
    for i, x in enumerate(evokedspan):
        terminate=False
        print(f"length{len(evokedspan)}")
        print(i)
        if abs(x)-baselineavg > 2* baselinesdnew :
            
            
            for p in range(5):
                if len(evokedspan)-i<5:
                    break
                elif abs(evokedspan[i + p])-baselineavg < 2 * baselinesdnew:
                    terminate=True
                    break
            

                onset = i
            
            if terminate==True:
                continue
            else:


                return onset

        else:
            continue


def wavelet_onset_detection(signal, wavelet='sym4', level=4, threshold=3):
    ###this is not working yet 
    # Decompose signal into wavelet coefficients
    coeff = pywt.wavedec(signal, wavelet, mode="smooth",level=3)
    # Calculate a threshold for each level of the wavelet decomposition
    thresholds = [threshold*np.nanmedian(np.abs(c)) for c in coeff]
    # Set coefficients below the threshold to zero
    coeff[1:] = (pywt.threshold(i, value=t, mode='soft') for i, t in zip(coeff[1:], thresholds[1:]))
    # Reconstruct the signal using the modified coefficients
    reconstructed_signal = pywt.waverec(coeff, wavelet, mode='smooth')
    threshold = threshold*np.nanmedian(np.abs(signal))/0.6745
    onset = np.argmax(np.abs(reconstructed_signal) > threshold)
    # Calculate the onset as the point where the reconstructed signal first exceeds a threshold
    
    fig, axs = plt.subplots(2, 1, figsize=(10, 6))
    axs[0].plot(signal)
    
    axs[0].set_title("Original Signal")
    axs[1].plot(reconstructed_signal)
    
    axs[1].set_title(f"{level}-Level Reconstructed Signal")
    #can i find the peak and then go to the left to find the point where thr value is increasing again
    plt.tight_layout()
    plt.close()
    
    
    
    
    return onset