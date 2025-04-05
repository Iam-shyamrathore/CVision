import json
import re
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union, Any
import os


os.environ["GOOGLE_API_KEY"] = "AIzaSyD4DzmDJxzxSWkoBucfBhgPGfPxlJmRDdY"

class JDSummary(BaseModel):
    title: str = Field(description="Job title")
    required_skills: List[str] = Field(description="List of required skills")
    required_experience: str = Field(description="Required years of experience and type")
    required_qualifications: str = Field(description="Required educational qualifications")
    responsibilities: List[str] = Field(description="Key job responsibilities")
    summary: str = Field(description="Brief summary of the job")

class CVSummary(BaseModel):
    name: str = Field(description="Candidate name")
    education: List[Dict[str, str]] = Field(description="Educational background")
    experience: List[Dict[str, str]] = Field(description="Work experience")
    skills: List[str] = Field(description="Skills and technologies")
    certifications: List[str] = Field(description="Certifications and qualifications")

class MatchResult(BaseModel):
    match_score: float = Field(description="Match score between 0 and 1")
    match_details: Dict[str, Any] = Field(description="Matching details by category")
    is_shortlisted: bool = Field(description="Whether the candidate should be shortlisted")
    justification: str = Field(description="Justification for the match score and shortlisting decision")

class JobDescriptionAgent:
    def __init__(self, model_name="gemini-2.0-flash-lite"):
        self.model = ChatGoogleGenerativeAI(model=model_name, temperature=0.2)
        self.parser = PydanticOutputParser(pydantic_object=JDSummary)
    
    def summarize_jd(self, jd_text):
        prompt_template = """
        You are an AI assistant specialized in analyzing job descriptions. 
        Given the following job description, extract the key information and format it according to the specified JSON schema.
        
        Job Description:
        {jd_text}
        
        {format_instructions}
        
        Ensure the output is properly formatted as JSON.
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["jd_text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        chain = prompt | self.model | self.parser
        
        try:
            result = chain.invoke({"jd_text": jd_text})
            return result
        except Exception as e:
            print(f"Error parsing JD: {e}")
            # Fallback mechanism for parsing
            try:
                # Try direct LLM call with simple JSON extraction
                response = self.model.invoke(
                    f"Analyze this job description and output ONLY a JSON with the following fields: title, required_skills (array), required_experience (string), required_qualifications (string), responsibilities (array), summary (string). Job Description: {jd_text}"
                )
                # Extract JSON from response
                match = re.search(r'```json\n(.*?)\n```', response.content, re.DOTALL)
                if match:
                    json_str = match.group(1)
                else:
                    json_str = response.content
                
                # Clean and parse the JSON
                json_str = re.sub(r'[\n\t]', '', json_str)
                result = json.loads(json_str)
                return JDSummary(**result)
            except Exception as inner_e:
                print(f"Fallback parsing failed: {inner_e}")
                return None

class CVAnalysisAgent:
    def __init__(self, model_name="gemini-2.0-flash-lite"):
        self.model = ChatGoogleGenerativeAI(model=model_name, temperature=0.2)
        self.parser = PydanticOutputParser(pydantic_object=CVSummary)
    
    def extract_cv_info(self, cv_text):
        prompt_template = """
        You are an AI assistant specialized in analyzing resumes and CVs. 
        Given the following CV, extract the key information and format it according to the specified JSON schema.
        
        CV:
        {cv_text}
        
        {format_instructions}
        
        Ensure the output is properly formatted as JSON.
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["cv_text"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        chain = prompt | self.model | self.parser
        
        try:
            result = chain.invoke({"cv_text": cv_text})
            return result
        except Exception as e:
            print(f"Error parsing CV: {e}")
            # Fallback mechanism for parsing
            try:
                # Try direct LLM call with simple JSON extraction
                response = self.model.invoke(
                    f"Analyze this CV and output ONLY a JSON with the following fields: name, education (array of objects), experience (array of objects), skills (array), certifications (array). CV: {cv_text}"
                )
                # Extract JSON from response
                match = re.search(r'```json\n(.*?)\n```', response.content, re.DOTALL)
                if match:
                    json_str = match.group(1)
                else:
                    json_str = response.content
                
                # Clean and parse the JSON
                json_str = re.sub(r'[\n\t]', '', json_str)
                result = json.loads(json_str)
                return CVSummary(**result)
            except Exception as inner_e:
                print(f"Fallback parsing failed: {inner_e}")
                return None

class RecruitingMatchAgent:
    def __init__(self, model_name="gemini-2.0-flash-lite"):
        self.model = ChatGoogleGenerativeAI(model=model_name, temperature=0.2)
        self.parser = PydanticOutputParser(pydantic_object=MatchResult)
    
    def calculate_match(self, jd_summary, cv_summary, threshold=0.8):
        prompt_template = """
        You are an AI assistant specialized in matching job candidates to job descriptions. 
        Analyze the job description and candidate information below and determine how well the candidate matches the job requirements.
        
        Job Description:
        {jd_summary}
        
        Candidate Information:
        {cv_summary}
        
        Calculate a match score between 0 and 1, where 1 is a perfect match. 
        Consider skills, experience, education, and other relevant factors.
        A candidate should be shortlisted if their match score is {threshold} or higher.
        
        {format_instructions}
        
        Ensure the output is properly formatted as JSON.
        """
        
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["jd_summary", "cv_summary", "threshold"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
        chain = prompt | self.model | self.parser
        
        try:
            result = chain.invoke({
                "jd_summary": json.dumps(jd_summary.model_dump() if hasattr(jd_summary, "model_dump") else jd_summary), 
                "cv_summary": json.dumps(cv_summary.model_dump() if hasattr(cv_summary, "model_dump") else cv_summary), 
                "threshold": threshold
            })
            return result
        except Exception as e:
            print(f"Error calculating match: {e}")
            # Fallback mechanism for parsing
            try:
                # Try direct LLM call with simple JSON extraction
                response = self.model.invoke(
                    f"""Analyze this job description and candidate information and output ONLY a JSON with the following fields: 
                    match_score (float between 0-1), 
                    match_details (object), 
                    is_shortlisted (boolean), 
                    justification (string).
                    
                    Job Description: {json.dumps(jd_summary)}
                    
                    Candidate Information: {json.dumps(cv_summary)}
                    
                    A candidate should be shortlisted if their match score is {threshold} or higher.
                    """
                )
                # Extract JSON from response
                match = re.search(r'```json\n(.*?)\n```', response.content, re.DOTALL)
                if match:
                    json_str = match.group(1)
                else:
                    json_str = response.content
                
                # Clean and parse the JSON
                json_str = re.sub(r'[\n\t]', '', json_str)
                result = json.loads(json_str)
                return MatchResult(**result)
            except Exception as inner_e:
                print(f"Fallback parsing failed: {inner_e}")
                return None

class InterviewSchedulerAgent:
    def __init__(self, model_name="gemini-2.0-flash-lite"):
        self.model = ChatGoogleGenerativeAI(model=model_name, temperature=0.7)
    
    def generate_interview_request(self, job_info, candidate_info, match_result):
        prompt = f"""
        You are an AI assistant specialized in HR communications. 
        Create a personalized interview request email for a candidate based on the information below.
        
        Job Information:
        {json.dumps(job_info)}
        
        Candidate Information:
        {json.dumps(candidate_info)}
        
        Match Result:
        {json.dumps(match_result)}
        
        Generate a professional email inviting the candidate for an interview. 
        Include the following details:
        1. Congratulatory message for being shortlisted
        2. Brief mention of why they are a good fit
        3. Suggestion of potential interview formats (video, in-person, or phone)
        4. Request for their availability in the next week
        5. Contact information for scheduling
        
        Format the email with appropriate subject line, greeting, body, and closing.
        """
        
        try:
            response = self.model.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"Error generating interview request: {e}")
            return None

# Example usage
def run_recruitment_pipeline(jd_text, cv_text, shortlist_threshold=0.7):
    """
    Run the complete recruitment pipeline from JD analysis to interview scheduling
    
    Args:
        jd_text (str): The job description text
        cv_text (str): The CV/resume text
        shortlist_threshold (float): Threshold for shortlisting candidates (0-1)
        
    Returns:
        dict: Results of the recruitment process
    """
    # Initialize agents
    jd_agent = JobDescriptionAgent()
    cv_agent = CVAnalysisAgent()
    match_agent = RecruitingMatchAgent()
    scheduler_agent = InterviewSchedulerAgent()
    
    # Process job description
    jd_summary = jd_agent.summarize_jd(jd_text)
    if not jd_summary:
        return {"status": "error", "message": "Failed to process job description"}
    
    # Process CV
    cv_summary = cv_agent.extract_cv_info(cv_text)
    if not cv_summary:
        return {"status": "error", "message": "Failed to process CV"}
    
    # Calculate match
    match_result = match_agent.calculate_match(jd_summary, cv_summary, shortlist_threshold)
    if not match_result:
        return {"status": "error", "message": "Failed to calculate match"}
    
    # Generate email if shortlisted
    email_content = None
    if match_result.is_shortlisted:
        email_content = scheduler_agent.generate_interview_request(
            jd_summary.dict() if hasattr(jd_summary, "dict") else jd_summary, 
            cv_summary.dict() if hasattr(cv_summary, "dict") else cv_summary, 
            match_result.dict() if hasattr(match_result, "dict") else match_result
        )
    
    # Return results
    return {
        "status": "success",
        "job_summary": jd_summary,
        "candidate_summary": cv_summary,
        "match_result": match_result,
        "interview_email": email_content if match_result.is_shortlisted else None,
        "is_shortlisted": match_result.is_shortlisted
    }

# If you want to use this as a script
if __name__ == "__main__":
    # Example - you would replace these with actual job descriptions and CVs
    job_description = """
    Senior Software Engineer
    We are looking for a Senior Software Engineer to join our team. You will be responsible for designing, developing, and maintaining software applications.
    Requirements:
    - 5+ years of experience in software development
    - Proficiency in Python, JavaScript, and SQL
    - Experience with cloud platforms (AWS/Azure/GCP)
    - Bachelor's degree in Computer Science or related field
    - Strong problem-solving skills
    Responsibilities:
    - Design and implement software solutions
    - Write clean, maintainable code
    - Code review and mentoring junior developers
    - Collaborate with product managers and designers
    """
    
    candidate_cv = """
    John Doe
    Software Engineer
    
    Education:
    - Master's in Computer Science, Stanford University, 2018
    - Bachelor's in Computer Engineering, MIT, 2016
    
    Experience:
    - Senior Developer at Tech Solutions Inc. (2020-Present)
      * Led team of 5 developers on cloud migration project
      * Implemented CI/CD pipeline reducing deployment time by 70%
    
    - Software Engineer at CodeCorp (2018-2020)
      * Developed RESTful APIs using Django
      * Optimized database queries improving performance by 40%
    
    Skills:
    - Programming Languages: Python, JavaScript, Java, SQL
    - Frameworks: Django, React, Node.js
    - Cloud: AWS (EC2, S3, Lambda), Docker, Kubernetes
    - Tools: Git, JIRA, Jenkins
    
    Certifications:
    - AWS Certified Developer
    - Certified Scrum Master
    """
    
    result = run_recruitment_pipeline(job_description, candidate_cv)
    print(json.dumps(result, indent=2))