import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
});

export interface JobDescription {
  title: string;
  company: string;
  description: string;
}

export interface CV {
  name: string;
  email: string;
  phone?: string;
  cv_text: string;
}

export interface MatchRequest {
  job_id: number;
  candidate_id: number;
  threshold: number;
}

export interface InterviewRequest {
  job_id: number;
  min_score: number;
}

export const recruitmentApi = {
  // Job Descriptions
  processJob: async (data: JobDescription) => {
    const response = await api.post('/process-job', data);
    return response.data;
  },

  // CVs
  processCV: async (data: CV) => {
    const response = await api.post('/process-cv', data);
    return response.data;
  },

  // Matches
  matchCandidate: async (data: MatchRequest) => {
    const response = await api.post('/api/match-candidate', data); // Updated to match backend
    return response.data;
  },

  // Interview Requests
  generateInterviewRequests: async (data: InterviewRequest) => {
    const response = await api.post('/api/generate-interview-requests', data);
    return response.data;
  },
};