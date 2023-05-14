#this is the userinput class 
import numpy as np
class User_Specified_Data:
    """Extract user specified window from data"""
    def __init__(self, raw_data,triggerchannel,range,khz_clean):
        self.event_data = raw_data
        self.channel=triggerchannel
        self.starttime=range["userstarttime"]
        self.endtime=range["userendtime"]
        self.khz_clean=khz_clean
        self.unclean=[]
    
    
        
    def extract(self):
        triggeruncleaned = self.channel[np.where((self.channel >self.starttime) & (self.channel <self.endtime))]
        self.unclean=triggeruncleaned
        return self
    
    
    def remove_khz(self):
        
        i = 0
        triggercleaned = []
        while i < len(self.unclean):
        
            per_s = 1 / (self.khz_clean * 1000) + 0.00005
            try:
                rightdiff = self.unclean[i + 1] - self.unclean[i]
                if rightdiff < per_s:
                    
                    triggercleaned.append(self.unclean[i])
                    i += self.khz_clean
                    continue
            except:
                pass
            i += 1
        if len(triggercleaned)==0:
            return self.unclean
        else:
            return triggercleaned


    
       