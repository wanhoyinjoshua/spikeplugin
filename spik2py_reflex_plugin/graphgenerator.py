import matplotlib.pyplot as plt
import time
from spik2py_reflex_plugin import compute_outcome_measures

import numpy as np
from spik2py_reflex_plugin import utlis

def generate_grouped_avg_graph_pickled(my_list,file_path,t_elasped_single=0.3,t_elasped_double_single=0.045,t_elasped_trains=0.03,pretriggersingle=0.01,posttriggersingle=0.05,pretriggerdouble=0.01,posttriggerdouble= 0.05 ):

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
            #filtered_list = [obj.waveform for obj in my_list if obj.name == name and round(obj.intensity) == intensityvalue]
            filtered_list=[]
            for obj in my_list:
                if obj.name == name and round(obj.intensity) == intensityvalue:
                    if obj.name=="pairedpulse":
                        filtered_list.append((obj.waveform1,obj.waveform2,obj.waveform,obj.trigger1index))
                    else:
                        filtered_list.append(obj.waveform)



            intensitylist.append((intensityvalue,filtered_list,index))

    print (len(intensitylist))
    
    fig1single, ax1 = plt.subplots(nrows=len(list(set(singleintensity))) if len(list(set(singleintensity))) > 0 else 1, ncols=1,sharey=True,sharex=True)
    
    fig1single.suptitle('single')
    fig2paried, ax2 = plt.subplots(nrows=len(list(set(pariedintensity))) if len(list(set(pariedintensity))) > 0 else 1,ncols=2,sharey=True,sharex=True)
    print(len(list(set(pariedintensity))))
    fig2paried.suptitle('paired')
    fig3single_trans, ax3 = plt.subplots(nrows=len(list(set(single_trans_intensity))) if len(list(set(single_trans_intensity))) > 0 else 1, ncols=1,sharey=True,sharex=True)
    fig3single_trans.suptitle('singletrans')
    
    intensitylist = [l for l in intensitylist if l]
    
    intensity_grouped_outcome_list=[]
    for ppindex,pp in enumerate(intensitylist):
        
        if pp[2]==0:
            #single
            allwaveforms=[]
            
            t_elasped=t_elasped_single
            
            for i,wave in enumerate(pp[1]):
                allwaveforms.append(wave)
                t_elasped=t_elasped_single
                timeaxis = np.linspace(0,  t_elasped, num=len(wave))
                x_new = timeaxis 
                try:
                    ax1[ppindex].plot(x_new,wave,color=(0.8, 0.8, 0.8))
                    
                    ax1[ppindex].text(0.95, 0.95, f" {pp[0]}", transform=ax1[ppindex].transAxes, ha='right', va='top')
                except:
                    ax1.plot(x_new,wave)
                    ax1.text(0.95, 0.95, f" {pp[0]}", transform=ax1.transAxes, ha='right', va='top')
            
            max_len = max(len(arr) for arr in allwaveforms)
            print(max_len)
            # Resize the arrays to have the same shape
            def artifactstart(element,artifacttime):
                return element >=artifacttime
            resized_list = [np.resize(arr, (max_len,)) for arr in allwaveforms]
            avg_arr = np.mean(resized_list, axis=0)
            ##now have to conmvert this avg _arr to the energy array 
            print(avg_arr)
            TKEOarray= utlis.TEOCONVERT(avg_arr)
            
            ##all the index should stay the same 

            timeaxis = np.linspace(0,  t_elasped, num=len(TKEOarray))
            ##i need trigger index, 
            print(timeaxis)
            triggerindex = np.where(timeaxis >= 0.2)[0][0]
            
            #endbaseline 0.3-0.06
            skipartifactstarttime= 0.01+0.2
            #endbaselineindex=next((i for i, elem in enumerate(timeaxis) if artifactstart(elem,skipartifactstarttime+0.09)), None)
            artifactsrtaindex= next((i for i, elem in enumerate(timeaxis) if artifactstart(elem,skipartifactstarttime)), None)
            artidactendindex=next((i for i, elem in enumerate(timeaxis) if artifactstart(elem,skipartifactstarttime+0.09)), None)
            baselinesd= np.std([abs(num) for num in TKEOarray[artifactsrtaindex:artidactendindex]])
            baselineavg=np.average([abs(num) for num in TKEOarray[artifactsrtaindex:artidactendindex]])
            #baselinesdold= np.std([abs(num) for num in TKEOarray[0:triggerindex]])
            #baselineavg=np.average([abs(num) for num in TKEOarray[0:triggerindex]])
            onsetindex=compute_outcome_measures.findonset(TKEOarray[triggerindex:],baselinesd,baselineavg,artifactsrtaindex-triggerindex,1,5)
            try:
                onsetime=timeaxis[onsetindex+triggerindex]-timeaxis[triggerindex]
            except:
                onsetime=None
            peak2peak,area=compute_outcome_measures.compute_peak2peak_area(avg_arr[artifactsrtaindex:])
            dataobject={"type":"single_pulse","intensity":pp[0],"avg_onset":onsetime,"avg_peak2peak":peak2peak,"avg_area":area}
            intensity_grouped_outcome_list.append(dataobject)

            try:
                ax1[ppindex].plot(timeaxis,avg_arr,color="red")
                #ax1[ppindex].plot(timeaxis,TKEOarray,color="green")
                try:
                    ax1[ppindex].axvline(x=timeaxis[onsetindex+triggerindex], color='blue')
                except:
                    pass
                ax1[ppindex].set_xlim(0.2-0.005, 0.25)
    
                
                
            except:
                ax1.plot(timeaxis,avg_arr,color="red")
                #ax1[ppindex].plot(timeaxis,TKEOarray,color="green")
                
                ax1.set_xlim(0.2-0.005, 0.25)
    
            
        elif pp[2]==1:
            #paried
            allwaveform1=[]
            allwaveform2=[]
            allbaselinewaveform=[]
            for i,wave in enumerate(pp[1]):
                allwaveform1.append(wave[0])
                allwaveform2.append(wave[1])
                baseline=wave[2][0:wave[3]]
                allbaselinewaveform.append(baseline)
                pulse1= wave[0]
                pulse2=wave[1]
               
                t_elasped=t_elasped_double_single
                timeaxis1 = np.linspace(0,  t_elasped, num=len(pulse1))
                timeaxis2= np.linspace(0,  t_elasped, num=len(pulse2))
                
                
                try:
                    if ppindex==0:
                        ppindex=ppindex
                    else:
                        ppindex=ppindex*2
                        
                    ax2[ppindex].plot(timeaxis1,pulse1,color=(0.8, 0.8, 0.8))
                    ax2[ppindex+1].plot(timeaxis2,pulse2,color=(0.8, 0.8, 0.8))
                    #ax2[ppindex][0].plot(x_new,TKEOarray,color="green")
                    ax2[ppindex].text(0.95, 0.95, f" {pp[0]}", transform=ax2[ppindex].transAxes, ha='right', va='top')
                except:
                    ax2[0].plot(timeaxis1,pulse1,color=(0.8, 0.8, 0.8))
                    ax2[1].plot(timeaxis2,pulse2,color=(0.8, 0.8, 0.8))
                    ax2[0].text(0.95, 0.95, f" {pp[0]}", transform=ax2[ppindex].transAxes, ha='right', va='top')
            
            max_len1 = max(len(arr) for arr in allwaveform1)
            max_len2 = max(len(arr) for arr in allwaveform2)
            
            
            # Resize the arrays to have the same shape
            def artifactstart(element,artifacttime):
                return element >=artifacttime
            resized_list1 = [np.resize(arr, (max_len1,)) for arr in allwaveform1]
            resized_list2 = [np.resize(arr, (max_len2,)) for arr in allwaveform2]
            resized_baseline = [np.resize(arr, (max_len2,)) for arr in allbaselinewaveform]
            avg_arr1 = np.mean(resized_list1, axis=0)
            timeaxisnew1 = np.linspace(0,  t_elasped, num=len(avg_arr1))
            avg_arr2 = np.mean(resized_list2, axis=0)
            timeaxisnew2 = np.linspace(0,  t_elasped, num=len(avg_arr2))
            avg_baseline=np.mean(resized_baseline, axis=0)
            baselinesd= np.std([abs(num) for num in avg_baseline])
            baselineavg=np.average([abs(num) for num in avg_baseline])
            skipartifactstarttime= 0.01
            artifactsrtaindex1= next((i for i, elem in enumerate(timeaxisnew1) if artifactstart(elem,skipartifactstarttime)), None)
            print(artifactsrtaindex1)
            
            endartifactsrtaindex1= next((i for i, elem in enumerate(timeaxisnew1) if artifactstart(elem,skipartifactstarttime+0.005)), None)
            artifactsrtaindex2= next((i for i, elem in enumerate(timeaxisnew2) if artifactstart(elem,skipartifactstarttime)), None)
            endartifactsrtaindex2= next((i for i, elem in enumerate(timeaxisnew2) if artifactstart(elem,skipartifactstarttime+0.005)), None)
            TKEOarray1= utlis.TEOCONVERT(avg_arr1)
            TKEOarray2= utlis.TEOCONVERT(avg_arr2)

            baselinesd1= np.std([abs(num) for num in TKEOarray1[artifactsrtaindex1:endartifactsrtaindex1]])
            baselineavg1=np.average([abs(num) for num in TKEOarray1[artifactsrtaindex1:endartifactsrtaindex1]])

            baselinesd2= np.std([abs(num) for num in TKEOarray2[artifactsrtaindex2:endartifactsrtaindex2]])
            baselineavg2=np.average([abs(num) for num in TKEOarray2[artifactsrtaindex2:endartifactsrtaindex2]])
            
            ##all the index should stay the same 

            timeaxisnew1 = np.linspace(0,  t_elasped, num=len(avg_arr1))
            timeaxisnew2 = np.linspace(0,  t_elasped, num=len(avg_arr2))
            onsetindex1=compute_outcome_measures.findonset(avg_arr1,baselinesd,baselineavg,artifactsrtaindex1,2,5)
            onsetindex2=compute_outcome_measures.findonset(avg_arr2,baselinesd,baselineavg,artifactsrtaindex2,2,5)
            
            onsettime1=timeaxisnew1[onsetindex1]
            onsettime2=timeaxisnew2[onsetindex2]
            peak2peak1,area1=compute_outcome_measures.compute_peak2peak_area(avg_arr1[artifactsrtaindex1:])
            peak2peak2,area2=compute_outcome_measures.compute_peak2peak_area(avg_arr2[artifactsrtaindex2:])
            peak_to_peak_ratio=peak2peak1/peak2peak2
            area_ratio=area1/area2
            ##need to find the ratio between areas, and peak to peak.
            dataobject={"type":"paired_pulse","intensity":pp[0],"avg_onset1":onsettime1,"avg_onset2":onsettime2,"avg_peak_to_peak1":peak2peak1,"avg_area1":area1,"avg_peak_to_peak2":peak2peak2,"avg_area2":area2,"peak_to_peak_ratio":peak_to_peak_ratio,"area_ratio":area_ratio}
            intensity_grouped_outcome_list.append(dataobject)

            try:
                ax2[ppindex].plot(timeaxisnew1,avg_arr1,color="red")
                ax2[ppindex+1].plot(timeaxisnew2,avg_arr2,color="red")
                #ax1[ppindex].plot(timeaxis,TKEOarray,color="green")
                
                ax2[ppindex+1].axvline(x=timeaxisnew2[onsetindex2], color='blue')

                
                ax2[ppindex].axvline(x=timeaxisnew1[onsetindex1], color='blue')
                ax2[ppindex+1].axvline(x=timeaxisnew2[onsetindex2], color='blue')
                #ax2[ppindex].set_xlim(0.2-0.005, 0.25)
    
                
                
            except:
                ax2[0].plot(timeaxisnew1,avg_arr1,color="red")
                ax2[1].plot(timeaxisnew2,avg_arr2,color="red")
                try:
                    ax2[0].axvline(x=timeaxisnew1[onsetindex1], color='blue')
                except:
                    pass

            
            
                
                try:
                    ax2[1].axvline(x=timeaxisnew2[onsetindex2], color='blue')
                except:
                    pass
                
                    
                
                #ax1[ppindex].plot(timeaxis,TKEOarray,color="green")
                
                
                
            
        elif pp[2]==2:
                #trans
            allwaveforms=[]
            t_elasped= t_elasped_trains
            
            for i,wave in enumerate(pp[1]):
                allwaveforms.append(wave)
                
                timeaxis = np.linspace(0,  t_elasped, num=len(wave))
                x_new=timeaxis
                
                try:
                    ax3[ppindex].plot(x_new,wave,color=(0.8, 0.8, 0.8))
                    
                    ax3[ppindex].text(0.95, 0.95, f" {pp[0]}", transform=ax3[ppindex].transAxes, ha='right', va='top')
                except:
                    ax3.plot(x_new,wave,color=(0.8, 0.8, 0.8))
                
                    ax3.text(0.95, 0.95, f" {pp[0]}", transform=ax3[ppindex].transAxes, ha='right', va='top')
            max_len = max(len(arr) for arr in allwaveforms)
            print(max_len)
        
            
            
            # Resize the arrays to have the same shape
            
            def artifactstart(element,artifacttime):
                return element >=artifacttime
            resized_list = [np.resize(arr, (max_len,)) for arr in allwaveforms]
            avg_arr = np.mean(resized_list, axis=0)
            timeaxis = np.linspace(0,  t_elasped, num=len(avg_arr))
            ##i need trigger index, 
            TKEOarray= utlis.TEOCONVERT(avg_arr)
            triggerindex = np.where(timeaxis >= 0.005)[0][0]
            baselinesd= np.std([abs(num) for num in TKEOarray[0:triggerindex]])
            baselineavg=np.average([abs(num) for num in TKEOarray[0:triggerindex]])
            skipartifactstarttime= 0.01+0.005
            artifactsrtaindex= next((i for i, elem in enumerate(timeaxis) if artifactstart(elem,skipartifactstarttime)), None)
            
            onsetindex=compute_outcome_measures.findonset(TKEOarray[triggerindex:],baselinesd,baselineavg,artifactsrtaindex-triggerindex)
            try:
                onsettime=timeaxis[onsetindex+triggerindex]-timeaxis[triggerindex]
            except:
                onsettime=None
            peak2peak,area=compute_outcome_measures.compute_peak2peak_area(avg_arr[artifactsrtaindex:])
            dataobject={"type":"trans_single_pulse","intensity":pp[0],"avg_onset":onsettime,"avg_peak2peak":peak2peak,"avg_area":area}
            intensity_grouped_outcome_list.append(dataobject)
            #onsetindex=compute_outcome_measures.wavelet_onset_detection(np.array(avg_arr[triggerindex:]),'sym4',4,3,artifactsrtaindex)
            try:
                ax3[ppindex].plot(timeaxis,avg_arr,color="red")
                ax3[ppindex].axvline(x=timeaxis[onsetindex+triggerindex], color='blue')
                #ax3[ppindex].plot(timeaxis,TKEOarray,color="green")
                
            except:
                ax3[ppindex].plot(timeaxis,avg_arr,color="red")
                #ax3[ppindex].plot(timeaxis,TKEOarray,color="green")
                
                
    
    fig1single.savefig(f"{file_path}_combined_single.png",orientation='landscape',dpi = 300)
    fig2paried.savefig(f"{file_path}_combined_pairs.png",orientation='landscape',dpi = 300)
    fig3single_trans.savefig(f"{file_path}_combined_single_trans.png",orientation='landscape',dpi = 300)
    
    
    plt.close()
    return intensity_grouped_outcome_list
   
   
    


