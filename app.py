import os
import numpy as np
import cv2
import pandas as pd
from flask import Flask, request, render_template, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import base64
from io import BytesIO
from PIL import Image

# Try to import TensorFlow, handle gracefully if not available
try:
    import tensorflow as tf
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("⚠️  TensorFlow not available. Model loading will be disabled.")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

# Global variables for model and class labels
model = None
class_labels = [
    "Accident",
    "Domestic_trash", 
    "Infrastructure_Damage_Concrete",
    "Non Accident",
    "Parking_Issues_Illegal_Parking",
    "Road_Issues_Damaged_Sign",
    "Road_Issues_Pothole",
    "Vandalism_Graffiti"
]

# Severity and priority mapping (you can modify this based on your CSV)
severity_priority_map = {
    "Accident": {"Severity": "Critical", "Priority": "High"},
    "Domestic_trash": {"Severity": "Medium", "Priority": "Medium"},
    "Infrastructure_Damage_Concrete": {"Severity": "High", "Priority": "High"},
    "Non Accident": {"Severity": "Info", "Priority": "Low"},
    "Parking_Issues_Illegal_Parking": {"Severity": "Medium", "Priority": "Medium"},
    "Road_Issues_Damaged_Sign": {"Severity": "High", "Priority": "High"},
    "Road_Issues_Pothole": {"Severity": "High", "Priority": "High"},
    "Vandalism_Graffiti": {"Severity": "Medium", "Priority": "Medium"}
}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_model():
    """Load the trained model"""
    global model
    if not TENSORFLOW_AVAILABLE:
        print("❌ TensorFlow not available. Cannot load model.")
        return False
    
    try:
        model_path = "saved_model/image_classifier.h5"
        if os.path.exists(model_path):
            model = tf.keras.models.load_model(model_path)
            print("✅ Model loaded successfully")
            return True
        else:
            print("❌ Model file not found. Please ensure the model is trained and saved.")
            return False
    except Exception as e:
        print(f"❌ Error loading model: {str(e)}")
        return False

def preprocess_image(image_path):
    """Preprocess image for prediction"""
    try:
        # Load image
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize to model input size
        img_size = (224, 224)
        img_resized = cv2.resize(img, img_size)
        
        # Normalize pixel values
        img_normalized = img_resized / 255.0
        
        # Add batch dimension
        img_batch = np.expand_dims(img_normalized, axis=0)
        
        return img_batch, img_resized
    except Exception as e:
        print(f"❌ Error preprocessing image: {str(e)}")
        return None, None

def predict_image(image_batch):
    """Make prediction on preprocessed image"""
    if not TENSORFLOW_AVAILABLE or model is None:
        print("❌ Model not available for prediction")
        return None, None, None, None
    
    try:
        predictions = model.predict(image_batch, verbose=0)
        predicted_class_idx = np.argmax(predictions)
        predicted_class = class_labels[predicted_class_idx]
        confidence = np.max(predictions)
        
        # Get severity and priority
        sev = severity_priority_map.get(predicted_class, {}).get("Severity", "Unknown")
        pri = severity_priority_map.get(predicted_class, {}).get("Priority", "Unknown")
        
        return predicted_class, confidence, sev, pri
    except Exception as e:
        print(f"❌ Error making prediction: {str(e)}")
        return None, None, None, None

def image_to_base64(image_array):
    """Convert image array to base64 string for display"""
    try:
        # Convert numpy array to PIL Image
        img_pil = Image.fromarray((image_array * 255).astype(np.uint8))
        
        # Convert to base64
        buffer = BytesIO()
        img_pil.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"data:image/png;base64,{img_str}"
    except Exception as e:
        print(f"❌ Error converting image to base64: {str(e)}")
        return None

@app.route('/')
def index():
    """Main page with upload form"""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and prediction"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Save uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Preprocess image
            image_batch, image_resized = preprocess_image(filepath)
            
            if image_batch is None:
                return jsonify({'error': 'Error processing image'}), 500
            
            # Make prediction
            predicted_class, confidence, severity, priority = predict_image(image_batch)
            
            if predicted_class is None:
                if not TENSORFLOW_AVAILABLE:
                    return jsonify({'error': 'TensorFlow not available. Please install TensorFlow to use predictions.'}), 500
                else:
                    return jsonify({'error': 'Error making prediction'}), 500
            
            # Convert image to base64 for display
            image_base64 = image_to_base64(image_resized)
            
            # Clean up uploaded file
            os.remove(filepath)
            
            # Return results
            result = {
                'success': True,
                'prediction': predicted_class,
                'confidence': float(confidence),
                'confidence_percent': round(confidence * 100, 2),
                'severity': severity,
                'priority': priority,
                'image': image_base64
            }
            
            return jsonify(result)
            
        except Exception as e:
            # Clean up file if it exists
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/train')
def train_model():
    """Page for training the model (optional feature)"""
    return render_template('train.html')

@app.route('/api/train', methods=['POST'])
def train_model_api():
    """API endpoint for training the model"""
    try:
        # This would contain the training logic from the notebook
        # For now, return a placeholder response
        return jsonify({
            'success': True,
            'message': 'Training functionality can be implemented here',
            'note': 'This requires the dataset to be available'
        })
    except Exception as e:
        return jsonify({'error': f'Training error: {str(e)}'}), 500

if __name__ == '__main__':
    # Load model on startup
    model_loaded = load_model()
    if model_loaded:
        print("🚀 Starting Flask application with model loaded...")
    else:
        print("⚠️  Starting Flask application without model (TensorFlow issue)")
        print("   The web interface will work, but predictions will be disabled.")
        print("   To fix this, install TensorFlow: pip install tensorflow")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
