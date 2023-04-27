from plugin import main
from spike2py.trial import TrialInfo, Trial
import json
"""
02_data001_C_M
02_data002_HF_M
04_ds7_cct17
04_ds7_setup000
"""
#file="C:/Users/wanho/Downloads/02_data000_HF_B.mat"
#ile="C:/Users/wanho/Downloads/data/02_data001_C_M.mat"
with open('data.json', 'r') as f:
    data = json.load(f)

subject=data['sub_ID']
trialcondition=["kHz_monophasic","kHz_biphasic","conventional_monophasic","conventional_biphasic"]
subtrialconditionlist=["threshold_window","doubles_105_threshold_window","doubles_5_mmax_window","trains_threshold_window"]
list=[]
for x in trialcondition:
    
    filename=data[x]["filename"]
    for y in subtrialconditionlist:
        list.append((subject,filename,x,y,data[x][y][0],data[x][y][1]))
print (list)
for i in list:
    #point this to the mat folder you shared with me on dropbox 
    data =Trial(TrialInfo(file=f"C:/Users/wanho/Downloads/matfiles/{i[1]}.mat",channels=["MMax","FDI","Ds8","stim"]))
    #need a list of [subject,trialcondition,subtrial,start,end]
    #and then loop through it 


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
    ###
    
    #"khz_freq":
    #"trans_frequency_units_hz":,
    #"pair_frequency_units_hz":,
    #"pre_stim_time_plot_s":,
    #"post_stim_time_plot_s":,
    ###
    paarameter_dictionary={
    "parseddata":data,
    "filename": data.info.name,
    "isparsesingle": True,
    "isparsepaired": True,
    "isparsetrans": True,
    "userstarttime": i[4],
    "userendtime": i[5],
    "subjectname": i[0],
    "trialcondition": i[2],
    "subtrialcondition": i[3],
    "filedata": i[1]


    }
    main.extract_evoked_responses(**paarameter_dictionary)
