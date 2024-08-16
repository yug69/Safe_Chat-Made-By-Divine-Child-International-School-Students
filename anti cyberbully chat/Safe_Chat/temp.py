import pickle

# Path to the uploaded file
file_path = r'C:\Users\neema\Downloads\anti cyberbully chat\anti cyberbully chat\Safe_Chat\tfidf_vector_vocabulary.pkl'

# Load the vocabulary from the .pkl file
with open(file_path, 'rb') as file:
    vocabulary = pickle.load(file)

# Display the vocabulary
print("Vocabulary loaded from the .pkl file:")
print(vocabulary)
