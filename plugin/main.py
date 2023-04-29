
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
from plugin.helper_functions import signal_cleaning, trains_extraction
from plugin import utlis


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
  
    triggeruncleaned=signal_cleaning.extract_user_window(arr, userstarttime,userendtime)
    
    khz_frq=10
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

    
    print(parsedtrigger)

###################
#now we have the parsed trigger of every pusle, now we are ready to parse it 
###################









   
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
        peak_to_peak, area=compute_outcome_measures.compute_peak2peak_area(parseddata.Fdi.values[artifactsrtaindex+triggerindex:endindex+startindex])
        
        
        onsetindex=compute_outcome_measures.findonset(TKEOarray[triggerindex:endindex+startindex],baselinesd,baselineavg,artifactsrtaindex)
        try:
            onsettime =parseddata.Fdi.times[onsetindex+triggerindex]
            relativetime=onsettime-parseddata.Fdi.times[triggerindex]
        except:
            onsettime=None
            relativetime=None
        
        
        print(skipartifactstarttime)
        print(artifactsrtaindex)
        #need to figure out how many ms to skip and how many index....
       
       
    
        data=SinglePulse("singlepulse",parseddata.Fdi.values[startindex:endindex+startindex],startindex,endindex+startindex,relativetime,onsettime,peak_to_peak,area,0,parseddata.Stim.values[intensityindex],triggerindex)



        return data

        #subsetit and then 






  
        
     
    
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
        peak_to_peak1, area1=compute_outcome_measures.compute_peak2peak_area(parseddata.Fdi.values[artifactsrtaindex+triggerindex1:firstendindex+startindex])
        #peak_to_peak1, area1=compute_outcome_measures._calculate_waveform_stats(parseddata.Fdi.values, firststartindex+startindex, firstendindex+firststartindex+startindex,triggerindex1,parseddata.Fdi.times,baselinesd,baselineavg,artifactsrtaindex)
        peak_to_peak2, area2=compute_outcome_measures.compute_peak2peak_area(parseddata.Fdi.values[artifactsrtaindex2+triggerindex2:secondendindex+startindex])
        #peak_to_peak2, area2=compute_outcome_measures._calculate_waveform_stats(parseddata.Fdi.values, secondstartindex+startindex, secondendindex+secondstartindex+startindex,triggerindex2,parseddata.Fdi.times,baselinesd,baselineavg,artifactsrtaindex2)
        peak_to_peak_ratio=peak_to_peak1/peak_to_peak2
        area_ratio=area1/area2
        
        onsetindex1=compute_outcome_measures.findonset(parseddata.Fdi.values[triggerindex1:firstendindex+firststartindex+startindex],baselinesd,baselineavg,0,3,5)
        print([onsetindex1,baselinesd,baselineavg,artifactsrtaindex])
        
        
        onsetindex2=compute_outcome_measures.findonset(parseddata.Fdi.values[triggerindex2:secondendindex+secondstartindex+startindex],baselinesd,baselineavg,artifactsrtaindex2,3,5)
        try:
            onset1=parseddata.Fdi.times[onsetindex1+triggerindex1]
            relativetime1=onset1-parseddata.Fdi.times[triggerindex1]
            
        except:
            onset1=None
            relativetime1=None
        try:
            onset2=parseddata.Fdi.times[onsetindex2+triggerindex2]
            relativetime2=onset2-parseddata.Fdi.times[triggerindex2]
        except:
            onset2=None
            relativetime2=None
        
        
        data = PairedPulse("pairedpulse",FDI[startindex:endindex+startindex],FDI[firststartindex+startindex:firstendindex+startindex],FDI[secondstartindex+startindex:secondendindex+startindex],firststartindex+startindex,firstendindex+startindex,secondstartindex+startindex,secondendindex+startindex,triggerindex1,triggerindex2,relativetime1,onset1,relativetime2,onset2,peak_to_peak1,peak_to_peak2,area1,area2,0,0,parseddata.Stim.values[intensityindex],triggerindex1,peak_to_peak_ratio,area_ratio)
        
        
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
        
        import time
        
        
        


        endindex = next((i for i, elem in enumerate(sliced_array) if condition2(elem)), None)
        skipartifactstarttime= parseddata.Fdi.times[triggerindex] +0.005
        artifactsrtaindex= next((i for i, elem in enumerate(times[triggerindex:endindex+startindex]) if artifactstart(elem,skipartifactstarttime)), None)
        print(artifactsrtaindex)
        
        #artidactendindex=next((i for i, elem in enumerate(times[triggerindex:endindex+startindex]) if artifactstart(elem,skipartifactstarttime+0.09)), None)
        print(artifactsrtaindex)
        
        baselinesd= np.std([abs(num) for num in parseddata.Fdi.values[startindex:triggerindex]])
        baselineavg=np.average([abs(num) for num in parseddata.Fdi.values[startindex:triggerindex]])
        peak_to_peak, area=compute_outcome_measures.compute_peak2peak_area(parseddata.Fdi.values[artifactsrtaindex+triggerindex:endindex+startindex])
        onsetindex=compute_outcome_measures.findonset(TKEOarray[triggerindex:endindex+startindex],baselinesd,baselineavg,artifactsrtaindex)
        try:
            onsettime =parseddata.Fdi.times[onsetindex+triggerindex]
            relativetime=onsettime-parseddata.Fdi.times[triggerindex]
        except:
            onsettime=None
        
        data=SingleTransPulse("single_trans_pulse",parseddata.Fdi.values[startindex:endindex+startindex],startindex,endindex+startindex,onsettime,relativetime,peak_to_peak,area,0,parseddata.Stim.values[intensityindex],triggerindex)
        
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
    

    ##plot it out man
    #x1 will be FDI times and values and then
    #also want the event cahnnels
    xx1=parseddata.Fdi.times
    yy1=parseddata.Fdi.values
    print(masterresult)

    #need to generate another file for grouped results...
    #for each protocol 


    groupedmeasure=graphgenerator.generate_graph(triggercleaned, triggeruncleaned, checktrigger, xx1, yy1, parseddata, masterresult, masteronset, userstarttime, userendtime, img_path,pickledtarget,filedata)
    
    #utility need to load in function to organise the data for indivisual to group all of them together 
    pickledtarget=utlis.Group_Individual_Pulses(pickledtarget)

    with open(f"{data_file_path}.pkl", "wb") as f:
        # Write the pickled data to the file
        pickle.dump({"individual":pickledtarget,"grouped":groupedmeasure}, f)
    
    # Close the file
    f.close()

