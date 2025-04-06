Welcome to CVision, an innovative AI-driven recruitment solution designed to automate and optimize the hiring process. Built with a multi-agent architecture, CVision leverages advanced natural language processing (NLP) and data intelligence to summarize job descriptions, match candidates, shortlist them, and send interview requests—all while maintaining persistent data with a SQLite database.

Table of Contents
Features
Job Description Summarizer: Automatically extracts and summarizes key details (skills, experience, qualifications) from job descriptions using NLP.
CV Analysis: Parses candidate CVs to extract education, skills, experience, and certifications.
Intelligent Matching: Calculates match scores between candidates and job requirements, with customizable thresholds.
Candidate Shortlisting: Identifies top candidates based on match scores for interview consideration.
Automated Interview Scheduling: Generates and sends personalized email invitations to shortlisted candidates.
Persistent Storage: Uses SQLite for long-term data management of jobs, candidates, and matches.
Installation
Prerequisites
Python 3.11+
Node.js 18+ (for frontend)
Git
Setup Instructions
Clone the Repository:
bash

Collapse

Wrap

Copy
git clone https://github.com/your-username/cvision.git
cd cvision
Set Up the Backend:
Install Python dependencies:
bash

Collapse

Wrap

Copy
pip install -r requirements.txt
Create a .env file in the root directory with your Gmail credentials:
text

Collapse

Wrap

Copy
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
(Note: Generate an App Password from your Google Account if 2FA is enabled.)
Set Up the Frontend:
Navigate to the frontend directory (if separated) or install dependencies in the root:
bash

Collapse

Wrap

Copy
npm install
Ensure .env includes:
text

Collapse

Wrap

Copy
VITE_API_URL=http://localhost:5000
Initialize the Database:
The database (recruitment.db) will be created automatically when the backend runs, but ensure write permissions in the project directory.
Usage
Run the Backend:
bash

Collapse

Wrap

Copy
python api.py
The server will start on http://0.0.0.0:5000.
Run the Frontend:
bash

Collapse

Wrap

Copy
npm run dev
Access the app at http://localhost:5173.
Interact with the System:
Use the web interface (MatchesPage) to process job descriptions, CVs, match candidates, and generate interview requests.
Example API endpoints:
POST /process-job: Submit a job description.
POST /process-cv: Upload a candidate CV.
POST /api/match-candidate: Match a candidate to a job.
POST /api/generate-interview-requests: Send interview emails.
Project Structure
text

Collapse

Wrap

Copy
cvision/
├── api.py                # FastAPI backend endpoints
├── main.py               # Recruitment system logic and agent orchestration
├── agents.py             # AI agent implementations (e.g., summarizer, matcher)
├── database.py           # SQLite database management
├── /frontend/            # (Optional) Frontend directory
│   ├── api.js            # Axios API client
│   ├── MatchesPage.tsx   # React component for UI
├── .env                  # Environment variables
├── recruitment.db        # SQLite database file
├── requirements.txt      # Python dependencies
├── package.json          # Node.js dependencies
└── README.md             # This file
Technologies Used
Backend: Python, FastAPI, LangChain (Google Generative AI), SMTPlib, SQLite
Frontend: React, TypeScript, Vite, TanStack Query, React Hook Form, Axios
Tools: Dotenv for environment management
Getting Started
Prerequisites Check: Ensure all dependencies are installed as per the section.
First Run: Follow the usage steps to process a sample job and CV.
Troubleshooting: Check api.py logs for errors; refer to the section if needed.
Contributing
We welcome contributions! To get involved:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes and commit (git commit -m "Add new feature").
Push to your fork (git push origin feature-branch).
Open a Pull Request with a clear description of your changes.
Please adhere to our  (create one if desired).

License
This project is licensed under the MIT License - see the  file for details.

Contact
Project Maintainer: [Your Name] - [your-email@example.com]
GitHub Repository: https://github.com/your-username/cvision
Issues: Report bugs or suggest features here.
Issues
Encountered a problem? Check the logs in the terminal running api.py.
Common fixes: Ensure unique emails for CVs, verify .env credentials, and confirm database write access.
