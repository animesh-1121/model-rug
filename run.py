#!/usr/bin/env python3
"""
Simple startup script for the Civic Issues Image Classifier Flask application.
This script provides an easy way to run the application with proper error handling.
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import tensorflow
        import numpy
        import cv2
        import pandas
        from PIL import Image
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_model():
    """Check if the model file exists"""
    model_path = "saved_model/image_classifier.h5"
    if os.path.exists(model_path):
        print("✅ Model file found")
        return True
    else:
        print("⚠️  Model file not found at saved_model/image_classifier.h5")
        print("   The application will still run, but you'll need to train a model first.")
        return False

def main():
    """Main function to start the application"""
    print("🚀 Starting Civic Issues Image Classifier...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check model
    check_model()
    
    print("\n📋 Application Information:")
    print("   - Web Interface: http://localhost:5000")
    print("   - Upload Page: http://localhost:5000")
    print("   - Training Page: http://localhost:5000/train")
    print("\n💡 Tips:")
    print("   - Make sure your images are under 16MB")
    print("   - Supported formats: PNG, JPG, JPEG, GIF, BMP")
    print("   - Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
