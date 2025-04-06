from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from agents import JDSummary, CVSummary, MatchResult
from main import RecruitmentSystem
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Recruitment System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

system = RecruitmentSystem()

class JobDescriptionRequest(BaseModel):
    title: str
    company: str
    description: str

class CVRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    cv_text: str

class MatchRequest(BaseModel):
    job_id: int
    candidate_id: int
    threshold: float = 0.8

class InterviewRequest(BaseModel):
    job_id: int
    min_score: float = 0.8

@app.post("/process-job")
async def process_job(request: JobDescriptionRequest):
    try:
        job_id = system.process_job_description(
            title=request.title,
            company=request.company,
            description=request.description
        )
        if job_id is None:
            raise HTTPException(status_code=500, detail="Failed to process job description")
        job_info = system.db.get_job_description(job_id)
        return {"job_id": job_id, "summary": job_info["summary"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing job description: {str(e)}")

@app.post("/process-cv")
async def process_cv(request: CVRequest):
    try:
        logger.info(f"Processing CV: name={request.name}, email={request.email}, phone={request.phone}, cv_text={request.cv_text}")
        candidate_id = system.process_cv(
            name=request.name,
            email=request.email,
            phone=request.phone,
            cv_text=request.cv_text
        )
        if candidate_id is None:
            raise HTTPException(status_code=400, detail="Failed to process CV, email might already exist")
        logger.info(f"CV processed successfully, candidate_id={candidate_id}")
        return {"candidate_id": candidate_id}
    except Exception as e:
        logger.error(f"Error processing CV: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")

@app.post("/api/match-candidate")
async def match_candidate(request: MatchRequest):
    try:
        logger.info(f"Matching candidate_id={request.candidate_id} for job_id={request.job_id} with threshold={request.threshold}")
        match_id, match_result = system.match_candidate_to_job(
            job_id=request.job_id,
            candidate_id=request.candidate_id,
            threshold=request.threshold
        )
        if match_id is None or match_result is None:
            raise HTTPException(status_code=500, detail="Failed to calculate match")
        result_dict = {
            "match_score": match_result.match_score,
            "match_details": match_result.match_details,
            "is_shortlisted": match_result.is_shortlisted,
            "justification": match_result.justification
        }
        return {"match_id": match_id, "match_result": result_dict}
    except Exception as e:
        logger.error(f"Error matching candidate: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error matching candidate: {str(e)}")

@app.post("/api/generate-interview-requests")
async def generate_interview_requests(request: InterviewRequest):
    try:
        requests = system.generate_interview_requests(
            job_id=request.job_id,
            min_score=request.min_score
        )
        if not requests:
            return []
        return requests
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating interview requests: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)