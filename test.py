from plugin import main
from spike2py.trial import TrialInfo, Trial
"""
02_data001_C_M
02_data002_HF_M
04_ds7_cct17
04_ds7_setup000
"""
#file="C:/Users/wanho/Downloads/02_data000_HF_B.mat"
#ile="C:/Users/wanho/Downloads/data/02_data001_C_M.mat"


data =Trial(TrialInfo(file="C:/Users/wanho/Downloads/data/02_data001_C_M.mat",channels=["MMax","FDI","Ds8","stim"]))


#this function assumes the Trial object contains the following Ds8 and Fdi 
#but obviously user will be able to specify later on....
#right now user can choose to disbale parsing on one of three trigger types
#single
#paired 
#trans_single
#if you are playing with it I recommend disabling trans_single as it will take a while...
#this is obviously a very basic version but perhaps we can iterate on it ?
# I haven't implemented class but will do so for sure
# I read through your email last night but havnt had the chance to implement those ideas but will do so in the weekends and see how I go
#I will think through the edge cases you mentioned, I might change up the whole struture or reuse some of it but I will see
# the major problem now is it is simply taking too long ( will figure somethign out) and it the onset time is troublesome (will sort that out)
main.extract_evoked_responses(data,data.info.name,True,False,False)
