import numpy as np
class ExtractStabletrains:
    def __init__(self, trialobject, starttrain,endtrain):
        self.trial_object=trialobject
        self.intensitytime=trialobject.Stim.times
        self.intensityvalues=trialobject.Stim.values
        self.starttraintime= starttrain
        self.endtraintime=endtrain
    def extract_stable(self):
        
        startintensityindex=np.where(self.intensitytime >= self.starttraintime)[0][0]
        endintensityindex=np.where(self.intensitytime >= self.endtraintime)[0][0]
        print(startintensityindex)
        print(endintensityindex)
        filteredintensityarray= self.intensityvalues[startintensityindex:endintensityindex]
        #now need to extract the stable periood.
        firstderivative = [filteredintensityarray[i+1]-filteredintensityarray[i] if i+1<len(filteredintensityarray) else 0 for i in range(len(filteredintensityarray))]

        jj=0
        stable=[]
        startstable=[]
        endstable=0
        
        while jj <len(firstderivative) :

            #this is the acceptable change ( threshold 0.2)
            #this is the change intensity ,so if it deviates more than 0.2 in any direction it will mark the end of a stable period ( regardless of how long it is , even if it is only 0.5s)
            if (firstderivative[jj]<=0.2 and firstderivative[jj]>=-0.2 ):

                startstable.extend([jj+startintensityindex, self.intensitytime[jj+startintensityindex], self.intensityvalues[jj+startintensityindex]])
                

            else:
                if len(startstable)>0:
                    endstable=jj++ startintensityindex
                    stable.extend([(startstable[0], startstable[1], endstable-1, self.intensitytime[endstable-1], startstable[2])])
                    #(index of start in bigger tiem array, valeu of time at that index, index of end , value of time at end, and intensity)
                    startstable=[];
                    endstable=0
                
                else:
                    pass



            jj += 1
        duration=2
        for x in stable.copy() :
            #definition of stable period 
            if self.intensitytime[x[2]]-self.intensitytime[x[0]]>=duration:
                pass
            else:
                
                stable.remove(x)
        print(stable)
        print ("above is stable")
        return stable

        


class Train_preprocessing:
    def __init__(self, trialobject,classified_entirelist,unclassified_entirelist):
        self.trial_object=trialobject
        self.intensitytime=trialobject.Stim.times
        self.intensityvalues=trialobject.Stim.values
        self.data = classified_entirelist
        self.unclassified_triggger=unclassified_entirelist
        self.data_removed_trainsblock=[]
        self.filteredtrains=[]
    def extract_trains_period(self):
        test_list = self.data
 
# initialize target list
        tar_list = ['Trains_Start','Trains_End']
        self.filteredtrains = [tup for tup in test_list if any(i in tup for i in tar_list)]
        print("shit")
        print(self.filteredtrains)
        self.data_removed_trainsblock = [tup for tup in test_list if not any(i in tup for i in tar_list)]
        self.flatten_trains_block()
        return  self

    def flatten_trains_block(self):
        if self.filteredtrains==[]:
            return self 
        else:
            for i in range(0, len(self.filteredtrains), 2):
                starttrain_time= self.filteredtrains[i][1]
                endtrain_time=self.filteredtrains[i+1][1]
                print("strttraintime")
                print(starttrain_time)
                print (endtrain_time)
                print(self.trial_object)
    
                #alltriggers_between_trains=self.unclassified_triggger[np.where(self.intensitytime == starttrain_time)[0] + 1:np.where(self.intensitytime == endtrain_time)[0]]
                #now i need to find the stable periods and then filter them  
                stable_periods=ExtractStabletrains(self.trial_object,starttrain_time,endtrain_time).extract_stable() 
                print("below is styable")
                print(stable_periods)
                #now need to produce the ( "sINGLE trains pulse, trigger time")
                singletranspulse=[]
                for cleantrigger in self.unclassified_triggger:
                    for stable in stable_periods:
                        if cleantrigger>=stable[3]-0.1 and cleantrigger<=stable[3]:
                            self.data_removed_trainsblock.append(("Single_Trains_pulse",cleantrigger))


                
