def parsesingle(x,pre_target_window_ms=200,post_target_window_ms=100,mode="single"):
    import numpy as np
    if isparsesingle==False and (mode=="single"):
        return
    
    

    target = x[1]
    
    left = target - pre_target_window_ms / 1000
    right = post_target_window_ms / 1000 + target
    times = parseddata.Fdi.times

    start_index = np.searchsorted(times, left)
    trigger_index = np.searchsorted(times, target)
    end_index = np.searchsorted(times, right)

    intensity_index = np.searchsorted(parseddata.Stim.times, target)

    # find artifact start time
    skip_artifact_start_time = parseddata.Fdi.times[trigger_index] + 0.005
    artifact_start_index = np.searchsorted(times[trigger_index:end_index], skip_artifact_start_time) + trigger_index
    artifact_end_index = np.searchsorted(times[trigger_index:end_index], skip_artifact_start_time + 0.09) + trigger_index

    # compute baseline SD and average
    tkeo_array = utlis.TEOCONVERT(parseddata.Fdi.values)
    baseline_values = tkeo_array[artifact_start_index:artifact_end_index]
    baseline_sd = np.std(np.abs(baseline_values))
    baseline_avg = np.mean(np.abs(baseline_values))
    
    peak_to_peak, area=compute_outcome_measures.compute_peak2peak_area(parseddata.Fdi.values[artifact_start_index:end_index])

    # compute peak-to-peak and area
    
    # find onset time
    if mode =="single":
        onset_index = compute_outcome_measures.findonset(tkeo_array[trigger_index:end_index], baseline_sd, baseline_avg, artifact_start_index - trigger_index)
    elif mode=="double":
        baseline_values = parseddata.Fdi.values[artifact_start_index:artifact_end_index]
        baseline_sd = np.std(np.abs(baseline_values))
        baseline_avg = np.mean(np.abs(baseline_values))
        onset_index = compute_outcome_measures.findonset(parseddata.Fdi.values[trigger_index:end_index], baseline_sd, baseline_avg, artifact_start_index - trigger_index)
    else:

        onset_index = compute_outcome_measures.findonset(tkeo_array[trigger_index:end_index], baseline_sd, baseline_avg, artifact_start_index - trigger_index)

    if onset_index is not None:
        onset_time = parseddata.Fdi.times[onset_index + trigger_index]
        relative_time = onset_time - parseddata.Fdi.times[trigger_index]
    else:
        onset_time = None
        relative_time = None

    # create SinglePulse object
    data = SinglePulse(
        "singlepulse",
        parseddata.Fdi.values[start_index:end_index],
        start_index,
        end_index,
        relative_time,
        onset_time,
        peak_to_peak,
        area,
        0,
        parseddata.Stim.values[intensity_index],
        trigger_index
    )

    return data



import numpy as np




    
    

def parsepaired(x):
    
    import numpy as np
    if isparsepaired==False:
        return
    

    target1 = x[1]
    print(x)
    target2=x[2]
    
    FDI = parseddata.Fdi.values
    time = parseddata.Fdi.times
    left = target1 - 200 / 1000
    right = 60 / 1000 + target2
    startindex = np.searchsorted(time, left)
    endindex = np.searchsorted(time, right)


    firstpulse=parsesingle([0,target1],15,40,"double")
    secondpulse=parsesingle([0,target2],15,40,"double")
    print(f"this is {firstpulse}")
    print(target1)
    arearatio=firstpulse.area/secondpulse.area
    p2pratio=firstpulse.peak_to_peak/secondpulse.peak_to_peak
    #pretarget will be 0.02s ~15ms 
    #post target  will be ~40ms 
    
    
    data = PairedPulse(
        "pairedpulse",
        FDI[startindex:endindex],
        firstpulse.waveform,
        secondpulse.waveform,
        firstpulse.startindex,
        firstpulse.endindex,
        secondpulse.startindex,
        secondpulse.endindex,
        firstpulse.triggerindex,
        secondpulse.triggerindex,
        firstpulse.relativeonset,
        firstpulse.onset,
        secondpulse.relativeonset,
        secondpulse.onset,
        firstpulse.peak_to_peak,
        secondpulse.peak_to_peak,
        firstpulse.area,
        secondpulse.area,
        0,
        0,
        firstpulse.intensity,
        firstpulse.triggerindex,
        p2pratio,
        arearatio
    )

    
    
    return data




def parsetrans(x):
    import numpy as np
    if isparsetrans==False:
        return
    
    target = x[1]
    pulse=parsesingle([0,target],5,25,"trains")
    
    
    
    times = parseddata.Fdi.times
    
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