def generate_individual_graph(triggercleaned, triggeruncleaned, checktrigger, xx1, yy1, parseddata, masterresult, masteronset, userstarttime, userendtime,file_path,pickledtarget,filedataname,pretriggersingle,posttriggersingle,pretriggerdouble,posttriggerdouble):
    
    
    
    #generate the combined one first 
    

    #this is generating the big plot as a big summary
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
    #plt.show()
    
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
            plt.xlim([xx1[x.triggerindex]-pretriggersingle,  parseddata.Fdi.times[x.endindex]+posttriggersingle])
            text1 = fig.text(0.5, 0.95, f"{filedataname}", ha='center', va='top')
            text2 = fig.text(0.9, 0.90, f"Onset:{round(x.relativeonset, 2)}" if x.onset is not None else "", ha='center', va='top')
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
            #disabling the generation of trains_graph
            """
            ymax= np.max(np.array(yy1[x.triggerindex:x.endindex]))
            ymin= np.min(np.array(yy1[x.triggerindex:x.endindex]))
            y_range = ymax - ymin
            print(ymax)
            print(ymin)
            plt.xlim([xx1[x.triggerindex]-0.01,  parseddata.Fdi.times[x.endindex]+0.001])
            
            
            plt.ylim([ymin - 0.1*y_range,ymax +0.1*y_range])
            text1 = fig.text(0.5, 0.95, f"{filedataname}", ha='center', va='top')
            text2 = fig.text(0.9, 0.90, f"Onset:{round(x.relativeonset, 2)}" if x.onset is not None else "", ha='center', va='top')
            text3 = fig.text(0.9, 0.80, f"Area:{round(x.area, 2)}" if x.area is not None else "", ha='center', va='top')
            text4 = fig.text(0.9, 0.70, f"peak to peak:{round(x.peak_to_peak, 2)}" if x.peak_to_peak is not None else "", ha='center', va='top')
                
            plt.savefig(f"{file_path}_{i}.png",dpi = 300,orientation='landscape')
            text_objects = [text1, text2,text3, text4]

            # remove the text objects
            for text_obj in text_objects:
                text_obj.remove()
            """


        else:
            pass
            ymax= np.max(np.array(yy1[x.triggerindex:x.endindex2]))
            ymin= np.min(np.array(yy1[x.triggerindex:x.endindex2]))
            print(ymax)
            print(ymin)
            y_range = ymax - ymin
            plt.xlim([xx1[x.triggerindex]-pretriggerdouble,  parseddata.Fdi.times[x.endindex2]+posttriggerdouble])
            
            plt.ylim([ymin - 0.1*y_range,ymax +0.1*y_range])
            text1 = fig.text(0.5, 0.95, f"{filedataname}", ha='center', va='top')
            text2 = fig.text(0.5, 0.90, f"Onset1: {round(x.relativeonset1, 2) if x.onset1 is not None else ''}", ha='center', va='top')
            text3 = fig.text(0.5, 0.80, f"Onset2: {round(x.relativeonset2, 2) if x.onset2 is not None else ''}", ha='center', va='top')
            text4 = fig.text(0.9, 0.90, f"Area1: {round(x.area1, 2) if x.area1 is not None else ''}", ha='center', va='top')
            text5 = fig.text(0.9, 0.80, f"Area2: {round(x.area2, 2) if x.area2 is not None else ''}", ha='center', va='top')
            text6 = fig.text(0.9, 0.70, f"Peak to peak1: {round(x.peak_to_peak1, 2) if x.peak_to_peak1 is not None else ''}", ha='center', va='top')
            text7 = fig.text(0.9, 0.60, f"Peak to peak2: {round(x.peak_to_peak2, 2) if x.peak_to_peak2 is not None else ''}", ha='center', va='top')
            text8 = fig.text(0.9, 0.50, f"Peak to peak ratio: {round(x.peak_to_peak_ratio, 2) if x.peak_to_peak2 is not None else ''}", ha='center', va='top')
            text9 = fig.text(0.9, 0.40, f"area ratio: {round(x.area_ratio, 2) if x.peak_to_peak2 is not None else ''}", ha='center', va='top')

            
            plt.savefig(f"{file_path}_{i}.png",dpi = 300,orientation='landscape')
            text_objects = [text1, text2,text3, text4,text5,text6,text7,text8,text9]

            # remove the text objects
            for text_obj in text_objects:
                text_obj.remove()
       
        
    

    
       
    