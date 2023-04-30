
from spike2py.trial import TrialInfo, Trial
from tqdm import tqdm
import os
import time
from spik2py_reflex_plugin import utlis
import pickle
import matplotlib.pyplot as plt
import mpld3
from mpld3 import plugins

import scipy
import matplotlib.pyplot as plt
import numpy as np
import math
import pickle

from dataclasses import dataclass
from spik2py_reflex_plugin import compute_outcome_measures,graphgenerator
from spik2py_reflex_plugin.helper_functions import signal_cleaning, trains_extraction
from spik2py_reflex_plugin import utlis


@dataclass
class SinglePulse:
    name:str
    waveform: list
    startindex:int
    endindex:int
    relativeonset:int
    onset:float
    peak_to_peak: float
    area: float
    rms:float
    intensity:float
    triggerindex:int

@dataclass
class PairedPulse:
    name:str
    waveform:list
    waveform1: list
    waveform2:list
    startindex1:int
    endindex1:int
    startindex2:int
    endindex2:int
    trigger1index:int
    trigger2index:int
    relativeonset1:int
    
    onset1:float
    relativeonset2:int
    onset2:float
    peak_to_peak1: float
    peak_to_peak2:float
    area1: float
    area2:float
    rms1:float
    rms2:float
    intensity:float
    triggerindex:int
    peak_to_peak_ratio:float
    area_ratio:float

@dataclass
class SingleTransPulse:
    name:str
    waveform: list
    startindex:int
    endindex:int
    relativeonset:int
    onset:float
    peak_to_peak: float
    area: float
    rms:float
    intensity:float
    triggerindex:int
    

def extract_evoked_responses(parseddata:TrialInfo,triggerchannel:any,filename:str,isparsesingle:bool,isparsepaired:bool,isparsetrans:bool,userstarttime:int,userendtime:int,khz_frq:int,_window_pair:any,_window_single:any,_window_single_trains:any,graphdisplaysettings:any,data_file_path:str,img_path:str):
    #do main stuff 
   



    #store it as tuple where [(1,single_pulse),([1,2],paired_pulse),(1,carrier_frequency),(1,single_tran_fq),([1,2],paried_tran_fq)
    """
    The function "clearfirstpass" removes kilohertz triggers from a list of uncleaned triggers and
    returns a cleaned list.

    :param triggeruncleaned: A list of trigger times (in seconds) that may contain kilohertz noise
    :return: The function `clearfirstpass` is being called with the argument `triggeruncleaned`, which
    is a list of trigger times. The function cleans out all kilohertz triggers and returns a cleaned
    list of trigger times. The length of the cleaned list is printed. Therefore, the output is the
    length of the cleaned list of trigger times.
    """

    import numpy as np
    
    arr = np.array(triggerchannel)
  
    triggeruncleaned=signal_cleaning.extract_user_window(arr, userstarttime,userendtime)
    
  
    triggercleaned= signal_cleaning.remove_khz(triggeruncleaned,khz_frq) 

    

    # The above code is parsing a list of trigger values and identifying different types of triggers such
    # as single pulse, paired pulse, and train of pulses. It does this by checking the time differences
    # between adjacent trigger values and comparing them to predefined thresholds for each type of
    # trigger. The code then stores the identified triggers in separate lists and prints them at the end.
    
    parsedtrigger, trainlist= signal_cleaning.classify_triggers(triggercleaned)
   
    #index of trigger cleaned
    #because
    #get lsit of times where given intensity is stable for 3 seconds and only get the last 2 seconds

    # The above code is calculating the first derivative of a signal (intensity) and then identifying
    # stable regions in the signal where the derivative is within a certain threshold (0.2). It does this
    # by iterating through the derivative values and checking if they are within the threshold. If they
    # are, it adds the index, time, and intensity value to a list called "startstable". If the derivative
    # value is outside the threshold, it checks if there are any values in "startstable". If there are, it
    # marks the end of the stable region and adds the start and end indices, times

    intensity=parseddata.Stim.values
    intensitytime=parseddata.Stim.times
    duration=2
    stable= trains_extraction.extract_stable_trains_period(intensity,intensitytime,duration)
    # The above code is filtering out a stable list based on a specified time period and appending the
    # filtered items to a new list called finaltrainlist. It then extracts the start and end times, as
    # well as the intensity, from each item in finaltrainlist and appends them to a new list called
    # traintime. Finally, it appends each time interval to a list called parsedtrigger in the format of
    # ("single_trains_freq", triggercleaned[i]).
    traintime=trains_extraction.traintime(trainlist,stable,triggercleaned)
   


    #append to triggerclean
    for x in traintime:
        for i in range(x[0],x[1]):

            parsedtrigger.append(("single_trains_freq", triggercleaned[i]))

    
   

