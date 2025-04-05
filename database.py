import sqlite3
import json
from datetime import datetime

class RecruitmentDB:
    def __init__(self, db_path="recruitment.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self.initialize_db()
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        self.cursor = self.conn.cursor()
        
    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def initialize_db(self):
        self.connect()
        
        # Create job_descriptions table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS job_descriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            description TEXT NOT NULL,
            summary TEXT,
            required_skills TEXT,  -- stored as JSON
            required_experience TEXT,
            required_qualifications TEXT,
            responsibilities TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create candidates table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT,
            cv_text TEXT NOT NULL,
            education TEXT,  -- stored as JSON
            experience TEXT,  -- stored as JSON
            skills TEXT,  -- stored as JSON
            certifications TEXT,  -- stored as JSON
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Create matches table
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            candidate_id INTEGER NOT NULL,
            match_score REAL NOT NULL,
            match_details TEXT,  -- stored as JSON
            is_shortlisted BOOLEAN DEFAULT FALSE,
            interview_requested BOOLEAN DEFAULT FALSE,
            interview_request_sent_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES job_descriptions (id),
            FOREIGN KEY (candidate_id) REFERENCES candidates (id)
        )
        ''')
        
        self.conn.commit()
        self.close()
    
    # Job Description Methods
    def add_job_description(self, title, company, description, summary=None, 
                           required_skills=None, required_experience=None, 
                           required_qualifications=None, responsibilities=None):
        self.connect()
        
        # Convert list fields to JSON strings if provided
        if required_skills and isinstance(required_skills, list):
            required_skills = json.dumps(required_skills)
        if responsibilities and isinstance(responsibilities, list):
            responsibilities = json.dumps(responsibilities)
        
        self.cursor.execute('''
        INSERT INTO job_descriptions 
        (title, company, description, summary, required_skills, 
         required_experience, required_qualifications, responsibilities) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, company, description, summary, required_skills, 
              required_experience, required_qualifications, responsibilities))
        
        job_id = self.cursor.lastrowid
        self.conn.commit()
        self.close()
        return job_id
    
    def get_job_description(self, job_id):
        self.connect()
        self.cursor.execute('SELECT * FROM job_descriptions WHERE id = ?', (job_id,))
        row = self.cursor.fetchone()
        if not row:
            self.close()
            return None
            
        job = dict(row)
        
        # Parse JSON fields
        for field in ['required_skills', 'responsibilities']:
            if job.get(field):
                try:
                    job[field] = json.loads(job[field])
                except json.JSONDecodeError:
                    # Keep as string if not valid JSON
                    pass
                
        self.close()
        return job
    
    def get_all_job_descriptions(self):
        """Get all job descriptions from the database"""
        self.connect()
        self.cursor.execute('SELECT * FROM job_descriptions ORDER BY created_at DESC')
        jobs = [dict(row) for row in self.cursor.fetchall()]
        
        # Parse JSON fields for each job
        for job in jobs:
            for field in ['required_skills', 'responsibilities']:
                if job.get(field):
                    try:
                        job[field] = json.loads(job[field])
                    except json.JSONDecodeError:
                        # Keep as string if not valid JSON
                        pass
        
        self.close()
        return jobs
    def delete_job_description(self, job_id):
        """Delete a job description and associated matches from the database"""
        self.connect()
        # First, delete associated matches
        self.cursor.execute('DELETE FROM matches WHERE job_id = ?', (job_id,))
        # Then, delete the job description
        self.cursor.execute('DELETE FROM job_descriptions WHERE id = ?', (job_id,))
        self.conn.commit()
        self.close()
    
    # Candidate Methods
    def add_candidate(self, name, email, cv_text, phone=None, 
                     education=None, experience=None, skills=None, certifications=None):
        self.connect()
        
        # Convert list/dict fields to JSON strings if provided
        if education and isinstance(education, (list, dict)):
            education = json.dumps(education)
        if experience and isinstance(experience, (list, dict)):
            experience = json.dumps(experience)
        if skills and isinstance(skills, list):
            skills = json.dumps(skills)
        if certifications and isinstance(certifications, list):
            certifications = json.dumps(certifications)
        
        try:
            self.cursor.execute('''
            INSERT INTO candidates 
            (name, email, phone, cv_text, education, experience, skills, certifications) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, email, phone, cv_text, education, experience, skills, certifications))
            
            candidate_id = self.cursor.lastrowid
            self.conn.commit()
            self.close()
            return candidate_id
        except sqlite3.IntegrityError:
            self.close()
            return None  # Email already exists
    
    def get_candidate(self, candidate_id):
        self.connect()
        self.cursor.execute('SELECT * FROM candidates WHERE id = ?', (candidate_id,))
        row = self.cursor.fetchone()
        if not row:
            self.close()
            return None
            
        candidate = dict(row)
        
        # Parse JSON fields
        for field in ['education', 'experience', 'skills', 'certifications']:
            if candidate.get(field):
                try:
                    candidate[field] = json.loads(candidate[field])
                except json.JSONDecodeError:
                    # Keep as string if not valid JSON
                    pass
                
        self.close()
        return candidate
    
    def get_candidate_by_email(self, email):
        """Get a candidate by email address"""
        self.connect()
        self.cursor.execute('SELECT * FROM candidates WHERE email = ?', (email,))
        row = self.cursor.fetchone()
        if not row:
            self.close()
            return None
            
        candidate = dict(row)
        
        # Parse JSON fields
        for field in ['education', 'experience', 'skills', 'certifications']:
            if candidate.get(field):
                try:
                    candidate[field] = json.loads(candidate[field])
                except json.JSONDecodeError:
                    # Keep as string if not valid JSON
                    pass
                
        self.close()
        return candidate
    
    def get_all_candidates(self):
        """Get all candidates from the database"""
        self.connect()
        self.cursor.execute('SELECT * FROM candidates ORDER BY created_at DESC')
        candidates = [dict(row) for row in self.cursor.fetchall()]
        
        # Parse JSON fields for each candidate
        for candidate in candidates:
            for field in ['education', 'experience', 'skills', 'certifications']:
                if candidate.get(field):
                    try:
                        candidate[field] = json.loads(candidate[field])
                    except json.JSONDecodeError:
                        # Keep as string if not valid JSON
                        pass
        
        self.close()
        return candidates
    def delete_candidate(self, candidate_id):
        """Delete a candidate and associated matches from the database"""
        self.connect()
        # First, delete associated matches
        self.cursor.execute('DELETE FROM matches WHERE candidate_id = ?', (candidate_id,))
        # Then, delete the candidate
        self.cursor.execute('DELETE FROM candidates WHERE id = ?', (candidate_id,))
        self.conn.commit()
        self.close()    
    
    # Match Methods
    def add_match(self, job_id, candidate_id, match_score, match_details=None, is_shortlisted=False):
        self.connect()
        
        if match_details and isinstance(match_details, dict):
            match_details = json.dumps(match_details)
        
        # Check if a match for this job and candidate already exists
        self.cursor.execute(
            'SELECT id FROM matches WHERE job_id = ? AND candidate_id = ?', 
            (job_id, candidate_id)
        )
        existing = self.cursor.fetchone()
        
        if existing:
            # Update existing match
            self.cursor.execute('''
            UPDATE matches 
            SET match_score = ?, match_details = ?, is_shortlisted = ?
            WHERE id = ?
            ''', (match_score, match_details, is_shortlisted, existing['id']))
            match_id = existing['id']
        else:
            # Insert new match
            self.cursor.execute('''
            INSERT INTO matches 
            (job_id, candidate_id, match_score, match_details, is_shortlisted) 
            VALUES (?, ?, ?, ?, ?)
            ''', (job_id, candidate_id, match_score, match_details, is_shortlisted))
            match_id = self.cursor.lastrowid
        
        self.conn.commit()
        self.close()
        return match_id
    
    def update_match_status(self, match_id, is_shortlisted=None, interview_requested=None):
        self.connect()
        
        update_parts = []
        params = []
        
        if is_shortlisted is not None:
            update_parts.append("is_shortlisted = ?")
            params.append(is_shortlisted)
        
        if interview_requested is not None:
            update_parts.append("interview_requested = ?")
            params.append(interview_requested)
            update_parts.append("interview_request_sent_at = ?")
            params.append(datetime.now().isoformat())
        
        if update_parts:
            query = f"UPDATE matches SET {', '.join(update_parts)} WHERE id = ?"
            params.append(match_id)
            
            self.cursor.execute(query, params)
            self.conn.commit()
        
        self.close()
    
    def get_match(self, match_id):
        self.connect()
        self.cursor.execute('SELECT * FROM matches WHERE id = ?', (match_id,))
        row = self.cursor.fetchone()
        if not row:
            self.close()
            return None
            
        match = dict(row)
        
        # Parse JSON fields
        if match.get('match_details'):
            try:
                match['match_details'] = json.loads(match['match_details'])
            except json.JSONDecodeError:
                # Keep as string if not valid JSON
                pass
                
        self.close()
        return match
    
    def get_matches_for_job(self, job_id):
        """Get all matches for a specific job"""
        self.connect()
        self.cursor.execute('''
        SELECT m.*, c.name, c.email 
        FROM matches m
        JOIN candidates c ON m.candidate_id = c.id
        WHERE m.job_id = ?
        ORDER BY m.match_score DESC
        ''', (job_id,))
        
        matches = [dict(row) for row in self.cursor.fetchall()]
        
        # Parse JSON fields for each match
        for match in matches:
            if match.get('match_details'):
                try:
                    match['match_details'] = json.loads(match['match_details'])
                except json.JSONDecodeError:
                    # Keep as string if not valid JSON
                    pass
        
        self.close()
        return matches
    def get_all_matches(self):
        """Get all matches from the database"""
        self.connect()
        self.cursor.execute('SELECT * FROM matches ORDER BY created_at DESC')
        matches = [dict(row) for row in self.cursor.fetchall()]
        
        # Parse JSON fields for each match
        for match in matches:
            if match.get('match_details'):
                try:
                    match['match_details'] = json.loads(match['match_details'])
                except json.JSONDecodeError:
                    # Keep as string if not valid JSON
                    pass
        
        self.close()
        return matches
    
    def get_match_by_candidate(self, candidate_id):
        """Get the match for a specific candidate"""
        self.connect()
        self.cursor.execute('SELECT * FROM matches WHERE candidate_id = ?', (candidate_id,))
        row = self.cursor.fetchone()
        if not row:
            self.close()
            return None
            
        match = dict(row)
        
        # Parse JSON fields
        if match.get('match_details'):
            try:
                match['match_details'] = json.loads(match['match_details'])
            except json.JSONDecodeError:
                # Keep as string if not valid JSON
                pass
                
        self.close()
        return match
    def get_shortlisted_candidates_for_job(self, job_id, min_score=0.7):
        self.connect()
        self.cursor.execute('''
        SELECT m.*, c.name, c.email, c.phone, c.cv_text 
        FROM matches m
        JOIN candidates c ON m.candidate_id = c.id
        WHERE m.job_id = ? AND m.match_score >= ? AND m.is_shortlisted = 1
        ORDER BY m.match_score DESC
        ''', (job_id, min_score))
        
        shortlisted = [dict(row) for row in self.cursor.fetchall()]
        
        # Parse JSON fields for each match
        for match in shortlisted:
            if match.get('match_details'):
                try:
                    match['match_details'] = json.loads(match['match_details'])
                except json.JSONDecodeError:
                    # Keep as string if not valid JSON
                    pass
        
        self.close()
        return shortlisted
    
    def delete_match(self, match_id):
        """Delete a match from the database"""
        self.connect()
        self.cursor.execute('DELETE FROM matches WHERE id = ?', (match_id,))
        self.conn.commit()
        self.close()