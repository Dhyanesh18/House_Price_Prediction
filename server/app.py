from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import util
import os
from waitress import serve

app = Flask(__name__, static_folder='../client', static_url_path='')
CORS(app)

# Serve frontend
@app.route('/')
def serve_client():
    return send_from_directory(app.static_folder, 'app.html')

# API Endpoints
@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    try:
        locations = util.get_location_names()
        if locations is None:
            return jsonify({'error': 'Locations not loaded'}), 500
        
        response = jsonify({
            'locations': locations
        })
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        data = request.get_json()
        
        # Validate input data
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        required_fields = ['location', 'total_sqft', 'bhk', 'bath']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Validate data types and ranges
        try:
            total_sqft = float(data['total_sqft'])
            bhk = int(data['bhk'])
            bath = int(data['bath'])
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid numeric values'}), 400
        
        if total_sqft <= 0:
            return jsonify({'error': 'Square footage must be greater than 0'}), 400
        
        if bhk <= 0 or bhk > 10:
            return jsonify({'error': 'BHK must be between 1 and 10'}), 400
        
        if bath <= 0 or bath > 10:
            return jsonify({'error': 'Bathrooms must be between 1 and 10'}), 400
        
        # Get prediction
        estimated_price = util.get_estimated_price(
            data['location'],
            total_sqft,
            bhk,
            bath
        )
        
        response = jsonify({
            'estimated_price': estimated_price
        })
        return response
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        print(f"Prediction error: {e}")  # Log the error
        return jsonify({'error': 'Internal server error'}), 500

# Serve static files explicitly (alternative approach)
@app.route('/<path:filename>')
def static_files(filename):
    try:
        return send_from_directory(app.static_folder, filename)
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

if __name__ == "__main__":
    print("Starting Python Flask Server...")
    try:
        util.load_saved_artifacts()
        print("Server starting on http://0.0.0.0:5000")
        serve(app, host="0.0.0.0", port=5000)
    except Exception as e:
        print(f"Failed to start server: {e}")
        exit(1)