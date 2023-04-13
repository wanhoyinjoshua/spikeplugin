
from spike2py.trial import TrialInfo, Trial
from tqdm import tqdm
import os

import pickle

import scipy
import matplotlib.pyplot as plt
import numpy as np
import math
import pickle
from dataclasses import dataclass
from plugin import compute_outcome_measures

@dataclass
class SinglePulse:
    name:str
    waveform: list
    startindex:int
    endindex:int
    onset:float
    peak_to_peak: float
    area: float
    rms:float

@dataclass
class PairedPulse:
    name:str
    entirewaveform:list
    waveform1: list
    waveform2:list
    startindex1:int
    endindex1:int
    startindex2:int
    endindex2:int
    trigger1index:int
    trigger2index:int
    onset1:float
    onset2:float
    peak_to_peak1: float
    peak_to_peak2:float
    area1: float
    area2:float
    rms1:float
    rms2:float

@dataclass
class SingleTransPulse:
    name:str
    waveform: list
    startindex:int
    endindex:int
    onset:float
    peak_to_peak: float
    area: float
    rms:float
    

def extract_evoked_responses(parseddata:TrialInfo,filename:str,isparsesingle:bool,isparsepaired:bool,isparsetrans:bool):
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
    triggeruncleaned= parseddata.Ds8.times
    triggercleaned=[]
    times=parseddata.Fdi.times
    i=0

    def clearfirstpass(triggeruncleaned):
        print("cleaning khz ...")
        i = 0
        triggercleaned = []
        while tqdm(i < len(triggeruncleaned)):
            
            # clean out all kilihertz first
            carrier_frq = 10
            # units s
            per_s = 1 / (carrier_frq * 1000) + 0.00005
            try:
                rightdiff = triggeruncleaned[i + 1] - triggeruncleaned[i]
                if rightdiff < per_s:
                    
                    triggercleaned.append(triggeruncleaned[i])
                    i += carrier_frq
                    continue
            except:
                pass
            i += 1
        if len(triggercleaned)==0:
            return triggeruncleaned
        else:
            return triggercleaned
    triggercleaned= clearfirstpass(triggeruncleaned)

    i=0

    # The above code is parsing a list of trigger values and identifying different types of triggers such
    # as single pulse, paired pulse, and train of pulses. It does this by checking the time differences
    # between adjacent trigger values and comparing them to predefined thresholds for each type of
    # trigger. The code then stores the identified triggers in separate lists and prints them at the end.
    startdouble=[]
    parsedtrigger=[]
    starttrain=[]
    istrains=False
    trainlist=[]
    while i < len(triggercleaned):

        x=triggercleaned[i]
        paired_pulse_isi = 50 / 1000 + 0.01
        train_frq = 20 + 5
        per_s_train = 1 / train_frq

        if i == 0 or i == len(triggercleaned) - 1:


            if i==0:
                rightdiff = triggercleaned[i + 1] - x
                rightdiff5 = triggercleaned[i + 4] - x
                rightdiff2 = triggercleaned[i + 2] - triggercleaned[i + 1]
                if rightdiff > 1 and rightdiff > paired_pulse_isi:
                    # is single pusle
                  
                    parsedtrigger.append(("single",triggercleaned[i]))
                elif rightdiff < paired_pulse_isi and rightdiff2 > paired_pulse_isi:
                    
                    startdouble.append(triggercleaned[i])
                elif rightdiff5 / 5 < per_s_train:
                    
                    starttrain.append(i)
                    starttrain.append(triggercleaned[i])
            elif i == len(triggercleaned) - 1:
                leftdiff5 = x - triggercleaned[i - 4]
                leftdiff2 = triggercleaned[i - 1] - triggercleaned[i - 2]
                leftdiff = x - triggercleaned[i - 1]
                print(triggercleaned[i])
                if leftdiff > 1 and leftdiff > paired_pulse_isi:
                    # is single pusle
                    
                    parsedtrigger.append(("single", triggercleaned[i]))
                elif leftdiff < paired_pulse_isi and leftdiff2 > paired_pulse_isi:
                   
                   
                    if len(startdouble)==1:
                        #push
                        parsedtrigger.append(("paired_pulse",startdouble[0],triggercleaned[i]))
                        startdouble=[]



                elif leftdiff5 / 5 < per_s_train :
                    
                    trainlist.append((starttrain[0],starttrain[1],i,triggercleaned[i]))
                    starttrain=[]

                    pass


            i+=1
            continue

        try:
            rightdiff = triggercleaned[i + 1] - x
            rightdiff5 = triggercleaned[i + 4] - x
            rightdiff2=  triggercleaned[i +2] - triggercleaned[i +1]
            leftdiff5= x- triggercleaned[i -4]
            leftdiff2= triggercleaned[i -1] - triggercleaned[i -2]
            leftdiff = x - triggercleaned[i - 1]
        except:
            i += 1
            continue
        if (rightdiff > 1 and rightdiff > paired_pulse_isi) and (leftdiff > 1 and leftdiff > paired_pulse_isi):
            # is single pusle
           

            parsedtrigger.append(("single", triggercleaned[i]))
        elif rightdiff<paired_pulse_isi and leftdiff>paired_pulse_isi and rightdiff2>paired_pulse_isi:
            
            startdouble.append(triggercleaned[i])
        elif rightdiff>paired_pulse_isi and leftdiff<paired_pulse_isi and leftdiff2>paired_pulse_isi:
            
            if len(startdouble) == 1:
                # push
                parsedtrigger.append(("paired_pulse", startdouble[0], triggercleaned[i]))
                startdouble = []
        elif rightdiff5 / 5 < per_s_train and leftdiff> per_s_train:
          
            starttrain.append(i)
            starttrain.append(triggercleaned[i])


        elif leftdiff5/5< per_s_train and rightdiff> per_s_train:
           

            trainlist.append((starttrain[0], starttrain[1], i, triggercleaned[i]))
            starttrain = []
            pass

        i+=1

  
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
    intenindex=0

    firstderivative = [intensity[i+1]-intensity[i] if i+1<len(intensity) else 0 for i in range(len(intensity))]


    jj=0
    filteredintensity=[]
    stable=[]
    startstable=[]
    endstable=0
    print("taking derivaative...")
    while jj <len(firstderivative) :

        #this is the acceptable change ( threshold 0.2)
        if (firstderivative[jj]<0.2 and firstderivative[jj]>-0.2 ):

            startstable.extend([jj, intensitytime[jj], intensity[jj]])
            

        else:
            if len(startstable)>0:
                endstable=jj
                stable.extend([(startstable[0], startstable[1], endstable-1, intensitytime[endstable-1], startstable[2])])
                
                startstable=[];
                endstable=0
             
            else:
                pass



        jj += 1


    for x in stable.copy() :
        if intensitytime[x[2]]-intensitytime[x[0]]>=3:
           pass
        else:
            
            stable.remove(x)
    
    # The above code is filtering out a stable list based on a specified time period and appending the
    # filtered items to a new list called finaltrainlist. It then extracts the start and end times, as
    # well as the intensity, from each item in finaltrainlist and appends them to a new list called
    # traintime. Finally, it appends each time interval to a list called parsedtrigger in the format of
    # ("single_trains_freq", triggercleaned[i]).
    finaltrainlist=[]
    ##now filiter out the stable list to peroid specified.
    for x in trainlist.copy():
        starttargettime= x[1]
        endtargettime=x[3]
        for y in stable:
            if y[1]>starttargettime and y[3]<endtargettime:
                finaltrainlist.append(y)
            else:
                pass



    traintime=[]
    for train in finaltrainlist:
        #return index from cleanedtriggerlist
        #do the seconds  here trim the first second here
        start= train[1]
        end=train[3]
        intensity=train[4]
        startindex=[]
        endindex=[]
        for i , x in enumerate(triggercleaned):
            #this is adjusting how many seconds to trim ( this s trimming last 1 second)
            if x>=start+2.5 and len(startindex)==0:
                startindex.append(i)
            if x>=end and len(endindex)==0:
                endindex.append(i)
        traintime.append((startindex[0],endindex[0],intensity))
        startindex = []
        endindex = []


    #append to triggerclean
    for x in traintime:
        for i in range(x[0],x[1]):

            parsedtrigger.append(("single_trains_freq", triggercleaned[i]))

    def findonset(evokedspan,baselinesdnew,baselineavg):
        onset=0
        
        for i, x in enumerate(evokedspan):
            terminate=False
 
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


        """
        The function parses trigger events and extracts relevant data from the parsed data based on the type
        of trigger event.
        
        :param x: The input parameter for the functions `parsesingle`, `parsepaired`, and `parsetrans`. It
        is a list containing the type of event ("single", "paired_pulse", or "single_trains_freq") and one
        or more trigger times
        :return: The code returns a plot with event markers for triggers and stimulus, as well as shaded
        regions indicating the extracted spans of interest. It also prints out the extracted spans and onset
        times for each trigger type.
        """


    def parsesingle(x):
        import numpy as np
        if isparsesingle==False:
            return
    
        target=x[1]
        left=target-200/1000

        right=100/1000+target

        time=parseddata.Fdi.times
    
    
        def condition(element):
            return element >=left
        def condition2(element):
            return element >=right
        def condition3(element):
            return element >=target
        triggerindex=next((i for i, elem in enumerate(time) if condition3(elem)), None)
        startindex= next((i for i, elem in enumerate(time) if condition(elem)), None)
        
        #slice the array to make it faster.
        sliced_array = time[startindex:]
        
        endindex=next((i for i, elem in enumerate(sliced_array) if condition2(elem)), None)
        baselinesd= np.std([abs(num) for num in parseddata.Fdi.values[startindex:triggerindex]])
        baselineavg=np.average([abs(num) for num in parseddata.Fdi.values[startindex:triggerindex]])
        peak_to_peak, area,onsettime=compute_outcome_measures._calculate_waveform_stats(parseddata.Fdi.values, startindex, endindex+startindex,triggerindex,parseddata.Fdi.times,baselinesd,baselineavg)

        data=SinglePulse("singlepulse",parseddata.Fdi.values[startindex:endindex+startindex],startindex,endindex+startindex,onsettime,peak_to_peak,area,0)



        return data

        #subsetit and then calculate shit






  
        name:str
        entirewaveform:list
        waveform1: list
        waveform2:list
        startindex1:int
        endindex1:int
        startindex2:int
        endindex2:int
        trigger1index:int
        trigger2index:int
        onset1:float
        onset2:float
        peak_to_peak1: float
        peak_to_peak2:float
        area1: float
        area2:float
        rms1:float
        rms2:float
    
    def parsepaired(x):

        import numpy as np
        if isparsepaired==False:
            return
    
        
     
        target1 = x[1]
        target2=x[2]
       

        left = target1 - 200 / 1000
        right = 60 / 1000 + target2
        subleft1=target1 - 5 / 1000
        subright1=40 / 1000 + target1
        subleft2=target2 - 5 / 1000
        subright2=40 / 1000 + target2

        time = parseddata.Fdi.times
        FDI = parseddata.Fdi.values
        startindex = []
        endindex = []
        extractedspan = []


        def condition(element):
            return element >= left

        def condition2(element):
            return element >= right
        def subcondition1left(element):
            return element >= subleft1
        def subcondition1right(element):
            return element >= subright1

        def subcondition2left(element):
            return element >= subleft2

        def subcondition2right(element):
            return element >= subright2
        def condition3(element):
            return element >=target1
        def condition6(element):
            return element >=target1
        def condition7(element):
            return element >=target2
        triggerindex1=next((i for i, elem in enumerate(time) if condition6(elem)), None)
        triggerindex2=next((i for i, elem in enumerate(time) if condition7(elem)), None)
        startindex = next((i for i, elem in enumerate(time) if condition(elem)), None)
        baselinesd= np.std([abs(num) for num in parseddata.Fdi.values[startindex:triggerindex1]])
        baselineavg=np.average([abs(num) for num in parseddata.Fdi.values[startindex:triggerindex1]])
        
        # slice the array to make it faster.
        sliced_array = time[startindex:]
  
        endindex = next((i for i, elem in enumerate(sliced_array) if condition2(elem)), None)

        subtargetarray=time[startindex:endindex+startindex]
 
        firststartindex=next((i for i, elem in enumerate(subtargetarray) if subcondition1left(elem)), None)
        firstendindex = next((i for i, elem in enumerate(subtargetarray) if subcondition1right(elem)), None)
        secondstartindex = next((i for i, elem in enumerate(subtargetarray) if subcondition2left(elem)), None)
        secondendindex = next((i for i, elem in enumerate(subtargetarray) if subcondition2right(elem)), None)
     
        baselinesd2=np.std([abs(num) for num in parseddata.Fdi.values[secondendindex+startindex:endindex+startindex]])
        baselineavg2=np.average([abs(num) for num in parseddata.Fdi.values[secondendindex+startindex:endindex+startindex]])
        
        peak_to_peak1, area1,onsettime1=compute_outcome_measures._calculate_waveform_stats(parseddata.Fdi.values, firststartindex+startindex, firstendindex+firststartindex+startindex,triggerindex1,parseddata.Fdi.times,baselinesd,baselineavg)
        peak_to_peak2, area2,onsettime2=compute_outcome_measures._calculate_waveform_stats(parseddata.Fdi.values, secondstartindex+startindex, secondendindex+secondstartindex+startindex,triggerindex2,parseddata.Fdi.times,baselinesd2,baselineavg2)
        
        data = PairedPulse("pairedpulse",FDI[startindex:endindex+startindex],FDI[firststartindex+startindex:firstendindex+startindex],FDI[secondstartindex+startindex:secondendindex+startindex],firststartindex+startindex,firstendindex+startindex,secondstartindex+startindex,secondendindex+startindex,triggerindex1,triggerindex2,onsettime1,onsettime2,peak_to_peak1,peak_to_peak2,area1,area2,0,0)
        
        
        return data




    def parsetrans(x):
        import numpy as np
        if isparsetrans==False:
            return
        
        

      
        target = x[1]
        left = target - 5 / 1000
        right = 25/ 1000 + target
        time = parseddata.Fdi.times
        emg = parseddata.Fdi.values
        startindex = []
        endindex = []
        extractedspan = []
     

        def condition(element):
            return element >= left

        def condition2(element):
            return element >= right
        def condition3(element):
            return element >=target
        triggerindex=next((i for i, elem in enumerate(time) if condition3(elem)), None)

        startindex = next((i for i, elem in enumerate(time) if condition(elem)), None)
        # slice the array to make it faster.
        sliced_array = time[startindex:]


        endindex = next((i for i, elem in enumerate(sliced_array) if condition2(elem)), None)
        baselinesd= np.std([abs(num) for num in parseddata.Fdi.values[startindex:triggerindex]])
        baselineavg=np.average([abs(num) for num in parseddata.Fdi.values[startindex:triggerindex]])
        peak_to_peak, area,onsettime=compute_outcome_measures._calculate_waveform_stats(parseddata.Fdi.values, startindex, endindex+startindex,triggerindex,parseddata.Fdi.times,baselinesd,baselineavg)
        
        data=SingleTransPulse("single_trans_pulse",parseddata.Fdi.values[startindex:endindex+startindex],startindex,endindex+startindex,onsettime,peak_to_peak,area,0)
        return data

    lookup_table = {
        "single": parsesingle,
        "paired_pulse": parsepaired,
        "single_trains_freq": parsetrans

    }




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
        print(result)
        
        
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
    
    
    directory = "extracted_reflexes_data"
    directory_path = os.path.join(os.getcwd(), directory)
    os.makedirs(directory_path, exist_ok=True)
    file_path = os.path.join(directory_path, filename)
    with open(f"{file_path}.pkl", "wb") as f:
        # Write the pickled data to the file
        pickle.dump(pickledtarget, f)
    
    # Close the file
    f.close()
    print("Now there should a folder in the directory where you are running your script called extracted reflexs data, and the picked data should be in there!")
    import matplotlib.pyplot as plt


    import numpy as np

    x = intensitytime
    y1 = firstderivative
    y2 = intensity

    ##plot it out man
    #x1 will be FDI times and values and then
    #also want the event cahnnels
    xx1=parseddata.Fdi.times
    yy1=parseddata.Fdi.values


    fig, (ax1, ax2,ax3,ax5,ax4,ax6) = plt.subplots(6, 1, sharex=True)
    ax1.eventplot(triggercleaned, orientation='horizontal', colors='g')
    ax2.eventplot(triggeruncleaned, orientation='horizontal', colors='r')
    ax3.eventplot(checktrigger, orientation='horizontal', colors='y')
    ax4.plot(xx1,yy1)
    ax5.plot(parseddata.Stim.times,parseddata.Stim.values)

    for x in masterresult:

        ax4.axvspan(parseddata.Fdi.times[x[0]], parseddata.Fdi.times[x[1]], alpha=0.2, color='gray')
    

    ax4.vlines(x=list(filter(lambda x: x is not None, masteronset)), ymin=0, ymax=len(x), colors='red', ls=':', lw=1, label='vline_single - full height')

    plt.show()

    

