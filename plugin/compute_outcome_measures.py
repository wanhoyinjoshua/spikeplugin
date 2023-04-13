 
from spike2py.trial import TrialInfo, Trial
from tqdm import tqdm

import scipy
import matplotlib.pyplot as plt
import numpy as np

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
        try:
            if onsetindex==None:
                onsettime=None
            else:
                onsettime=times[onsetindex+triggerindex]
               
        except:
            pass

        
        return peak_to_peak, area,onsettime
 



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
