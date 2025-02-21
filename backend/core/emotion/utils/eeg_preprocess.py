import pickle

def load_model():
    with open(r'C:\Users\Mayank\eeg_project\backend\core\emotion\utils\eeg_movement_classifier.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()  