###################
#now we have the parsed trigger of every pusle, now we are ready to parse it 
###################









   
    def parsesingle(x,pre_target_window_ms=_window_single[0],post_target_window_ms=_window_single[1],mode="single"):
        import numpy as np
        if isparsesingle==False and (mode=="single"):
            return
        
        

        target = x[1]
        
        left = target - pre_target_window_ms / 1000
        right = post_target_window_ms / 1000 + target
        times = parseddata.Fdi.times

        start_index = np.searchsorted(times, left)
        trigger_index = np.searchsorted(times, target)
        end_index = np.searchsorted(times, right)

        intensity_index = np.searchsorted(parseddata.Stim.times, target)

        # find artifact start time
        skip_artifact_start_time = parseddata.Fdi.times[trigger_index] + 0.005
        artifact_start_index = np.searchsorted(times[trigger_index:end_index], skip_artifact_start_time) + trigger_index
        artifact_end_index = np.searchsorted(times[trigger_index:end_index], skip_artifact_start_time + 0.09) + trigger_index

        # compute baseline SD and average
        tkeo_array = utlis.TEOCONVERT(parseddata.Fdi.values)
        baseline_values = tkeo_array[artifact_start_index:artifact_end_index]
        baseline_sd = np.std(np.abs(baseline_values))
        baseline_avg = np.mean(np.abs(baseline_values))
        
        peak_to_peak, area=compute_outcome_measures.compute_peak2peak_area(parseddata.Fdi.values[artifact_start_index:end_index])

        # compute peak-to-peak and area
       
        # find onset time
        if mode =="single":
            onset_index = compute_outcome_measures.findonset(tkeo_array[trigger_index:end_index], baseline_sd, baseline_avg, artifact_start_index - trigger_index)
        elif mode=="double":
            baseline_values = parseddata.Fdi.values[artifact_start_index:artifact_end_index]
            baseline_sd = np.std(np.abs(baseline_values))
            baseline_avg = np.mean(np.abs(baseline_values))
            onset_index = compute_outcome_measures.findonset(parseddata.Fdi.values[trigger_index:end_index], baseline_sd, baseline_avg, artifact_start_index - trigger_index)
        else:

            onset_index = compute_outcome_measures.findonset(tkeo_array[trigger_index:end_index], baseline_sd, baseline_avg, artifact_start_index - trigger_index)

        if onset_index is not None:
            onset_time = parseddata.Fdi.times[onset_index + trigger_index]
            relative_time = onset_time - parseddata.Fdi.times[trigger_index]
        else:
            onset_time = None
            relative_time = None

        # create SinglePulse object
        data = SinglePulse(
            "singlepulse",
            parseddata.Fdi.values[start_index:end_index],
            start_index,
            end_index,
            relative_time,
            onset_time,
            peak_to_peak,
            area,
            0,
            parseddata.Stim.values[intensity_index],
            trigger_index
        )

        return data



    import numpy as np



  
        
     
    
    def parsepaired(x,pre=_window_pair[0],post=_window_pair[1]):
    
        import numpy as np
        if isparsepaired==False:
            return
        
    
        target1 = x[1]
        print(x)
        target2=x[2]
        
        FDI = parseddata.Fdi.values
        time = parseddata.Fdi.times
        left = target1 - 200 / 1000
        right = 60 / 1000 + target2
        startindex = np.searchsorted(time, left)
        endindex = np.searchsorted(time, right)

    
        firstpulse=parsesingle([0,target1],pre,post,"double")
        secondpulse=parsesingle([0,target2],pre,post,"double")
        print(f"this is {firstpulse}")
        print(target1)
        arearatio=firstpulse.area/secondpulse.area
        p2pratio=firstpulse.peak_to_peak/secondpulse.peak_to_peak
        #pretarget will be 0.02s ~15ms 
        #post target  will be ~40ms 
       
        
        data = PairedPulse(
            "pairedpulse",
            FDI[startindex:endindex],
            firstpulse.waveform,
            secondpulse.waveform,
            firstpulse.startindex,
            firstpulse.endindex,
            secondpulse.startindex,
            secondpulse.endindex,
            firstpulse.triggerindex,
            secondpulse.triggerindex,
            firstpulse.relativeonset,
            firstpulse.onset,
            secondpulse.relativeonset,
            secondpulse.onset,
            firstpulse.peak_to_peak,
            secondpulse.peak_to_peak,
            firstpulse.area,
            secondpulse.area,
            0,
            0,
            firstpulse.intensity,
            firstpulse.triggerindex,
            p2pratio,
            arearatio
        )

        
        
        return data




    def parsetrans(x,pre=_window_single_trains[0],post=_window_single_trains[1]):
        import numpy as np
        if isparsetrans==False:
            return
        
        target = x[1]
        pulse=parsesingle([0,target],pre,post,"trains")
      
        
      
        times = parseddata.Fdi.times
       
        data = SingleTransPulse(
        "single_trans_pulse",
        pulse.waveform,
        pulse.startindex,
        pulse.endindex,
        pulse.relativeonset,
        pulse.onset,
        pulse.peak_to_peak,
        pulse.area,
        0,
        pulse.intensity,
        pulse.triggerindex
    )

        
        return data
    



    lookup_table = {
        "single": parsesingle,
        "paired_pulse": parsepaired,
        "single_trains_freq": parsetrans

    }



