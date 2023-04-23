import pickle
import matplotlib.pyplot as plt
import numpy as np
import time

# Open the pickled file in read-binary mode
with open('C:/Users/wanho/Downloads/test/spikeplugin/extracted_reflexes_data/10/kHz_monophasic/doubles_105_threshold_window_10_DATA001_H_M/data.pkl', 'rb') as f:
    # Load the list of objects from the pickled file
    my_list = pickle.load(f)
print(len(my_list["individual"]))


def plot_diff_intensity(my_list):
    singleintensity = [round(i.intensity) for i in my_list if i.name == "singlepulse"]
    pariedintensity = [round(i.intensity)  for i in my_list if i.name == "pairedpulse"]
    single_trans_intensity = [round(i.intensity)  for i in my_list if i.name == "single_trans_pulse"]
    print([list(set(singleintensity)),list(set(pariedintensity)),list(set(single_trans_intensity))])
    #need a list of waveforms to correspond with a list of intensity s, {{122,,,d,}} to [1,2,]
    intensitylist=[]
    for index,i in enumerate([list(set(singleintensity)),list(set(pariedintensity)),list(set(single_trans_intensity))]):
        print('hi')
        if index==0:
            name="singlepulse"
        elif index==1:
            name="pairedpulse"

        elif index==2:
            name="single_trans_pulse"

        for intensityvalue in i:
            filtered_list = [obj.waveform for obj in my_list if obj.name == name and round(obj.intensity) == intensityvalue]
            intensitylist.append((intensityvalue,filtered_list,index))

    print (len(intensitylist))
    
    fig1single, ax1 = plt.subplots(nrows=len(list(set(singleintensity))) if len(list(set(singleintensity))) > 0 else 1, ncols=1)
    
    fig2paried, ax2 = plt.subplots(nrows=len(list(set(pariedintensity))) if len(list(set(pariedintensity))) > 0 else 1,ncols=1)
    
    fig3single_trans, ax3 = plt.subplots(nrows=len(list(set(single_trans_intensity))) if len(list(set(single_trans_intensity))) > 0 else 1, ncols=1)
    intensitylist = [l for l in intensitylist if l]
    for ppindex,pp in enumerate(intensitylist):
        if pp[2]==0:
            #single
            for i,wave in enumerate(pp[1]):

                ax1[ppindex].plot(wave)
                ax1[ppindex].set_title(f" {pp[0]}",loc="right")
                
                
               
        elif pp[2]==1:
            #paried
            for i,wave in enumerate(pp[1]):

                ax2[ppindex].plot(wave)
                ax2[ppindex].set_title(f" {pp[0]}",loc="right")
                
               
        elif pp[2]==2:
                #trans
            for i,wave in enumerate(pp[1]):

                ax3[ppindex].plot(wave)
                ax3[ppindex].set_title(f" {pp[0]}",loc="right")
                
                

    
    plt.savefig("C:/Users/wanho/Downloads/test/spikeplugin/testimag.png",dpi = 300,orientation='landscape')
  
   
   


def plotavgwaveform(my_list):
    waveformlist=[]
    for item in my_list:
        waveformlist.append(np.array(item.waveform))
        print(len(np.array(item.waveform)))
        
        
    t_elasped=0.3
    timeaxis = np.linspace(0,  t_elasped, num=len(waveformlist[0]))
    min = min([len(arr) for arr in waveformlist])
    cropped_arr_list = [arr[:min] for arr in waveformlist]
    avg = np.mean(cropped_arr_list , axis=0) 
    plt.plot(timeaxis, avg)
    plt.show()
    # Print the list of objects
    
