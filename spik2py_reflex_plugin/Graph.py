import matplotlib.pyplot as plt
import numpy as np
class Graph:
    def __init__(self,trial,parsedresults,triggercleaned,triggeruncleaned,range,filepath):
        self.trial=trial
        self.results= parsedresults
        self.triggercleaned=triggercleaned
        self.triggeruncleaned=triggeruncleaned
        self.userstarttime= range["userstarttime"]
        self.userendtime= range["userendtime"]
        self.filepath=filepath


        
    def generate_individual_graph(self):
    
        fig, (ax1, ax2,ax5,ax4) = plt.subplots(4, 1, sharex=True,figsize=(10, 6))
        ax1.eventplot(self.triggercleaned, orientation='horizontal', colors='g')
        ax2.eventplot(self.triggeruncleaned, orientation='horizontal', colors='r')
        
        
        ax4.plot(self.trial.Fdi.times,self.trial.Fdi.values)
        
        ax5.plot(self.trial.Stim.times,self.trial.Stim.values)
        
    
        plt.xlim(self.userstarttime, self.userendtime)
        
        plt.ylim(-1,1)
        #fig.text(0.5, 0.95, f"{filedataname}", ha='center', va='top')
        #plt.show()
        
        plt.savefig(self.filepath,dpi = 300,orientation='landscape')
        
       
        gg=fig.text(0.5, 0.95, f"hi", ha='center', va='top')
        gg.remove()

        for i , x in enumerate(self.results):
            if  x.name=="singlepulse":
                ymax= np.max(np.array(self.trial.Fdi.values[x.triggerindex:x.endindex]))
                ymin= np.min(np.array(self.trial.Fdi.values[x.triggerindex:x.endindex]))
                y_range = ymax - ymin
               
                plt.xlim([self.trial.Fdi.times[x.triggerindex],  self.trial.Fdi.times[x.endindex]])
                text1 = fig.text(0.5, 0.95, f"hi", ha='center', va='top')
                text2 = fig.text(0.9, 0.90, f"Onset:{round(x.relativeonset, 2)}" if x.onset is not None else "", ha='center', va='top')
                text3 = fig.text(0.9, 0.80, f"Area:{round(x.area, 2)}" if x.area is not None else "", ha='center', va='top')
                text4 = fig.text(0.9, 0.70, f"peak to peak:{round(x.peak_to_peak, 2)}" if x.peak_to_peak is not None else "", ha='center', va='top')

                
                plt.ylim([ymin - 0.1*y_range,ymax +0.1*y_range])
                fig.text(0.5, 0.95, "hi", ha='center', va='top')
                
                
                

                plt.savefig(f"{self.filepath}_{i}.png",dpi = 300,orientation='landscape')
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
                """
                
                ymax= np.max(np.array(self.trial.Fdi.values[x.triggerindex:x.endindex2]))
                ymin= np.min(np.array(self.trial.Fdi.values[x.triggerindex:x.endindex2]))
                print(ymax)
                print(ymin)
                y_range = ymax - ymin
                plt.xlim([self.trial.Fdi.times[x.triggerindex],  self.trial.Fdi.times[x.endindex2]+posttriggerdouble])
                
                plt.ylim([ymin - 0.1*y_range,ymax +0.1*y_range])
                text1 = fig.text(0.5, 0.95, f"hi", ha='center', va='top')
                text2 = fig.text(0.5, 0.90, f"Onset1: {round(x.relativeonset1, 2) if x.onset1 is not None else ''}", ha='center', va='top')
                text3 = fig.text(0.5, 0.80, f"Onset2: {round(x.relativeonset2, 2) if x.onset2 is not None else ''}", ha='center', va='top')
                text4 = fig.text(0.9, 0.90, f"Area1: {round(x.area1, 2) if x.area1 is not None else ''}", ha='center', va='top')
                text5 = fig.text(0.9, 0.80, f"Area2: {round(x.area2, 2) if x.area2 is not None else ''}", ha='center', va='top')
                text6 = fig.text(0.9, 0.70, f"Peak to peak1: {round(x.peak_to_peak1, 2) if x.peak_to_peak1 is not None else ''}", ha='center', va='top')
                text7 = fig.text(0.9, 0.60, f"Peak to peak2: {round(x.peak_to_peak2, 2) if x.peak_to_peak2 is not None else ''}", ha='center', va='top')
                text8 = fig.text(0.9, 0.50, f"Peak to peak ratio: {round(x.peak_to_peak_ratio, 2) if x.peak_to_peak2 is not None else ''}", ha='center', va='top')
                text9 = fig.text(0.9, 0.40, f"area ratio: {round(x.area_ratio, 2) if x.peak_to_peak2 is not None else ''}", ha='center', va='top')

                
                plt.savefig(f"{self.filepath}_{i}.png",dpi = 300,orientation='landscape')
                text_objects = [text1, text2,text3, text4,text5,text6,text7,text8,text9]

                # remove the text objects
                for text_obj in text_objects:
                    text_obj.remove()
            
            
            
            #ax4.vlines(x=list(filter(lambda x: x is not None, masteronset)), ymin=ax4.get_ylim()[0], ymax=ax4.get_ylim()[1], colors='red', ls=':', lw=1, label='vline_single - full height')
        
"""
            
            