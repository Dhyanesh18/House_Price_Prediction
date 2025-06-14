import os
import pickle
import json
import numpy as np

__locations = None
__data_columns = None
__model = None

def load_saved_artifacts():
    global __data_columns
    global __locations
    global __model
    
    # Get the directory where util.py is located
    current_dir = os.path.dirname(__file__)
    artifacts_path = os.path.join(current_dir, 'artifacts')
    
    try:
        # Load columns.json
        columns_path = os.path.join(artifacts_path, 'columns.json')
        with open(columns_path, "r") as f:
            __data_columns = json.load(f)['data_columns']
            __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk
        
        # Load model
        model_path = os.path.join(artifacts_path, 'banglore_home_prices_model.pickle')
        with open(model_path, 'rb') as f:
            __model = pickle.load(f)
            
        print("Artifacts loaded successfully")
    except FileNotFoundError as e:
        print(f"Error loading artifacts: {e}")
        raise
    except Exception as e:
        print(f"Unexpected error loading artifacts: {e}")
        raise

def get_location_names():
    return __locations

def get_data_columns():
    return __data_columns

def get_estimated_price(location, sqft, bhk, bath):
    """
    Predict home price based on location, square footage, BHK, and bathrooms
    """
    try:
        # Find the index of the location in the data columns
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        # Location not found, return error or default behavior
        raise ValueError(f"Location '{location}' not found in training data")
    
    # Create input array with zeros
    x = np.zeros(len(__data_columns))
    x[0] = sqft    # total_sqft
    x[1] = bath    # bath
    x[2] = bhk     # bhk
    
    if loc_index >= 0:
        x[loc_index] = 1  # Set the location column to 1
    
    # Make prediction
    predicted_price = round(__model.predict([x])[0], 2)
    return predicted_price