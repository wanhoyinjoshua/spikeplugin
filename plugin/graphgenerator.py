import matplotlib.pyplot as plt
import time
import numpy as np
def generate_graph(triggercleaned, triggeruncleaned, checktrigger, xx1, yy1, parseddata, masterresult, masteronset, userstarttime, userendtime,file_path,pickledtarget,filedataname):
    print(pickledtarget)
    
    
    #generate the combined one first 
    def plot_diff_intensity(my_list,file_path):
        singleintensity = [round(i.intensity) for i in my_list if i.name == "singlepulse"]
        pariedintensity = [round(i.intensity)  for i in my_list if i.name == "pairedpulse"]
        single_trans_intensity = [round(i.intensity)  for i in my_list if i.name == "single_trans_pulse"]
        cleanedsingle=list(set(singleintensity))
        cleanedpaired=list(set(pariedintensity))
        cleanedtrans=list(set(single_trans_intensity))
        def sorting (list):


            if len(list) == 0:
                return list
            else:
                newlist=sorted(list)
                return newlist
        
        
        #need a list of waveforms to correspond with a list of intensity s, {{122,,,d,}} to [1,2,]
        intensitylist=[]
        for index,i in enumerate([sorting(cleanedsingle),sorting(cleanedpaired),sorting(cleanedtrans)]):
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
        
        fig1single, ax1 = plt.subplots(nrows=len(list(set(singleintensity))) if len(list(set(singleintensity))) > 0 else 1, ncols=1,sharey=True)
        fig1single.suptitle('single')
        fig2paried, ax2 = plt.subplots(nrows=len(list(set(pariedintensity))) if len(list(set(pariedintensity))) > 0 else 1,ncols=1,sharey=True)
        print(len(list(set(pariedintensity))))
        fig2paried.suptitle('paired')
        fig3single_trans, ax3 = plt.subplots(nrows=len(list(set(single_trans_intensity))) if len(list(set(single_trans_intensity))) > 0 else 1, ncols=1,sharey=True)
        fig3single_trans.suptitle('singletrans')
        intensitylist = [l for l in intensitylist if l]
       
       
        for ppindex,pp in enumerate(intensitylist):
            if pp[2]==0:
                #single
                for i,wave in enumerate(pp[1]):
                    t_elasped=0.3
                    timeaxis = np.linspace(0,  t_elasped, num=len(wave))
                    x_new = timeaxis 
                    try:
                        ax1[ppindex].plot(x_new,wave)
                        ax1[ppindex].set_title(f" {pp[0]}",loc="right")
                    except:
                        ax1.plot(x_new,wave)
                        ax1.set_title(f" {pp[0]}",loc="right")

                   
               
            elif pp[2]==1:
                #paried
                for i,wave in enumerate(pp[1]):
                    t_elasped=0.26
                    timeaxis = np.linspace(0,  t_elasped, num=len(wave))
                    x_new=timeaxis
                    try:
                        ax2[ppindex].plot(x_new,wave)
                        ax2[ppindex].set_title(f" {pp[0]}",loc="right")
                    except:
                        ax2.plot(x_new,wave)
                        ax2.set_title(f" {pp[0]}",loc="right")
                    
                
            elif pp[2]==2:
                    #trans
                for i,wave in enumerate(pp[1]):
                    t_elasped=0.03
                    timeaxis = np.linspace(0,  t_elasped, num=len(wave))
                    x_new=timeaxis
                    try:
                        ax3[ppindex].plot(x_new,wave)
                        
                        ax3[ppindex].set_title(f" {pp[0]}",loc="right")
                    except:
                        ax3.plot(x_new,wave)
                    
                        ax3.set_title(f" {pp[0]}",loc="right")
                    
        
        fig1single.savefig(f"{file_path}_combined_single.png",orientation='landscape',dpi = 300)
        fig2paried.savefig(f"{file_path}_combined_pairs.png",orientation='landscape',dpi = 300)
        fig3single_trans.savefig(f"{file_path}_combined_single_trans.png",orientation='landscape',dpi = 300)
        plt.close()
   
    plot_diff_intensity(pickledtarget,file_path)
    


    fig, (ax1, ax2,ax3,ax5,ax4) = plt.subplots(5, 1, sharex=True,figsize=(10, 6))
    ax1.eventplot(triggercleaned, orientation='horizontal', colors='g')
    ax2.eventplot(triggeruncleaned, orientation='horizontal', colors='r')
    ax3.eventplot(checktrigger, orientation='horizontal', colors='y')
    ax4.plot(xx1,yy1)
    ax5.plot(parseddata.Stim.times,parseddata.Stim.values)
    for i,x in enumerate(masterresult):
        ax4.axvspan(xx1[x[0]], parseddata.Fdi.times[x[1]], alpha=0.2, color='gray')
        
   
    plt.xlim(userstarttime, userendtime)
    
    plt.ylim(-1,1)
    fig.text(0.5, 0.95, f"{filedataname}", ha='center', va='top')
    
    
    plt.savefig(file_path,dpi = 300,orientation='landscape')
    print(filedataname)
    gg=fig.text(0.5, 0.95, f"{filedataname}", ha='center', va='top')
    gg.remove()
    
    
    length=len(masteronset)
    ax4.vlines(x=list(filter(lambda x: x is not None, masteronset)), ymin=ax4.get_ylim()[0], ymax=ax4.get_ylim()[1], colors='red', ls=':', lw=1, label='vline_single - full height')
    
  
    for i , x in enumerate(pickledtarget):
        if  x.name=="singlepulse":
            ymax= np.max(np.array(yy1[x.triggerindex:x.endindex]))
            ymin= np.min(np.array(yy1[x.triggerindex:x.endindex]))
            y_range = ymax - ymin
            print(ymax)
            print(ymin)
            plt.xlim([xx1[x.triggerindex]-0.01,  parseddata.Fdi.times[x.endindex]+0.05])
            text1 = fig.text(0.5, 0.95, f"{filedataname}", ha='center', va='top')
            text2 = fig.text(0.9, 0.90, f"Onset:{round(x.onset, 2)}" if x.onset is not None else "", ha='center', va='top')
            text3 = fig.text(0.9, 0.80, f"Area:{round(x.area, 2)}" if x.area is not None else "", ha='center', va='top')
            text4 = fig.text(0.9, 0.70, f"peak to peak:{round(x.peak_to_peak, 2)}" if x.peak_to_peak is not None else "", ha='center', va='top')

            
            plt.ylim([ymin - 0.1*y_range,ymax +0.1*y_range])
            fig.text(0.5, 0.95, filedataname, ha='center', va='top')
           
           
            
    
            plt.savefig(f"{file_path}_{i}.png",dpi = 300,orientation='landscape')
            text_objects = [text1, text2,text3, text4]

