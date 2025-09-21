// JavaScript for Civic Issues Classifier

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const results = document.getElementById('results');
    const errorMessage = document.getElementById('errorMessage');

    // File input change handler
    fileInput.addEventListener('change', function() {
        const file = this.files[0];
        if (file) {
            // Validate file size (16MB max)
            if (file.size > 16 * 1024 * 1024) {
                showError('File size must be less than 16MB');
                this.value = '';
                return;
            }
            
            // Validate file type
            const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/bmp'];
            if (!allowedTypes.includes(file.type)) {
                showError('Please select a valid image file (PNG, JPG, JPEG, GIF, BMP)');
                this.value = '';
                return;
            }
            
            hideError();
        }
    });

    // Form submission handler
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const file = fileInput.files[0];
        if (!file) {
            showError('Please select a file to upload');
            return;
        }

        uploadAndClassify(file);
    });

    function uploadAndClassify(file) {
        const formData = new FormData();
        formData.append('file', file);

        // Show loading state
        showLoading();
        hideResults();
        hideError();

        // Make API request
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            hideLoading();
            
            if (data.success) {
                displayResults(data);
            } else {
                showError(data.error || 'An error occurred during classification');
            }
        })
        .catch(error => {
            hideLoading();
            showError('Network error: ' + error.message);
        });
    }

    function displayResults(data) {
        const predictionResult = document.getElementById('predictionResult');
        const severityPriority = document.getElementById('severityPriority');
        const resultImage = document.getElementById('resultImage');

        // Format prediction result
        predictionResult.innerHTML = `
            <div class="text-center">
                <div class="prediction-badge bg-primary text-white mb-3">
                    ${formatClassName(data.prediction)}
                </div>
                <div class="mb-2">
                    <strong>Confidence:</strong> ${data.confidence_percent}%
                </div>
                <div class="confidence-bar mb-2" style="width: 100%; background: linear-gradient(90deg, 
                    #dc3545 0%, #ffc107 50%, #28a745 100%);">
                    <div class="progress-bar bg-transparent" style="width: ${data.confidence_percent}%; 
                        background: rgba(255,255,255,0.3); border-radius: 10px;"></div>
                </div>
            </div>
        `;

        // Format severity and priority
        severityPriority.innerHTML = `
            <div class="text-center">
                <div class="mb-3">
                    <strong>Severity:</strong><br>
                    <span class="severity-badge severity-${data.severity.toLowerCase()}">
                        ${data.severity}
                    </span>
                </div>
                <div>
                    <strong>Priority:</strong><br>
                    <span class="priority-badge priority-${data.priority.toLowerCase()}">
                        ${data.priority}
                    </span>
                </div>
            </div>
        `;

        // Display image
        if (data.image) {
            resultImage.src = data.image;
            resultImage.alt = 'Uploaded image';
        }

        // Show results with animation
        results.style.display = 'block';
        results.classList.add('fade-in-up');
    }

    function formatClassName(className) {
        return className.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
    }

    function showLoading() {
        loadingSpinner.style.display = 'block';
        uploadBtn.disabled = true;
        uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
    }

    function hideLoading() {
        loadingSpinner.style.display = 'none';
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<i class="fas fa-search"></i> Classify Image';
    }

    function showResults() {
        results.style.display = 'block';
    }

    function hideResults() {
        results.style.display = 'none';
        results.classList.remove('fade-in-up');
    }

    function showError(message) {
        errorMessage.style.display = 'block';
        document.getElementById('errorText').textContent = message;
    }

    function hideError() {
        errorMessage.style.display = 'none';
    }

    // Reset form function (called from HTML)
    window.resetForm = function() {
        uploadForm.reset();
        hideResults();
        hideError();
        hideLoading();
    };
});

// Training functionality
function startTraining() {
    const datasetPath = document.getElementById('datasetPath').value;
    const epochs = document.getElementById('epochs').value;
    const batchSize = document.getElementById('batchSize').value;

    if (!datasetPath) {
        showTrainingError('Please provide a dataset path');
        return;
    }

    const trainBtn = document.getElementById('trainBtn');
    const trainingProgress = document.getElementById('trainingProgress');
    const trainingResults = document.getElementById('trainingResults');
    const trainingError = document.getElementById('trainingError');

    // Hide previous results/errors
    trainingResults.style.display = 'none';
    trainingError.style.display = 'none';

    // Show progress section
    trainingProgress.style.display = 'block';

    // Update button state
    trainBtn.disabled = true;
    trainBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Training...';

    // Clear previous log
    document.getElementById('logContent').innerHTML = '';

    // Simulate training progress (in real implementation, this would be WebSocket or polling)
    simulateTrainingProgress();

    // Make API call
    fetch('/api/train', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            dataset_path: datasetPath,
            epochs: parseInt(epochs),
            batch_size: parseInt(batchSize)
        })
    })
    .then(response => response.json())
    .then(data => {
        trainBtn.disabled = false;
        trainBtn.innerHTML = '<i class="fas fa-play"></i> Start Training';
        
        if (data.success) {
            showTrainingResults(data);
        } else {
            showTrainingError(data.error || 'Training failed');
        }
    })
    .catch(error => {
        trainBtn.disabled = false;
        trainBtn.innerHTML = '<i class="fas fa-play"></i> Start Training';
        showTrainingError('Network error: ' + error.message);
    });
}

function simulateTrainingProgress() {
    const progressBar = document.getElementById('progressBar');
    const logContent = document.getElementById('logContent');
    
    let progress = 0;
    const interval = setInterval(() => {
        progress += Math.random() * 10;
        if (progress > 100) progress = 100;
        
        progressBar.style.width = progress + '%';
        progressBar.textContent = Math.round(progress) + '%';
        
        // Add log entries
        if (Math.random() < 0.3) {
            addLogEntry(`Epoch ${Math.floor(progress / 10) + 1}: Training accuracy improving...`, 'info');
        }
        
        if (progress >= 100) {
            clearInterval(interval);
            addLogEntry('Training completed successfully!', 'success');
        }
    }, 500);
}

function addLogEntry(message, type = 'info') {
    const logContent = document.getElementById('logContent');
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry log-${type}`;
    logEntry.textContent = `[${timestamp}] ${message}`;
    logContent.appendChild(logEntry);
    logContent.scrollTop = logContent.scrollHeight;
}

function showTrainingResults(data) {
    const trainingResults = document.getElementById('trainingResults');
    const resultsContent = document.getElementById('resultsContent');
    
    resultsContent.innerHTML = `
        <div class="alert alert-success">
            <i class="fas fa-check-circle"></i>
            <strong>Training completed successfully!</strong>
        </div>
        <p><strong>Message:</strong> ${data.message}</p>
        <p><strong>Note:</strong> ${data.note}</p>
    `;
    
    trainingResults.style.display = 'block';
}

function showTrainingError(message) {
    const trainingError = document.getElementById('trainingError');
    document.getElementById('trainingErrorText').textContent = message;
    trainingError.style.display = 'block';
}
