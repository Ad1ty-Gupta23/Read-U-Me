import os
import json
import tempfile
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from analyze_resume import analyze_resume
from processing.skill_extractor import extract_text_from_pdf, get_skills

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure upload folder
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Flask server is running"})

@app.route('/api/analyze-resume', methods=['POST'])
def api_analyze_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file provided"}), 400
    
    file = request.files['resume']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    try:
        # Save the uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Analyze the resume
        results = analyze_resume(file_path)
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/extract-skills', methods=['POST'])
def api_extract_skills():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file provided"}), 400
    
    file = request.files['resume']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "File must be a PDF"}), 400
    
    try:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp:
            file.save(temp.name)
            temp_path = temp.name
        
        # Extract text from PDF
        resume_text = extract_text_from_pdf(temp_path)
        
        # Extract skills
        skills = get_skills(resume_text)
        
        # Clean up the temporary file
        os.unlink(temp_path)
        
        return jsonify({"skills": skills})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/job-recommendations', methods=['POST'])
def api_job_recommendations():
    data = request.json
    
    if not data or 'skills' not in data:
        return jsonify({"error": "No skills provided"}), 400
    
    skills = data['skills']
    
    if not isinstance(skills, list) or len(skills) == 0:
        return jsonify({"error": "Skills must be a non-empty list"}), 400
    
    try:
        # Create a mock resume text with the provided skills
        mock_resume_text = "Skills: " + ", ".join(skills)
        
        # Use the analyze_resume function but with our mock resume
        with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp:
            temp.write(mock_resume_text.encode('utf-8'))
            temp_path = temp.name
        
        # Analyze the mock resume to get job recommendations
        results = analyze_resume(temp_path)
        
        # Clean up the temporary file
        os.unlink(temp_path)
        
        # Return only the job recommendations part
        return jsonify({
            "job_recommendations": results.get('job_recommendations', [])
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)