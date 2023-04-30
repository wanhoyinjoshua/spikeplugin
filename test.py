from spik2py_reflex_plugin import main
from spike2py.trial import TrialInfo, Trial
import json
import os
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
subtrialconditionlist=["mmax_window","threshold_window","doubles_105_threshold_window","doubles_5_mmax_window","trains_threshold_window"]
list=[]
for x in trialcondition:
    
    filename=data[x]["filename"]
    for y in subtrialconditionlist:
        list.append((subject,filename,x,y,data[x][y][0],data[x][y][1]))
print (list)
for i in list:
    #point this to the mat folder you shared with me on dropbox 
    data =Trial(TrialInfo(file=f"C:/Users/wanho/Downloads/matfiles/{i[1]}.mat",channels=["MMax","FDI","Ds8","stim"]))
   

    directory = "extracted_reflexes_data"
    subjectname=i[0]
    trialcondition=i[2]
    subtrialcondition=i[3]
    filedata=i[1]



    directory_path = os.path.join(os.getcwd(), directory)
    os.makedirs(directory_path, exist_ok=True)
    os.makedirs(os.path.join(os.getcwd(),directory, subjectname), exist_ok=True)
    os.makedirs(os.path.join(os.getcwd(),directory, subjectname,trialcondition), exist_ok=True)
    os.makedirs(os.path.join(os.getcwd(),directory, subjectname,trialcondition,f"{subtrialcondition}"), exist_ok=True)
    trialconditionfolder=os.path.join(os.getcwd(),directory, subjectname,trialcondition,f"{subtrialcondition}")
    data_file_path = os.path.join(trialconditionfolder, "data")
    img_path=os.path.join(trialconditionfolder, "img")
    if subtrialcondition=="mmax_window":
        triggerchannel=data.Mmax.times
    else:
        triggerchannel=data.Ds8.times


    paarameter_dictionary={
    "parseddata":data,
    "triggerchannel": triggerchannel,
    "filename": data.info.name,
    "isparsesingle": True,
    "isparsepaired":True,
    "isparsetrans": True,
    "khz_frq":10,
    "userstarttime": i[4],
    "userendtime": i[5],
    "_window_pair":[15,40],
    "_window_single":[200,100],
    "_window_single_trains":[5,25],
    "graphdisplaysettings":{
        "single":[0.01,0.05],
        "double":[0.01,0.05],
        "trains":[0.01,0.05]
        

    },
    "data_file_path":data_file_path,
    "img_path":img_path



    }
    main.extract_evoked_responses(**paarameter_dictionary)
