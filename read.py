import pickle

# Open the pickled file in read-binary mode
with open('C:/Users/wanho/PycharmProjects/spike/extracted_reflexes_data/02_data000_HF_B.pkl', 'rb') as f:
    # Load the list of objects from the pickled file
    my_list = pickle.load(f)

# Print the list of objects
print(my_list)