from agents import JobDescriptionAgent, CVAnalysisAgent, RecruitingMatchAgent, InterviewSchedulerAgent
from database import RecruitmentDB
import json
from langchain_google_genai import ChatGoogleGenerativeAI

class RecruitmentSystem:
    def __init__(self, model_name="gemini-2.0-flash-lite"):
        self.db = RecruitmentDB()
        try:
            test_model = ChatGoogleGenerativeAI(model=model_name, temperature=0.2)
            response = test_model.invoke("Test model availability")
            print(f"Model '{model_name}' is valid and will be used. Test response: {response.content[:20]}...")
        except Exception as e:
            print(f"Warning: Model '{model_name}' failed with error: {e}")
            print("Falling back to 'gemini-pro' as default model.")
            model_name = "gemini-pro"
        
        self.jd_agent = JobDescriptionAgent(model_name)
        self.cv_agent = CVAnalysisAgent(model_name)
        self.match_agent = RecruitingMatchAgent(model_name)
        self.scheduler_agent = InterviewSchedulerAgent(model_name)
    
    def process_job_description(self, title, company, description):
        jd_summary = self.jd_agent.summarize_jd(description)
        
        if not jd_summary:
            print("Failed to summarize job description")
            return None
        
        job_id = self.db.add_job_description(
            title=title,
            company=company,
            description=description,
            summary=jd_summary.summary,
            required_skills=json.dumps(jd_summary.required_skills),
            required_experience=jd_summary.required_experience,
            required_qualifications=jd_summary.required_qualifications,
            responsibilities=json.dumps(jd_summary.responsibilities)
        )
        
        if job_id:
            print(f"Job description processed and stored with ID: {job_id}")
            print(f"Summary: {jd_summary.summary[:50]}...")  # Preview summary
        else:
            print("Failed to store job description in database")
        return job_id

    def process_cv(self, name, email, cv_text, phone=None):
        """Process a CV and store it in the database"""
        # Step 1: Extract information from CV
        cv_summary = self.cv_agent.extract_cv_info(cv_text)
        
        if not cv_summary:
            print("Failed to extract CV information")
            return None
        
        # Step 2: Store in database
        candidate_id = self.db.add_candidate(
            name=name,
            email=email,
            phone=phone,
            cv_text=cv_text,
            education=json.dumps(cv_summary.education),
            experience=json.dumps(cv_summary.experience),
            skills=json.dumps(cv_summary.skills),
            certifications=json.dumps(cv_summary.certifications)
        )
        
        if not candidate_id:
            print(f"Failed to add candidate {email}, might already exist")
            return None
            
        print(f"CV processed and stored with ID: {candidate_id}")
        return candidate_id
    
    def match_candidate_to_job(self, job_id, candidate_id, threshold=0.8):
        """Match a candidate to a job description"""
        # Step 1: Retrieve job and candidate information
        job_info = self.db.get_job_description(job_id)
        candidate_info = self.db.get_candidate(candidate_id)
        
        if not job_info or not candidate_info:
            print("Failed to retrieve job or candidate information")
            return None
        
        # Step 2: Calculate match
        match_result = self.match_agent.calculate_match(job_info, candidate_info, threshold)
        
        if not match_result:
            print("Failed to calculate match")
            return None
        
        # Step 3: Store match result
        match_id = self.db.add_match(
            job_id=job_id,
            candidate_id=candidate_id,
            match_score=match_result.match_score,
            match_details=json.dumps(match_result.match_details)
        )
        
        # Step 4: Update shortlisting status
        self.db.update_match_status(
            match_id=match_id,
            is_shortlisted=match_result.is_shortlisted
        )
        
        print(f"Match processed and stored with ID: {match_id}")
        print(f"Match score: {match_result.match_score}, Shortlisted: {match_result.is_shortlisted}")
        return match_id, match_result
    
    def generate_interview_requests(self, job_id, min_score=0.8):
        """Generate interview requests for shortlisted candidates"""
        # Step 1: Get all shortlisted candidates
        shortlisted = self.db.get_shortlisted_candidates_for_job(job_id, min_score)
        
        if not shortlisted:
            print("No shortlisted candidates found")
            return []
        
        # Step 2: Generate interview request for each shortlisted candidate
        requests = []
        job_info = self.db.get_job_description(job_id)
        
        for candidate in shortlisted:
            match_info = self.db.get_match(candidate['id'])
            
            # Generate interview request
            email_content = self.scheduler_agent.generate_interview_request(
                job_info=job_info,
                candidate_info=candidate,
                match_result=match_info
            )
            
            if email_content:
                # Update database to mark interview request as sent
                self.db.update_match_status(
                    match_id=candidate['id'],
                    interview_requested=True
                )
                
                requests.append({
                    'candidate_id': candidate['candidate_id'],
                    'candidate_name': candidate['name'],
                    'candidate_email': candidate['email'],
                    'email_content': email_content
                })
        
        print(f"Generated {len(requests)} interview requests")
        return requests

# Simple example usage
if __name__ == "__main__":
    # Initialize the system
    system = RecruitmentSystem()
    
    print("Welcome to the AI Recruitment System!")
    print("1. Process a Job Description")
    print("2. Process a CV")
    print("3. Match a Candidate to a Job")
    print("4. Generate Interview Requests")
    
    choice = input("Enter your choice (1-4): ")
    
    if choice == "1":
        title = input("Enter job title: ")
        company = input("Enter company name: ")
        print("Enter job description (press Enter then Ctrl+D on Unix/Linux or Ctrl+Z then Enter on Windows to finish):")
        description = ""
        try:
            while True:
                line = input()
                description += line + "\n"
        except EOFError:
            pass
        
        job_id = system.process_job_description(title, company, description)
        print(f"Job processed with ID: {job_id}")
        
    elif choice == "2":
        name = input("Enter candidate name: ")
        email = input("Enter candidate email: ")
        phone = input("Enter candidate phone (optional): ")
        print("Enter CV text (press Enter then Ctrl+D on Unix/Linux or Ctrl+Z then Enter on Windows to finish):")
        cv_text = ""
        try:
            while True:
                line = input()
                cv_text += line + "\n"
        except EOFError:
            pass
        
        candidate_id = system.process_cv(name, email, cv_text, phone)
        print(f"CV processed with ID: {candidate_id}")
        
    elif choice == "3":
        job_id = int(input("Enter job ID: "))
        candidate_id = int(input("Enter candidate ID: "))
        threshold = float(input("Enter matching threshold (0.0-1.0, default 0.8): ") or "0.8")
        
        match_result = system.match_candidate_to_job(job_id, candidate_id, threshold)
        print(f"Match result: {match_result}")
        
    elif choice == "4":
        job_id = int(input("Enter job ID: "))
        min_score = float(input("Enter minimum match score (0.0-1.0, default 0.8): ") or "0.8")
        
        requests = system.generate_interview_requests(job_id, min_score)
        for i, req in enumerate(requests, 1):
            print(f"\n--- Interview Request {i} ---")
            print(f"Candidate: {req['candidate_name']} ({req['candidate_email']})")
            print("Email Content:")
            print(req['email_content'])
            print("-" * 40)
    
    else:
        print("Invalid choice")