###so now I need to get the master onset ansd the master reuslt for plotting 
#need to seperate the logic for plotting and the main  output
#mainoutput is graphs and pickled bot the for loop to 
    ##now in have to actually read it and extract it
    checktrigger=[]
    for x in parsedtrigger:

        for i in range(len(x)):
            if i==0:
                continue
            else:
                checktrigger.append(x[i])

    masterresult=[]
    masteronset=[]
    pickledtarget=[]
    for x in tqdm(parsedtrigger):
        result=lookup_table[x[0]](x)
        
        
        
        if result==None:
            continue
        pickledtarget.append(result)
        if result.name=="pairedpulse":
            masterresult.extend([(result.startindex1,result.endindex1),(result.startindex2,result.endindex2)])
        else:
            masterresult.append((result.startindex,result.endindex))
        
        
        
        if result.name=="pairedpulse":
            if result.onset1==-1 or result.onset2==-1:
                pass
            else:
                masteronset.extend([result.onset1,result.onset2])
        else:
            if result.onset==-1:
                pass
            else:
                masteronset.append(result.onset)
    
    print(pickledtarget)
    ##need to organise the data, group intensity name 
   
 
    
    

    #do something with the pickledtarget 
    print(parsedtrigger)
 

        

   

    print("Now there should a folder in the directory where you are running your script called extracted reflexs data, and the picked data should be in there!")
   


    import numpy as np

    x = intensitytime
    

    ##plot it out man
    #x1 will be FDI times and values and then
    #also want the event cahnnels
    xx1=parseddata.Fdi.times
    yy1=parseddata.Fdi.values
    print(masterresult)

    #need to generate another file for grouped results...
    #for each protocol 

    ##get the grouped averaghe measure 
    graphgenerator.generate_individual_graph(triggercleaned, triggeruncleaned, checktrigger, xx1, yy1, parseddata, masterresult, masteronset, userstarttime, userendtime, img_path,pickledtarget,filename,graphdisplaysettings["single"][0],graphdisplaysettings["single"][1],graphdisplaysettings["double"][0],graphdisplaysettings["double"][1])
    time_elapsed_single=(_window_single[1]+_window_single[0])/1000
    print(time_elapsed_single)
    time_elapsed_double=(_window_pair[1]+_window_pair[0])/1000
    time_elapsed_train=(_window_single_trains[1]+_window_single_trains[0])/1000
    groupedmeasure=graphgenerator.generate_grouped_avg_graph_pickled(pickledtarget,img_path,time_elapsed_single,time_elapsed_double,time_elapsed_train)

    #utility need to load in function to organise the data for indivisual to group all of them together 
    pickledtarget=utlis.Group_Individual_Pulses(pickledtarget)

    with open(f"{data_file_path}.pkl", "wb") as f:
        # Write the pickled data to the file
        pickle.dump({"individual":pickledtarget,"grouped":groupedmeasure}, f)
    
    # Close the file
    f.close()

