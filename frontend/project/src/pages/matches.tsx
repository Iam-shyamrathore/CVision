import { PageHeader } from '@/components/layout/page-header';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { recruitmentApi } from '@/lib/api';
import { useMutation } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';

interface MatchFormData {
  job_id: string;
  candidate_id: string;
  threshold: string;
}

interface InterviewFormData {
  job_id: string;
  min_score: string;
}

export function MatchesPage() {
  const { register: matchRegister, handleSubmit: matchHandleSubmit, formState: { errors: matchErrors }, reset: matchReset } = useForm<MatchFormData>({
    defaultValues: { threshold: '0.8' },
  });
  const { register: interviewRegister, handleSubmit: interviewHandleSubmit, formState: { errors: interviewErrors }, reset: interviewReset } = useForm<InterviewFormData>({
    defaultValues: { min_score: '0.8' },
  });
  const navigate = useNavigate();

  // Mutation for matching candidates
  const matchCandidate = useMutation({
    mutationFn: (data: { job_id: number; candidate_id: number; threshold: number }) =>
      recruitmentApi.matchCandidate({
        job_id: data.job_id,
        candidate_id: data.candidate_id,
        threshold: data.threshold,
      }),
    onSuccess: (data) => {
      console.log('Match successful:', data);
      alert(`Match ID ${data.match_id} created with score ${data.match_result.match_score}`);
      matchReset();
    },
    onError: (error: any) => {
      console.error('Error matching candidate:', error);
      alert(`Error: ${error.response?.data?.detail || 'Failed to match candidate'}`);
    },
  });

  // Mutation for generating interview requests
  const generateInterviewRequests = useMutation({
    mutationFn: (data: { job_id: number; min_score: number }) =>
      recruitmentApi.generateInterviewRequests({
        job_id: data.job_id,
        min_score: data.min_score,
      }),
    onSuccess: (data) => {
      console.log('Interview requests generated:', data);
      alert(`Generated ${data.length} interview requests`);
      interviewReset();
    },
    onError: (error: any) => {
      console.error('Error generating interview requests:', error);
      alert(`Error: ${error.response?.data?.detail || 'Failed to generate interview requests'}`);
    },
  });

  const onMatchSubmit = (data: MatchFormData) => {
    const jobId = parseInt(data.job_id, 10);
    const candidateId = parseInt(data.candidate_id, 10);
    const threshold = parseFloat(data.threshold);

    if (isNaN(jobId) || isNaN(candidateId) || isNaN(threshold)) {
      alert('Please enter valid numeric values for Job ID, Candidate ID, and Threshold.');
      return;
    }

    matchCandidate.mutate({ job_id: jobId, candidate_id: candidateId, threshold });
  };

  const onInterviewSubmit = (data: InterviewFormData) => {
    const jobId = parseInt(data.job_id, 10);
    const minScore = parseFloat(data.min_score);

    if (isNaN(jobId) || isNaN(minScore)) {
      alert('Please enter valid numeric values for Job ID and Minimum Score.');
      return;
    }

    generateInterviewRequests.mutate({ job_id: jobId, min_score: minScore });
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Matches"
        description="Match candidates to jobs and generate interview requests."
      >
        <div className="flex space-x-2">
          <Button variant="outline" onClick={() => navigate('/')}>Back to Jobs</Button>
          <Button variant="outline" onClick={() => navigate('/cv')}>Back to CVs</Button>
        </div>
      </PageHeader>

      {/* Match Candidate Form */}
      <form onSubmit={matchHandleSubmit(onMatchSubmit)} className="space-y-4 max-w-md">
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="job_id">
            Job ID
          </label>
          <Input
            id="job_id"
            type="number"
            {...matchRegister('job_id', { required: 'Job ID is required' })}
            error={matchErrors.job_id?.message}
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="candidate_id">
            Candidate ID
          </label>
          <Input
            id="candidate_id"
            type="number"
            {...matchRegister('candidate_id', { required: 'Candidate ID is required' })}
            error={matchErrors.candidate_id?.message}
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="threshold">
            Threshold (0-1)
          </label>
          <Input
            id="threshold"
            type="number"
            step="0.1"
            min="0"
            max="1"
            {...matchRegister('threshold', {
              required: 'Threshold is required',
              min: { value: 0, message: 'Must be at least 0' },
              max: { value: 1, message: 'Must be at most 1' },
            })}
            error={matchErrors.threshold?.message}
          />
        </div>

        <Button
          type="submit"
          className="w-full sm:w-auto"
          disabled={matchCandidate.isPending}
        >
          {matchCandidate.isPending ? 'Matching...' : 'Match Candidate'}
        </Button>
      </form>

      {/* Generate Interview Requests Form */}
      <form onSubmit={interviewHandleSubmit(onInterviewSubmit)} className="space-y-4 max-w-md">
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="interview_job_id">
            Job ID
          </label>
          <Input
            id="interview_job_id"
            type="number"
            {...interviewRegister('job_id', { required: 'Job ID is required' })}
            error={interviewErrors.job_id?.message}
          />
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="min_score">
            Minimum Score (0-1)
          </label>
          <Input
            id="min_score"
            type="number"
            step="0.1"
            min="0"
            max="1"
            {...interviewRegister('min_score', {
              required: 'Minimum Score is required',
              min: { value: 0, message: 'Must be at least 0' },
              max: { value: 1, message: 'Must be at most 1' },
            })}
            error={interviewErrors.min_score?.message}
          />
        </div>

        <Button
          type="submit"
          className="w-full sm:w-auto"
          disabled={generateInterviewRequests.isPending}
        >
          {generateInterviewRequests.isPending ? 'Generating...' : 'Generate Interview Requests'}
        </Button>
      </form>

      {/* Success/Error Messages for Match */}
      {matchCandidate.isSuccess && matchCandidate.data && (
        <div className="rounded-md bg-green-50 p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-green-800">Success</h3>
              <div className="mt-2 text-sm text-green-700">
                <p>Match ID: {matchCandidate.data.match_id}</p>
                <p>Score: {matchCandidate.data.match_result.match_score}</p>
                <p>Shortlisted: {matchCandidate.data.match_result.is_shortlisted ? 'Yes' : 'No'}</p>
                <p>Justification: {matchCandidate.data.match_result.justification}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {matchCandidate.isError && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>Failed to match candidate. {matchCandidate.error?.message || 'Please try again.'}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Success/Error Messages for Interview Requests */}
      {generateInterviewRequests.isSuccess && generateInterviewRequests.data && (
        <div className="rounded-md bg-green-50 p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-green-800">Success</h3>
              <div className="mt-2 text-sm text-green-700">
                {generateInterviewRequests.data.length > 0 ? (
                  generateInterviewRequests.data.map((request: any, index: number) => (
                    <div key={index}>
                      <p>Candidate: {request.candidate_name} ({request.candidate_email})</p>
                      <p>Email Content: {request.email_content}</p>
                    </div>
                  ))
                ) : (
                  <p>No interview requests generated.</p>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {generateInterviewRequests.isError && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>Failed to generate interview requests. {generateInterviewRequests.error?.message || 'Please try again.'}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}