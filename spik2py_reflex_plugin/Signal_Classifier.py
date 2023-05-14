import numpy as np
class Event:
    def __init__(self,trigger, triggertimes):
        
        self.trigger= trigger
        self.unclassified_trigger = triggertimes
        
    def meet_condition(trigger,self):
        return False

class Difference_Calculator:
    def __init__(self,trigger, triggertimes):
        self.alltriggers = triggertimes
        self.trigger= trigger
        
        self.index=np.where(triggertimes >= trigger)[0][0]
    def leftdiff(self):
        index = self.index
        if index==0:
            return None
        try:
            
            leftdiff = self.alltriggers[index]-self.alltriggers[index - 1] 
            return leftdiff
        except:
            return None
    def rightdiff(self):
        index = self.index
        if self.alltriggers[index]== self.alltriggers[-1]:
            return None
        try:
            rightdiff = self.alltriggers[index + 1] -self.alltriggers[index]
            return rightdiff
        except:
            return None
    def leftdiff2(self):
        index = self.index
        if index==0:
            return None
        try:
            
            leftdiff = self.alltriggers[index-1]-self.alltriggers[index - 2] 
            return leftdiff
        except:
            return None
    def rightdiff2(self):
        index = self.index
        if self.alltriggers[index]== self.alltriggers[-1]:
            return None
        try:
            rightdiff = self.alltriggers[index + 2] -self.alltriggers[index+1]
            return rightdiff
        except:
            return None
    def rightdiff5(self):
        index = self.index
        if self.alltriggers[index]== self.alltriggers[-1]:
            return None
        try:
            rightdiff = self.alltriggers[index + 4] -self.alltriggers[index]
            return rightdiff
        except:
            return None
    def leftdiff5(self):
        index = self.index
        if index==0 or index==1 or index==2 or index==3  :
            return None
        try:
            leftdiff = self.alltriggers[index] -self.alltriggers[index-4]
            return leftdiff
        except:
            return None
    
    
    

class Single_Pulse(Event):
    name="Single_Pulse"
    def __init__(self, triggertimes, trigger, param):
        super().__init__(triggertimes, trigger)
        self.name="Single_Pulse"
        self.index = None
        self.left_diff=Difference_Calculator(self.unclassified_trigger,self.trigger).leftdiff()
        self.right_diff=Difference_Calculator(self.unclassified_trigger,self.trigger).rightdiff()
        self.paired_pulse_isi=param["paired_pulse_isi"]

    def getname(self):
        return self.name
    def meet_condition(self):
  
       
        if self.left_diff==None:
            if self.right_diff > 1 and self.right_diff > self.paired_pulse_isi:
                return self.name , True
            else:
                return self.name ,False
        
        elif self.right_diff==None:
            if self.left_diff > 1 and self.left_diff > self.paired_pulse_isi:
                return self.name , True
            else:
                return self.name ,False

        else:
            if self.right_diff > 1 and self.left_diff>1 and self.right_diff > self.paired_pulse_isi:
                return self.name , True
            else:
                return self.name ,False


class Paired_Pulse(Event):
    name="Paired_Pulse"
    def __init__(self, triggertimes, trigger, param):
        super().__init__(triggertimes, trigger)
        self.name="Paired_Pulse"
        self.index = None
        self.left_diff=Difference_Calculator(self.unclassified_trigger,self.trigger).leftdiff()
        self.right_diff=Difference_Calculator(self.unclassified_trigger,self.trigger).rightdiff()
        self.right_2_diff= Difference_Calculator(self.unclassified_trigger,self.trigger).rightdiff2()
        self.left_2_diff= Difference_Calculator(self.unclassified_trigger,self.trigger).leftdiff2()
        self.paired_pulse_isi=param["paired_pulse_isi"]

    def getname(self):
        return self.name
    def meet_condition(self):
       
        if self.left_diff==None :
            if self.right_diff < self.paired_pulse_isi and self.right_2_diff > self.paired_pulse_isi:
                return self.name , True
            else:
                return self.name ,False
        elif self.right_diff==None :
            return self.name, False
        elif self.right_2_diff==None:
            if self.right_diff < self.paired_pulse_isi and self.left_diff > self.paired_pulse_isi:
                return self.name , True
            else:
                return self.name ,False

        

        else:
            if self.right_diff<self.paired_pulse_isi and self.left_diff>self.paired_pulse_isi and self.right_2_diff>self.paired_pulse_isi:
                return self.name , True
            else:
                return self.name ,False


class Trains(Event):
    name=""
    def __init__(self, triggertimes, trigger, param):
        super().__init__(triggertimes, trigger)
        self.name="Trains"
        self.index = None
        self.left_diff=Difference_Calculator(self.unclassified_trigger,self.trigger).leftdiff()
        self.right_diff=Difference_Calculator(self.unclassified_trigger,self.trigger).rightdiff()
        self.right_diff_5=Difference_Calculator(self.unclassified_trigger,self.trigger).rightdiff5()
        self.left_diff_5=Difference_Calculator(self.unclassified_trigger,self.trigger).leftdiff5()
       
        self.right_2_diff= Difference_Calculator(self.unclassified_trigger,self.trigger).rightdiff2()
        self.left_2_diff= Difference_Calculator(self.unclassified_trigger,self.trigger).leftdiff2()
        self.per_s_train=param["per_s_train"]
        
    def getname(self):
        return self.name

    def meet_condition(self):
        
        
        
            
        if self.left_diff==None :
            
            if self.right_diff_5 / 5 < self.per_s_train:
                self.name="Trains_Start"
                return self.name , True
            else:
                return self.name ,False
        
        elif self.right_diff==None:
            if self.left_diff_5 / 5 < self.per_s_train:
                self.name="Trains_End"
                return self.name , True
            else:
                return self.name ,False

    

        else:
            
            try:
                if self.right_diff_5 / 5 < self.per_s_train and self.left_diff> self.per_s_train:
                    self.name="Trains_Start"
                    return self.name , True
                elif self.left_diff_5/5< self.per_s_train and self.right_diff> self.per_s_train:
                    self.name="Trains_End"
                    return self.name , True
                else:
                    return self.name,False
            except:
                return self.name , False
            
            
        



        



class Pulse_Classifier:
    """transform list of trigertimes to list of trigger times with pulse time"""
    def __init__(self, triggertimes,paired_pulse_isi,per_s_train):
        self.unclassified_trigger = triggertimes
        self.classified_trigger:list=[]
        self.paired_pulse_isi=paired_pulse_isi
        self.per_s_train=per_s_train
        

    def classify(self):
        param={
            "paired_pulse_isi":self.paired_pulse_isi,
            "per_s_train":self.per_s_train
        }
        skip_next = False
        for index,trigger in enumerate(self.unclassified_trigger):
            if skip_next:
                skip_next = False
                continue # skip 
            for subclass in Event.__subclasses__():
                name,boolval=subclass(self.unclassified_trigger,trigger,param).meet_condition()
                if boolval==True:
                    if subclass.__name__=="Paired_Pulse":
                        self.classified_trigger.append((name,trigger,self.unclassified_trigger[index+1]))
                        skip_next = True
                        break

                    else:
                            
                        self.classified_trigger.append((name,trigger))
                        break
                else:
                    pass

        return self.classified_trigger