# remove the text objects
            for text_obj in text_objects:
                text_obj.remove()

            

        elif x.name=="single_trans_pulse":
            ymax= np.max(np.array(yy1[x.triggerindex:x.endindex]))
            ymin= np.min(np.array(yy1[x.triggerindex:x.endindex]))
            y_range = ymax - ymin
            print(ymax)
            print(ymin)
            plt.xlim([xx1[x.triggerindex]-0.01,  parseddata.Fdi.times[x.endindex]+0.001])
            
            
            plt.ylim([ymin - 0.1*y_range,ymax +0.1*y_range])
            text1 = fig.text(0.5, 0.95, f"{filedataname}", ha='center', va='top')
            text2 = fig.text(0.9, 0.90, f"Onset:{round(x.onset, 2)}" if x.onset is not None else "", ha='center', va='top')
            text3 = fig.text(0.9, 0.80, f"Area:{round(x.area, 2)}" if x.area is not None else "", ha='center', va='top')
            text4 = fig.text(0.9, 0.70, f"peak to peak:{round(x.peak_to_peak, 2)}" if x.peak_to_peak is not None else "", ha='center', va='top')
                
            plt.savefig(f"{file_path}_{i}.png",dpi = 300,orientation='landscape')
            text_objects = [text1, text2,text3, text4]

            # remove the text objects
            for text_obj in text_objects:
                text_obj.remove()


        else:
            ymax= np.max(np.array(yy1[x.triggerindex:x.endindex2]))
            ymin= np.min(np.array(yy1[x.triggerindex:x.endindex2]))
            print(ymax)
            print(ymin)
            y_range = ymax - ymin
            plt.xlim([xx1[x.triggerindex]-0.01,  parseddata.Fdi.times[x.endindex2]+0.05])
            
            plt.ylim([ymin - 0.1*y_range,ymax +0.1*y_range])
            text1 = fig.text(0.5, 0.95, f"{filedataname}", ha='center', va='top')
            text2 = fig.text(0.5, 0.90, f"Onset1: {round(x.onset1, 2) if x.onset1 is not None else ''}", ha='center', va='top')
            text3 = fig.text(0.5, 0.80, f"Onset2: {round(x.onset2, 2) if x.onset2 is not None else ''}", ha='center', va='top')
            text4 = fig.text(0.9, 0.90, f"Area1: {round(x.area1, 2) if x.area1 is not None else ''}", ha='center', va='top')
            text5 = fig.text(0.9, 0.80, f"Area2: {round(x.area2, 2) if x.area2 is not None else ''}", ha='center', va='top')
            text6 = fig.text(0.9, 0.70, f"Peak to peak1: {round(x.peak_to_peak1, 2) if x.peak_to_peak1 is not None else ''}", ha='center', va='top')
            text7 = fig.text(0.9, 0.60, f"Peak to peak2: {round(x.peak_to_peak2, 2) if x.peak_to_peak2 is not None else ''}", ha='center', va='top')

            
            plt.savefig(f"{file_path}_{i}.png",dpi = 300,orientation='landscape')
            text_objects = [text1, text2,text3, text4,text5,text6,text7]

            # remove the text objects
            for text_obj in text_objects:
                text_obj.remove()
       
        
    

    
    plt.close()