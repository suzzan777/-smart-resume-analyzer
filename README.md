Smart Resume Analyzer & AI-Powered Job Matching System

Project Overview

This project was developed for the COM668 Computing Project module. It is a web-based prototype designed to support resume analysis and job matching. The system allows a user to upload one or more resumes, enter a target job description, and receive a structured analysis showing how well a candidate matches the role.

The main purpose of the project is to improve the early stages of recruitment screening by using natural language processing and information retrieval techniques. Instead of relying only on manual reading or simple keyword overlap, the system extracts important information from resumes and compares it with job requirements in a more structured and explainable way.

Main Features

The system currently includes the following features:

* Resume upload in PDF and DOCX formats
* Text extraction from uploaded resumes
* Job title, job source, and job source URL input
* Manual job description input
* Job seeker view and employer view
* Skill extraction from resumes and job descriptions
* Education keyword extraction
* Experience indicator extraction
* Organisation extraction using spaCy
* TF-IDF and cosine similarity matching
* Feature-level scoring
* Matched skills and missing skills analysis
* Job seeker improvement feedback
* Employer fit summary
* Multiple candidate ranking
* SQLite database storage
* Analysis history page
* CSV export of stored analysis results
* Evaluation dashboard with precision, recall, F1-score, and accuracy
* Chart-based visualisation for history and evaluation pages

Technologies Used

This project was built using the following tools and technologies:

* Python
* Flask
* SQLite
* pdfplumber
* python-docx
* spaCy
* scikit-learn
* HTML
* CSS
* JavaScript
* Chart.js

How the System Works

The user uploads a resume and enters a target job description. The system first extracts raw text from the uploaded resume file. It then identifies useful information such as skills, education-related terms, experience indicators, and organisation names. After that, the extracted resume data is compared with the job description.

The matching process combines two approaches. The first is a text-based similarity score using TF-IDF and cosine similarity. The second is a feature-level score based on how well the candidate matches the required skills, education, and experience indicators. These two scores are combined to produce an overall match score.

The system can present results in two ways. In Job Seeker View, the focus is on missing skills, matched skills, and suggestions for improving the resume. In Employer View, the focus is on candidate fit, matched and missing skills, and experience-related indicators.

Evaluation

The project also includes an evaluation workflow. A labelled dataset of resume and job-description pairs can be used to test how well the system performs. The evaluation dashboard reports:

* Precision
* Recall
* F1-score
* Accuracy

It also includes qualitative comments to help explain the strengths and limitations of the system.

How to Run the Project

1. Open the project folder in VS Code.
2. Create and activate a virtual environment.
3. Install the required libraries using:

python -m pip install -r requirements.txt

4. Download the spaCy English model:

python -m spacy download en_core_web_sm

5. Run the application:

python app.py

6. Open the browser and go to:

http://127.0.0.1:5000

Project Structure

The main project includes:

* app.py for the Flask application
* templates/ for HTML pages
* static/ for CSS and JavaScript files
* utils/ for parsing, extraction, matching, feedback, database, and evaluation modules
* data/ for evaluation files
* uploads/ for uploaded resume files
* resume_data.db for stored analysis results

Purpose and Scope

This project is intended as an academic prototype rather than a full commercial recruitment platform. It is designed to show how resume parsing, NLP-based extraction, feature-level analysis, and job matching can be combined into a practical web application.

The system is intended to support decision-making, not replace human judgement. It should be used as a recruitment support tool rather than an automated hiring system.

Future Improvements

Possible future improvements include:

* more advanced spaCy-based entity extraction
* stronger semantic matching models
* better section-level resume parsing
* integration with approved job APIs
* PDF report export
* stronger evaluation with larger labelled datasets

Author

Sujan Khatri
COM668 Computing Project