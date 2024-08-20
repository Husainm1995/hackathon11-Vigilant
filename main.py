import pickle

def load_object(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# Vulnerable code: Unrestricted pickle deserialization
#adding comment line
user_data = load_object('user_input.pkl')