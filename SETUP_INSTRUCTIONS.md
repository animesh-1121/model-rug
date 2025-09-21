# Setup Instructions for Civic Issues Image Classifier

## Quick Start

### Option 1: Using the Batch File (Windows)
1. Double-click `start.bat`
2. Wait for dependencies to install
3. Open your browser to `http://localhost:5000`

### Option 2: Manual Setup
1. Install Python 3.8 or higher
2. Run: `pip install -r requirements.txt`
3. Run: `python run.py`
4. Open your browser to `http://localhost:5000`

## Important: Model File Setup

The application expects a trained model file at `saved_model/image_classifier.h5`. 

### If you have the trained model from the notebook:
1. Copy the model file from your Google Colab or local training
2. Place it in the `saved_model/` directory
3. Rename it to `image_classifier.h5`

### If you don't have a trained model:
1. Use the training interface at `http://localhost:5000/train`
2. Prepare your dataset in folders named after each class
3. Follow the training instructions in the web interface

## File Structure Created

```
model-rug/
├── app.py                              # Main Flask application
├── run.py                              # Startup script with checks
├── start.bat                           # Windows batch file for easy start
├── requirements.txt                    # Python dependencies
├── README.md                           # Comprehensive documentation
├── SETUP_INSTRUCTIONS.md              # This file
├── templates/                          # HTML templates
│   ├── base.html                       # Base template with navigation
│   ├── index.html                      # Main upload page
│   └── train.html                      # Training interface
├── static/                             # Static files
│   ├── style.css                       # Custom styling
│   └── script.js                       # JavaScript functionality
├── saved_model/                        # Model storage
│   ├── civic_issues_report_classified.csv  # Severity/priority mapping
│   └── image_classifier.h5            # Your trained model (copy here)
└── uploads/                            # Temporary upload directory (auto-created)
```

## Features Implemented

✅ **Image Upload & Classification**
- Drag-and-drop or click to upload images
- Real-time processing with progress indicator
- Confidence scores and visual feedback

✅ **Modern Web Interface**
- Responsive Bootstrap design
- Mobile-friendly interface
- Professional styling with animations

✅ **Severity & Priority Mapping**
- Automatic severity and priority assignment
- Color-coded badges for easy identification
- Configurable mapping system

✅ **Model Training Interface**
- Web-based training interface
- Progress tracking and logging
- Parameter configuration

✅ **Error Handling**
- File validation (size, format)
- Network error handling
- User-friendly error messages

✅ **Documentation**
- Comprehensive README
- Setup instructions
- API documentation

## Next Steps

1. **Copy your trained model** to `saved_model/image_classifier.h5`
2. **Test the application** by uploading sample images
3. **Customize the interface** if needed (colors, labels, etc.)
4. **Deploy to production** when ready

## Troubleshooting

- **Model not found**: Copy your trained model to the correct location
- **Import errors**: Run `pip install -r requirements.txt`
- **Port already in use**: Change the port in `app.py` or `run.py`
- **File upload issues**: Check file size (max 16MB) and format

## Support

The application is now ready to use! The Flask app provides a complete web interface for your civic issues image classification model.
