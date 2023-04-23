
from spike2py.trial import TrialInfo, Trial
from tqdm import tqdm
import os
import time
from plugin import utlis
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
from plugin import compute_outcome_measures,graphgenerator


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
    onset1:float
    onset2:float
    peak_to_peak1: float
    peak_to_peak2:float
    area1: float
    area2:float
    rms1:float
    rms2:float
    intensity:float
    triggerindex:int

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
    intensity:float
    triggerindex:int
    

def extract_evoked_responses(parseddata:TrialInfo,filename:str,isparsesingle:bool,isparsepaired:bool,isparsetrans:bool,userstarttime:int,userendtime:int,subjectname:str,trialcondition:str,subtrialcondition:str,filedata:str):
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

    arr = np.array(parseddata.Ds8.times)

    triggeruncleaned = arr[np.where((arr >userstarttime) & (arr <userendtime))]

    
  
    triggercleaned=[]
    times=parseddata.Fdi.times
    i=0

    def clearfirstpass(triggeruncleaned):
        print("cleaning khz ...")
        i = 0
        triggercleaned = []
        while i < len(triggeruncleaned):
            
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
        #+0.01 is to account for small errors same as +5 for frequency
        paired_pulse_isi = 50 / 1000 + 0.01
        train_frq = 20 + 5
        per_s_train = 1 / train_frq
        #edge case of first and last index 
        if i == 0 or i == len(triggercleaned) - 1:


            if i==0:
                rightdiff = triggercleaned[i + 1] - x
                try:
                    rightdiff5 = triggercleaned[i + 4] - x
                except:
                    rightdiff5 =-1
                
                rightdiff2 = triggercleaned[i + 2] - triggercleaned[i + 1]
                
                if rightdiff > 1 and rightdiff > paired_pulse_isi:
                    # is single pusle
                  
                    parsedtrigger.append(("single",triggercleaned[i]))
                elif rightdiff < paired_pulse_isi and rightdiff2 > paired_pulse_isi:
                    
                    
                    parsedtrigger.append(("paired_pulse",triggercleaned[i],triggercleaned[i+1]))
                    i+=1
                    continue
                    
                elif rightdiff5>0 and rightdiff5 / 5 < per_s_train:
                    
                    starttrain.append(i)
                    starttrain.append(triggercleaned[i])
            elif i == len(triggercleaned) - 1:
                try:
                    leftdiff5 = x - triggercleaned[i - 4]
                except:
                    leftdiff5=-1
                

                leftdiff2 = triggercleaned[i - 1] - triggercleaned[i - 2]
                
                leftdiff = x - triggercleaned[i - 1]
                
                if leftdiff > 1 and leftdiff > paired_pulse_isi:
                    # is single pusle
                    
                    parsedtrigger.append(("single", triggercleaned[i]))
                


                elif leftdiff5>0 and leftdiff5 / 5 < per_s_train :
                    print("endtrain")
                    trainlist.append((starttrain[0],starttrain[1],i,triggercleaned[i]))
                    starttrain=[]

                    pass


            i+=1
            continue

        try:
            rightdiff = triggercleaned[i + 1] - x
            try:
                rightdiff5 = triggercleaned[i + 4] - x
            except:
                rightdiff5 = -1

            try:
                rightdiff2=  triggercleaned[i +2] - triggercleaned[i +1]
            except:
                rightdiff2=100
            
            try:
                leftdiff5= x- triggercleaned[i -4]
            except:
                leftdiff5= -1
            
            
            
            leftdiff = x - triggercleaned[i - 1]
        except:
            i += 1
            continue
        if (rightdiff > 1 and rightdiff > paired_pulse_isi) and (leftdiff > 1 and leftdiff > paired_pulse_isi):
            # is single pusle
           

            parsedtrigger.append(("single", triggercleaned[i]))
        elif rightdiff<paired_pulse_isi and leftdiff>paired_pulse_isi and rightdiff2>paired_pulse_isi:
            print("startdouble")
            startdouble.append(triggercleaned[i])
            parsedtrigger.append(("paired_pulse", triggercleaned[i], triggercleaned[i+1]))
            i+=1
            continue
            
       
            
        elif rightdiff5>0 and rightdiff5 / 5 < per_s_train and leftdiff> per_s_train:
            print("starttrain")
            starttrain.append(i)
            starttrain.append(triggercleaned[i])


        elif leftdiff5>0 and leftdiff5/5< per_s_train and rightdiff> per_s_train:
           
            print("endtrain")
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
    

   
    

    firstderivative = [intensity[i+1]-intensity[i] if i+1<len(intensity) else 0 for i in range(len(intensity))]

   

    jj=0
    filteredintensity=[]
    stable=[]
    startstable=[]
    endstable=0
    
    while jj <len(firstderivative) :

        #this is the acceptable change ( threshold 0.2)
        #this is the change intensity ,so if it deviates more than 0.2 in any direction it will mark the end of a stable period ( regardless of how long it is , even if it is only 0.5s)
        if (firstderivative[jj]<=0.2 and firstderivative[jj]>=-0.2 ):

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
   
    
    
    print(stable)
    for x in stable.copy() :
        #definition of stable period 
        if intensitytime[x[2]]-intensitytime[x[0]]>=2:
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
    
    print(trainlist)
    for x in trainlist.copy():
        starttargettime= x[1]
        endtargettime=x[3]
        for y in stable:
            if y[1]>starttargettime and y[3]<endtargettime:
                finaltrainlist.append(y)
            else:
                pass


   
    traintime=[]
    print(finaltrainlist)
    #finaltrainlist is a list of stable periods in intensity >3s but for all time not just trains period 
    for train in finaltrainlist:
        #return index from cleanedtriggerlist
        #do the seconds  here trim the first second here
        start= train[1]
        end=train[3]
        intensity=train[4]
        startindex=[]
        endindex=[]
        #triggercleaned is cleaning of khz( first pass)
        for i , x in enumerate(triggercleaned):
            #this is adjusting how many seconds to trim ( this s trimming last 1 second)
            if x>=end-1 and len(startindex)==0:
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

    
    print(parsedtrigger)
   
    def parsesingle(x):
        import numpy as np
        if isparsesingle==False:
            return
    
        target=x[1]
        left=target-200/1000

        right=100/1000+target

        times=parseddata.Fdi.times
    
    
        def condition(element):
            return element >=left
        def condition2(element):
            return element >=right
        def condition3(element):
            return element >=target
        def intensity(element):
            return element >=target
        def artifactstart(element,artifacttime):
            return element >=artifacttime
        intensityindex=next((i for i, elem in enumerate(parseddata.Stim.times) if intensity(elem)), None)
        triggerindex=next((i for i, elem in enumerate(times) if condition3(elem)), None)
        
        startindex= next((i for i, elem in enumerate(times) if condition(elem)), None)
        
        #slice the array to make it faster.
        sliced_array = times[startindex:]

        #find artifactsrart time 
        
        #noww to return the first index this is in the array 
        
        endindex=next((i for i, elem in enumerate(sliced_array) if condition2(elem)), None)
        TKEOarray= utlis.TEOCONVERT(parseddata.Fdi.values)
        skipartifactstarttime= parseddata.Fdi.times[triggerindex] +0.005
        print(f"shitty {skipartifactstarttime}")
        import time
        
        artifactsrtaindex= next((i for i, elem in enumerate(times[triggerindex:endindex+startindex]) if artifactstart(elem,skipartifactstarttime)), None)
        artidactendindex=next((i for i, elem in enumerate(times[triggerindex:endindex+startindex]) if artifactstart(elem,skipartifactstarttime+0.09)), None)
        print(artifactsrtaindex)
        
        baselinesd= np.std([abs(num) for num in TKEOarray[artifactsrtaindex+triggerindex:artidactendindex+triggerindex]])
        baselineavg=np.average([abs(num) for num in TKEOarray[artifactsrtaindex+triggerindex:artidactendindex+triggerindex]])
        peak_to_peak, area=compute_outcome_measures._calculate_waveform_stats(parseddata.Fdi.values, startindex, endindex+startindex,triggerindex,parseddata.Fdi.times,baselinesd,baselineavg,artifactsrtaindex)
        
        
        onsetindex=compute_outcome_measures.findonset(TKEOarray[triggerindex:endindex+startindex],baselinesd,baselineavg,artifactsrtaindex)
        try:
            onsettime =parseddata.Fdi.times[onsetindex+triggerindex]
            relativetime=onsettime-parseddata.Fdi.times[triggerindex]
        except:
            onsettime=None
        
        
        print(skipartifactstarttime)
        print(artifactsrtaindex)
        #need to figure out how many ms to skip and how many index....
       
       
    
        data=SinglePulse("singlepulse",parseddata.Fdi.values[startindex:endindex+startindex],startindex,endindex+startindex,onsettime,peak_to_peak,area,0,parseddata.Stim.values[intensityindex],triggerindex)



        return data

        #subsetit and then calculate shit






  
        
     
    
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
        def intensity(element):
            return element >=target1
        def artifactstart(element,artifacttime):
            return element >=artifacttime
        intensityindex=next((i for i, elem in enumerate(parseddata.Stim.times) if intensity(elem)), None)
        triggerindex1=next((i for i, elem in enumerate(time) if condition6(elem)), None)
        triggerindex2=next((i for i, elem in enumerate(time) if condition7(elem)), None)
        
        startindex = next((i for i, elem in enumerate(time) if condition(elem)), None)
        baselinesd= np.std([abs(num) for num in parseddata.Fdi.values[startindex:triggerindex1]])
        baselineavg=np.average([abs(num) for num in parseddata.Fdi.values[startindex:triggerindex1]])
        
        # slice the array to make it faster.
        sliced_array = time[startindex:]
  
        endindex = next((i for i, elem in enumerate(sliced_array) if condition2(elem)), None)
        skipartifactstarttime= parseddata.Fdi.times[triggerindex1] +0.005
        print (skipartifactstarttime)
        
        skipartifactstarttime2= parseddata.Fdi.times[triggerindex2] +0.005
        artifactsrtaindex= next((i for i, elem in enumerate(time[triggerindex1:endindex+startindex]) if artifactstart(elem,skipartifactstarttime)), None)
        artifactsrtaindex2= next((i for i, elem in enumerate(time[triggerindex2:endindex+startindex]) if artifactstart(elem,skipartifactstarttime2)), None)
        print (artifactsrtaindex)
        print(artifactsrtaindex2)
        
        subtargetarray=time[startindex:endindex+startindex]
 
        firststartindex=next((i for i, elem in enumerate(subtargetarray) if subcondition1left(elem)), None)
        firstendindex = next((i for i, elem in enumerate(subtargetarray) if subcondition1right(elem)), None)
        secondstartindex = next((i for i, elem in enumerate(subtargetarray) if subcondition2left(elem)), None)
        secondendindex = next((i for i, elem in enumerate(subtargetarray) if subcondition2right(elem)), None)
        #TKEOarray=utlis.TEOCONVERT(parseddata.Fdi.values)
        #baselinesd2=np.std([abs(num) for num in TKEOarray[secondendindex+startindex:endindex+startindex]])
        #baselineavg2=np.average([abs(num) for num in TKEOarray[secondendindex+startindex:endindex+startindex]])
        
        peak_to_peak1, area1=compute_outcome_measures._calculate_waveform_stats(parseddata.Fdi.values, firststartindex+startindex, firstendindex+firststartindex+startindex,triggerindex1,parseddata.Fdi.times,baselinesd,baselineavg,artifactsrtaindex)
        peak_to_peak2, area2=compute_outcome_measures._calculate_waveform_stats(parseddata.Fdi.values, secondstartindex+startindex, secondendindex+secondstartindex+startindex,triggerindex2,parseddata.Fdi.times,baselinesd,baselineavg,artifactsrtaindex)
        onsetindex1=compute_outcome_measures.findonset(parseddata.Fdi.values[triggerindex1:firstendindex+firststartindex+startindex],baselinesd,baselineavg,0,3,5)
        print([onsetindex1,baselinesd,baselineavg,artifactsrtaindex])
        
        
        onsetindex2=compute_outcome_measures.findonset(parseddata.Fdi.values[triggerindex2:secondendindex+secondstartindex+startindex],baselinesd,baselineavg,artifactsrtaindex2,3,5)
        try:
            onset1=parseddata.Fdi.times[onsetindex1+triggerindex1]
            
        except:
            onset1=None
        try:
            onset2=parseddata.Fdi.times[onsetindex2+triggerindex2]
        except:
            onset2=None
        
        
        data = PairedPulse("pairedpulse",FDI[startindex:endindex+startindex],FDI[firststartindex+startindex:firstendindex+startindex],FDI[secondstartindex+startindex:secondendindex+startindex],firststartindex+startindex,firstendindex+startindex,secondstartindex+startindex,secondendindex+startindex,triggerindex1,triggerindex2,onset1,onset2,peak_to_peak1,peak_to_peak2,area1,area2,0,0,parseddata.Stim.values[intensityindex],triggerindex1)
        
        
        return data




    def parsetrans(x):
        import numpy as np
        if isparsetrans==False:
            return
        
        

      
        target = x[1]
        left = target - 5 / 1000
        right = 25/ 1000 + target
        times = parseddata.Fdi.times
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
        def intensity(element):
            return element >=target
        def artifactstart(element,artifacttime):
            return element >=artifacttime
        
        intensityindex=next((i for i, elem in enumerate(parseddata.Stim.times) if intensity(elem)), None)
        triggerindex=next((i for i, elem in enumerate(times) if condition3(elem)), None)
        
        startindex = next((i for i, elem in enumerate(times) if condition(elem)), None)
        # slice the array to make it faster.
        sliced_array = times[startindex:]
        TKEOarray= utlis.TEOCONVERT(parseddata.Fdi.values)
        skipartifactstarttime= parseddata.Fdi.times[triggerindex] +0.005
        print(f"shitty {skipartifactstarttime}")
        import time
        
        
        


        endindex = next((i for i, elem in enumerate(sliced_array) if condition2(elem)), None)
        skipartifactstarttime= parseddata.Fdi.times[triggerindex] +0.005
        artifactsrtaindex= next((i for i, elem in enumerate(times[triggerindex:endindex+startindex]) if artifactstart(elem,skipartifactstarttime)), None)
        print(artifactsrtaindex)
        
        #artidactendindex=next((i for i, elem in enumerate(times[triggerindex:endindex+startindex]) if artifactstart(elem,skipartifactstarttime+0.09)), None)
        print(artifactsrtaindex)
        
        baselinesd= np.std([abs(num) for num in parseddata.Fdi.values[startindex:triggerindex]])
        baselineavg=np.average([abs(num) for num in parseddata.Fdi.values[startindex:triggerindex]])
        peak_to_peak, area=compute_outcome_measures._calculate_waveform_stats(parseddata.Fdi.values, startindex, endindex+startindex,triggerindex,parseddata.Fdi.times,baselinesd,baselineavg,artifactsrtaindex)
        onsetindex=compute_outcome_measures.findonset(TKEOarray[triggerindex:endindex+startindex],baselinesd,baselineavg,artifactsrtaindex)
        try:
            onsettime =parseddata.Fdi.times[onsetindex+triggerindex]
            relativetime=onsettime-parseddata.Fdi.times[triggerindex]
        except:
            onsettime=None
        
        data=SingleTransPulse("single_trans_pulse",parseddata.Fdi.values[startindex:endindex+startindex],startindex,endindex+startindex,onsettime,peak_to_peak,area,0,parseddata.Stim.values[intensityindex],triggerindex)
        
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
    directory = "extracted_reflexes_data"
    directory_path = os.path.join(os.getcwd(), directory)
    os.makedirs(directory_path, exist_ok=True)
    os.makedirs(os.path.join(os.getcwd(),directory, subjectname), exist_ok=True)
    os.makedirs(os.path.join(os.getcwd(),directory, subjectname,trialcondition), exist_ok=True)
    os.makedirs(os.path.join(os.getcwd(),directory, subjectname,trialcondition,f"{subtrialcondition}_{filedata}"), exist_ok=True)
    trialconditionfolder=os.path.join(os.getcwd(),directory, subjectname,trialcondition,f"{subtrialcondition}_{filedata}")
    data_file_path = os.path.join(trialconditionfolder, "data")
    img_path=os.path.join(trialconditionfolder, "img")
 
    
    

    #do something with the pickledtarget 
    print(parsedtrigger)
    """
        def diff_intensity_outcomemeasure(pickledtarget):
            singleintensity = [round(i.intensity) for i in pickledtarget if i.name == "singlepulse"]
            pariedintensity = [round(i.intensity)  for i in pickledtarget if i.name == "pairedpulse"]
            single_trans_intensity = [round(i.intensity)  for i in pickledtarget if i.name == "single_trans_pulse"]
            cleanedsingle=list(set(singleintensity))
            cleanedpaired=list(set(pariedintensity))
            cleanedtrans=list(set(single_trans_intensity))
            def sorting (list):


                if len(list) == 0:
                    return list
                else:
                    newlist=sorted(list)
                    return newlist
            
            
            #need a list of waveforms to correspond with a list of intensity s, {{122,,,d,}} to [1,2,]
            intensitylist=[]
            for index,i in enumerate([sorting(cleanedsingle),sorting(cleanedpaired),sorting(cleanedtrans)]):
                print('hi')
                if index==0:
                    name="singlepulse"
                elif index==1:
                    name="pairedpulse"

                elif index==2:
                    name="single_trans_pulse"
                filtered_list=[]
                for intensityvalue in i:
                    for obj in pickledtarget:
                        if obj.name == name and round(obj.intensity) == intensityvalue:
                            if obj.name=="pairedpulse":
                                filtered_list.append([(obj.startindex1,obj.endindex1,obj.startindex2,obj.endindex2)])
                            else:
                                filtered_list.append([(obj.waveform,obj.startindex,obj.endindex)])


                    #filtered_list = [(obj.startindex,obj,endindex) for obj in pickledtarget if obj.name == name and round(obj.intensity) == intensityvalue]
                    intensitylist.append((intensityvalue,filtered_list,index))

            print (len(intensitylist))
            return intensitylist
        
        groupedintensitylist=diff_intensity_outcomemeasure(pickledtarget)
        print (groupedintensitylist)
        def intensityparse(x,timeelapsed):
            awaveform=[]
            t_elasped=timeelapsed
            
            
            xaixs=[]
            yaxis=[]
            print(x[1])
            
            #this is filtered list and it  is [[(,)],[],[]]
            for y in x[1]:
                
                
                awaveform.append(y[0][0])
            max_len = max(len(arr) for arr in awaveform)
            print(max_len)
        
            
            def artifactstart(element,artifacttime):
                return element >=artifacttime
            # Resize the arrays to have the same shape
            resized_list = [np.resize(arr, (max_len,)) for arr in awaveform]
            avg_arr = np.mean(resized_list, axis=0)
        
            timeaxis = np.linspace(0,  t_elasped, num=len(avg_arr))
            triggerindex = np.where(timeaxis >= 0.02)[0][0]
            baselinesd= np.std([abs(num) for num in avg_arr[0:triggerindex]])
            baselineavg=np.average([abs(num) for num in avg_arr[0:triggerindex]])
            skipartifactstarttime= 0.0005+0.02
            artifactsrtaindex= next((i for i, elem in enumerate(timeaxis) if artifactstart(elem,skipartifactstarttime)), None)
            print(artifactsrtaindex)
            onsetindex=compute_outcome_measures.findonset(avg_arr[triggerindex:],baselinesd,baselineavg,artifactsrtaindex-triggerindex)
            print(onsetindex)
            print(baselineavg)
            print(baselinesd)
            plt.plot(timeaxis,avg_arr)
            plt.axvline(x=timeaxis[triggerindex], color='r')
            plt.axvline(x=timeaxis[artifactsrtaindex], color='r')
            plt.axvline(x=timeaxis[onsetindex+triggerindex], color='b')
            plt.show()
            plt.close()
            
            relativeonsettime=timeaxis[onsetindex+triggerindex]-timeaxis[triggerindex]
            print(relativeonsettime)
            
            
            return relativeonsettime
        secondpickled=[]
        for x in groupedintensitylist:
            if x[2]=="pairedpulse":
                print("hi")
            
            elif x[2]=="singlepulse":
                result=intensityparse(x,0.3)
                print(f"this is {result}")
                blob={"intensity":x[0], "avg_onset":result}
                secondpickled.append(blob)
                

            elif x[2 =="single_trans_pulse"]:
                result=intensityparse(x,0.03)
                print(f"this is {result}")
                blob={"intensity":x[0], "avg_onset":result}
                secondpickled.append(blob)

        
        print(secondpickled)
        
    """
    
    

        

   

    print("Now there should a folder in the directory where you are running your script called extracted reflexs data, and the picked data should be in there!")
   


    import numpy as np

    x = intensitytime
    y1 = firstderivative
    y2 = intensity

    ##plot it out man
    #x1 will be FDI times and values and then
    #also want the event cahnnels
    xx1=parseddata.Fdi.times
    yy1=parseddata.Fdi.values
    print(masterresult)

    #need to generate another file for grouped results...
    #for each protocol 


    groupedmeasure=graphgenerator.generate_graph(triggercleaned, triggeruncleaned, checktrigger, xx1, yy1, parseddata, masterresult, masteronset, userstarttime, userendtime, img_path,pickledtarget,filedata)
    

    with open(f"{data_file_path}.pkl", "wb") as f:
        # Write the pickled data to the file
        pickle.dump({"individual":pickledtarget,"grouped":groupedmeasure}, f)
    
    # Close the file
    f.close()

