import numpy as np
    

def extract_user_window(arr, userstarttime,userendtime):

    triggeruncleaned = arr[np.where((arr >userstarttime) & (arr <userendtime))]
    return triggeruncleaned

def remove_khz(triggeruncleaned,carrier_frq):
    print("cleaning khz ...")
    i = 0
    triggercleaned = []
    while i < len(triggeruncleaned):
        
        # clean out all kilihertz first
        
        #carrier_frq=khz_freq
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


def classify_triggers(triggercleaned):
    startdouble=[]
    parsedtrigger=[]
    starttrain=[]
    istrains=False
    trainlist=[]
    i=0
    if len(triggercleaned)==1:
        parsedtrigger.append(("single", triggercleaned[0]))
        return parsedtrigger,trainlist
    while i < len(triggercleaned):
    
        x=triggercleaned[i]
        #+0.01 is to account for small errors same as +5 for frequency
        #here is the paired pulse 
        #pair_frequency_units_hz
        paired_pulse_isi = 50 / 1000 + 0.01
        #trans_frequency_units_hz
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

    return parsedtrigger, trainlist
  