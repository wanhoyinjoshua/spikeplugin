from spik2py_reflex_plugin import compute_outcome_measures,graphgenerator
from spik2py_reflex_plugin.helper_functions import signal_cleaning, trains_extraction
from spik2py_reflex_plugin import utlis
from dataclasses import dataclass
@dataclass
class SinglePulse:
    name:str
    waveform: list
    startindex:int
    endindex:int
    relativeonset:int
    onset:float
    peak_to_peak: float
    area: float
    rms:float
    intensity:float
    triggerindex:int

@dataclass
class PairedPulse:
    name:str
    waveform:list
    waveform1: list
    waveform2:list
    startindex1:int
    endindex1:int
    startindex2:int
    endindex2:int
    trigger1index:int
    trigger2index:int
    relativeonset1:int
    
    onset1:float
    relativeonset2:int
    onset2:float
    peak_to_peak1: float
    peak_to_peak2:float
    area1: float
    area2:float
    rms1:float
    rms2:float
    intensity:float
    triggerindex:int
    peak_to_peak_ratio:float
    area_ratio:float

@dataclass
class SingleTransPulse:
    name:str
    waveform: list
    startindex:int
    endindex:int
    relativeonset:int
    onset:float
    peak_to_peak: float
    area: float
    rms:float
    intensity:float
    triggerindex:int
    

class Parse:
    """no documentation yet"""
    def __init__(self,singlepre,singlepost,doublepre,doublepost,trainspre,trainspost,trial,mode):
        self.single_pre=singlepre
        self.single_post=singlepost
        self.double_pre=doublepre
        self.double_post= doublepost
        self.trains_pre= trainspre
        self.trains_post=trainspost
        self.trial=trial
        self.mode=mode
        
    
    def parsesingle(self,trigger):
        import numpy as np
        
        
        

        target = trigger[1]
        
        left = target - self.single_pre/ 1000
        right = self.single_post / 1000 + target
        times = self.trial.Fdi.times

        start_index = np.searchsorted(times, left)
        trigger_index = np.searchsorted(times, target)
        end_index = np.searchsorted(times, right)

        intensity_index = np.searchsorted(self.trial.Stim.times, target)

        # find artifact start time
        skip_artifact_start_time = self.trial.Fdi.times[trigger_index] + 0.005
        artifact_start_index = np.searchsorted(times[trigger_index:end_index], skip_artifact_start_time) + trigger_index
        artifact_end_index = np.searchsorted(times[trigger_index:end_index], skip_artifact_start_time + 0.09) + trigger_index

        # compute baseline SD and average
        tkeo_array = utlis.TEOCONVERT(self.trial.Fdi.values)
        baseline_values = tkeo_array[artifact_start_index:artifact_end_index]
        baseline_sd = np.std(np.abs(baseline_values))
        baseline_avg = np.mean(np.abs(baseline_values))
        
        peak_to_peak, area=compute_outcome_measures.compute_peak2peak_area(self.trial.Fdi.values[artifact_start_index:end_index])

        # compute peak-to-peak and area
       
        # find onset time
        if self.mode =="single":
            onset_index = compute_outcome_measures.findonset(tkeo_array[trigger_index:end_index], baseline_sd, baseline_avg, artifact_start_index - trigger_index)
        elif self.mode=="double":
            baseline_values = self.trial.Fdi.values[artifact_start_index:artifact_end_index]
            baseline_sd = np.std(np.abs(baseline_values))
            baseline_avg = np.mean(np.abs(baseline_values))
            onset_index = compute_outcome_measures.findonset(self.trial.Fdi.values[trigger_index:end_index], baseline_sd, baseline_avg, artifact_start_index - trigger_index)
        else:

            onset_index = compute_outcome_measures.findonset(tkeo_array[trigger_index:end_index], baseline_sd, baseline_avg, artifact_start_index - trigger_index)

        if onset_index is not None:
            onset_time = self.trial.Fdi.times[onset_index + trigger_index]
            relative_time = onset_time - self.trial.Fdi.times[trigger_index]
        else:
            onset_time = None
            relative_time = None

        # create SinglePulse object
        data = SinglePulse(
            "singlepulse",
            self.trial.Fdi.values[start_index:end_index],
            start_index,
            end_index,
            relative_time,
            onset_time,
            peak_to_peak,
            area,
            0,
            self.trial.Stim.values[intensity_index],
            trigger_index
        )

        return data


    def parsetrans(self,trigger):
        import numpy as np
        
        
        
        pulse=self.parsesingle(trigger)
      
        
      
       
       
        data = SingleTransPulse(
        "single_trans_pulse",
        pulse.waveform,
        pulse.startindex,
        pulse.endindex,
        pulse.relativeonset,
        pulse.onset,
        pulse.peak_to_peak,
        pulse.area,
        0,
        pulse.intensity,
        pulse.triggerindex
    )

        
        return data
    

