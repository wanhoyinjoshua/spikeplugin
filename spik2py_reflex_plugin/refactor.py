from spik2py_reflex_plugin.Userinput import User_Specified_Data
from spik2py_reflex_plugin.Signal_Classifier import Pulse_Classifier
from spik2py_reflex_plugin.Trains_processing import Train_preprocessing
from spik2py_reflex_plugin.Parse_Signals import Parse
from spik2py_reflex_plugin.Graph import Graph
from tqdm import tqdm

from spik2py_reflex_plugin import utlis

import time
def extract_evoked_responses(data,triggerchannel,range,khz_clean,filepath):
    User_Specified_Data= User_Specified_Data(data,triggerchannel,range,khz_clean).extract().remove_khz()
    
    Pre_trains_processing_classidfied_list= Pulse_Classifier(User_Specified_Data,50 / 1000 + 0.01,1/25).classify()
   
    Post_trains_entire_classified_list= Train_preprocessing(data,Pre_trains_processing_classidfied_list,triggerchannel).extract_trains_period().data_removed_trainsblock

  
    

    lookup_table = {
        
        "Single_Pulse": Parse(200,100,15,40,5,25,data,"single").parsesingle,
        "Single_Trains_pulse":Parse(200,100,15,40,5,25,data,"trains").parsetrans
        
    }
    single_pulse_result=[]
    double_pulse_result=[]
    trains_pulse_result=[]

    for trigger in tqdm(Post_trains_entire_classified_list):
            try:
                  
                result=lookup_table[trigger[0]](trigger)
                if result.name=="single_trans_pusle":
                     trains_pulse_result.append(result)
                elif result.name=="singlepulse":
                     single_pulse_result.append(result)
               
                     

            except:
                 pass

    #now try to plot it with a class 
    masterresult=single_pulse_result+double_pulse_result+trains_pulse_result
    Graph(data,masterresult,User_Specified_Data,triggerchannel,range,filepath).generate_individual_graph()
    
    groupedsingle=utlis.Group_Individual_Pulses(single_pulse_result)
    groupedpaired=utlis.Group_Individual_Pulses(double_pulse_result)
    groupedtraains=utlis.Group_Individual_Pulses(trains_pulse_result)
    individualpickled=groupedsingle+groupedpaired+groupedtraains
    print(individualpickled)

        
        
        

        
        
        
       


   
    
    
    
    