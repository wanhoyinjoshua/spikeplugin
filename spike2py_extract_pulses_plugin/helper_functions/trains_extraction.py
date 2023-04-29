def extract_stable_trains_period(intensity,intensitytime,duration):

    
   
    

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
        if intensitytime[x[2]]-intensitytime[x[0]]>=duration:
           pass
        else:
            
            stable.remove(x)
    return stable
   

def traintime(trainlist,stable,triggercleaned):
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
    
    return traintime
    