# 🧠 CVision – AI-Driven Recruitment Platform

**CVision** is an innovative AI-driven recruitment solution designed to automate and optimize the hiring process. Built with a **multi-agent architecture**, CVision leverages advanced **Natural Language Processing (NLP)** and **data intelligence** to:

- Summarize job descriptions
- Parse and analyze CVs
- Match candidates to job requirements
- Shortlist candidates
- Automate interview requests  
All while maintaining **persistent data** using **SQLite**.

---

## 📑 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 🚀 Features

- **Job Description Summarizer:**  
  Automatically extracts and summarizes key details (skills, experience, qualifications) using NLP.

- **CV Analysis:**  
  Parses candidate CVs to extract education, skills, experience, and certifications.

- **Intelligent Matching:**  
  Calculates match scores between candidates and job requirements, with customizable thresholds.

- **Candidate Shortlisting:**  
  Identifies top candidates based on match scores for interview consideration.

- **Automated Interview Scheduling:**  
  Generates and sends personalized email invitations to shortlisted candidates.

- **Persistent Storage:**  
  Uses SQLite for long-term data management of jobs, candidates, and matches.

---

## ⚙️ Installation

### 🔍 Prerequisites

- Python 3.11+
- Node.js 18+
- Git

### 📦 Setup Instructions

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/cvision.git
cd cvision
```

### 2. Set Up the Backend
Install Python dependencies:

```bash
pip install -r requirements.txt
```
Create a .env file in the root directory:

```env
EMAIL_USER=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```
Note: Generate an App Password from your Google Account if 2FA is enabled.

### 3. Set Up the Frontend
Navigate to the frontend directory or stay in root (depending on structure):

```bash

npm install
Add to .env:
```
```env

VITE_API_URL=http://localhost:5000
```
### 4. Initialize the Database
The recruitment.db file is auto-generated when the backend runs.
Make sure the project directory has write permissions.

## 🧪 Usage
Start the Backend
```bash
python api.py
```
The backend will run on:
http://0.0.0.0:5000

Start the Frontend
```bash

npm run dev
```
Access the frontend UI at:
http://localhost:5173

## Interact with the System
- Use the UI  to:

  - Upload and process job descriptions

  - Upload candidate CVs

  - Match candidates

  - Generate interview invitations

## Example API Endpoints
| Endpoint |	Description |
| --------- | ----------- |
| POST /process-job | Submit a job description |
| POST /process-cv |	Upload a candidate CV |
| POST /api/match-candidate | Match a candidate to a job |
| POST /api/generate-interview-requests | Send interview emails |
### 🧱 Project Structure
```bash

cvision/
├── api.py                 # FastAPI backend endpoints
├── main.py                # Recruitment system logic and orchestration
├── agents.py              # AI agent implementations
├── database.py            # SQLite database handling
├── frontend/              # React frontend
│   ├── api.js             # Axios API client
│   ├── MatchesPage.tsx    # Matching UI component
├── .env                   # Environment variables
├── recruitment.db         # SQLite database
├── requirements.txt       # Python packages
├── package.json           # Node.js packages
└── README.md              # This file
```
### 🛠 Technologies Used
Backend: Python, FastAPI, LangChain, SMTPlib, SQLite

Frontend: React, TypeScript, Vite, TanStack Query, React Hook Form, Axios

Tools: Dotenv for environment management

# 🧭 Getting Started
- ### ✅ Install all prerequisites

- ### ▶️ Follow installation steps

- ### 🧪 Run the app with usage instructions

- ### 🧰 Check backend logs (api.py) for troubleshooting

- ### 🤝 Contributing
- ### We welcome contributions!

### Steps:
- Fork the repository

- Create a new branch

```bash

git checkout -b feature-branch

```
- Make your changes and commit
```bash

git commit -m "Add new feature"
```
- Push to your fork

```bash

git push origin feature-branch

```
- Open a Pull Request with a clear description.

## Please follow our contribution guidelines (coming soon if not present).

## 📄 License
Licensed under the MIT License.
See the LICENSE file for details.

## 📬 Contact
Maintainer: Shyam
📧 Email: Shyamrathore013@gmail.com
🔗 GitHub: https://github.com/your-username/cvision


