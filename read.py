import pickle
import matplotlib.pyplot as plt
import numpy as np
import spike2py_extract_pulses_plugin
from spike2py_extract_pulses_plugin import main

# Open the pickled file in read-binary mode
with open('C:/Users/wanho/Downloads/test/spikeplugin/extracted_reflexes_data/10/kHz_monophasic/threshold_window_10_DATA001_H_M/data.pkl', 'rb') as f:
    # Load the list of objects from the pickled file
    
    my_list = pickle.load(f)
print(len(my_list["individual"]))

for i in my_list["individual"]:
    print(len(i))
    print(i[0].intensity)

print (my_list["grouped"] )

