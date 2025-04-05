import argparse
import os
import sys
from main import RecruitmentSystem

def read_multiline_input(prompt):
    """Read multiline input from the user"""
    print(prompt)
    print("(Type your content, then press Enter followed by Ctrl+D on Unix/Linux or Ctrl+Z then Enter on Windows)")
    content = ""
    try:
        while True:
            line = input()
            content += line + "\n"
    except EOFError:
        pass
    return content

def process_job_description(system, args):
    """Process a job description"""
    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File {args.file} not found")
            return
        with open(args.file, 'r') as f:
            description = f.read()
    else:
        title = input("Enter job title: ")
        company = input("Enter company name: ")
        description = read_multiline_input("Enter job description:")
        
    job_id = system.process_job_description(
        title=args.title if args.title else title,
        company=args.company if args.company else company,
        description=description
    )
    
    if job_id:
        print(f"Job description processed successfully with ID: {job_id}")
    else:
        print("Failed to process job description")

def process_cv(system, args):
    """Process a CV"""
    if args.file:
        if not os.path.exists(args.file):
            print(f"Error: File {args.file} not found")
            return
        with open(args.file, 'r') as f:
            cv_text = f.read()
    else:
        name = input("Enter candidate name: ")
        email = input("Enter candidate email: ")
        phone = input("Enter candidate phone (optional): ")
        cv_text = read_multiline_input("Enter CV text:")
        
    candidate_id = system.process_cv(
        name=args.name if args.name else name,
        email=args.email if args.email else email,
        phone=args.phone if args.phone else phone,
        cv_text=cv_text
    )
    
    if candidate_id:
        print(f"CV processed successfully with ID: {candidate_id}")
    else:
        print("Failed to process CV")

def match_candidate(system, args):
    """Match a candidate to a job"""
    job_id = args.job_id
    candidate_id = args.candidate_id
    threshold = args.threshold
    
    match_id, match_result = system.match_candidate_to_job(job_id, candidate_id, threshold)
    
    if match_id:
        print(f"Match processed successfully with ID: {match_id}")
        print(f"Match score: {match_result.match_score}")
        print(f"Shortlisted: {match_result.is_shortlisted}")
        print(f"Justification: {match_result.justification}")
    else:
        print("Failed to match candidate to job")

def generate_interviews(system, args):
    """Generate interview requests"""
    job_id = args.job_id
    min_score = args.min_score
    
    requests = system.generate_interview_requests(job_id, min_score)
    
    if requests:
        print(f"Generated {len(requests)} interview requests:")
        for i, req in enumerate(requests, 1):
            print(f"\n--- Interview Request {i} ---")
            print(f"Candidate: {req['candidate_name']} ({req['candidate_email']})")
            print("Email Content:")
            print(req['email_content'])
            print("-" * 40)
    else:
        print("No interview requests generated")

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="AI Recruitment System CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Job Description Parser
    jd_parser = subparsers.add_parser("job", help="Process a job description")
    jd_parser.add_argument("--title", help="Job title")
    jd_parser.add_argument("--company", help="Company name")
    jd_parser.add_argument("--file", help="Path to job description file")
    
    # CV Parser
    cv_parser = subparsers.add_parser("cv", help="Process a CV")
    cv_parser.add_argument("--name", help="Candidate name")
    cv_parser.add_argument("--email", help="Candidate email")
    cv_parser.add_argument("--phone", help="Candidate phone")
    cv_parser.add_argument("--file", help="Path to CV file")
    
    # Match Parser
    match_parser = subparsers.add_parser("match", help="Match a candidate to a job")
    match_parser.add_argument("job_id", type=int, help="Job ID")
    match_parser.add_argument("candidate_id", type=int, help="Candidate ID")
    match_parser.add_argument("--threshold", type=float, default=0.8, help="Matching threshold (0.0-1.0)")
    
    # Interview Parser
    interview_parser = subparsers.add_parser("interview", help="Generate interview requests")
    interview_parser.add_argument("job_id", type=int, help="Job ID")
    interview_parser.add_argument("--min-score", type=float, default=0.8, help="Minimum match score (0.0-1.0)")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Initialize the system
    system = RecruitmentSystem()
    
    # Route to the appropriate function
    if args.command == "job":
        process_job_description(system, args)
    elif args.command == "cv":
        process_cv(system, args)
    elif args.command == "match":
        match_candidate(system, args)
    elif args.command == "interview":
        generate_interviews(system, args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()