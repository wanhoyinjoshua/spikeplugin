import pickle
import matplotlib.pyplot as plt
import numpy as np
import spik2py_reflex_plugin
from spik2py_reflex_plugin import main

# Open the pickled file in read-binary mode
with open('C:/Users/wanho/Downloads/test/spikeplugin/extracted_reflexes_data/10/kHz_monophasic/threshold_window/data.pkl', 'rb') as f:
    # Load the list of objects from the pickled file
    
    my_list = pickle.load(f)
print(my_list)
