import { PageHeader } from '@/components/layout/page-header';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { recruitmentApi } from '@/lib/api';
import { useMutation } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';

interface JobFormData {
  title: string;
  company: string;
  description: string;
}

export function JobDescriptionPage() {
  const { register, handleSubmit, reset, formState: { errors } } = useForm<JobFormData>();

  const processJob = useMutation({
    mutationFn: recruitmentApi.processJob,
    onSuccess: (data: { job_id: number; summary: string }) => {
      reset();
      console.log('Job processed:', data);
    },
    onError: (error: any) => {
      console.error('Error processing job:', error);
    },
  });
  const onSubmit = (data: JobFormData) => {
    processJob.mutate(data);
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Process Job Description"
        description="Enter the job details below to analyze and extract key information."
      />

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="grid gap-4 sm:grid-cols-2">
          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="title">
              Job Title
            </label>
            <Input
              id="title"
              {...register('title', { required: 'Job title is required' })}
              error={errors.title?.message}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium" htmlFor="company">
              Company Name
            </label>
            <Input
              id="company"
              {...register('company', { required: 'Company name is required' })}
              error={errors.company?.message}
            />
          </div>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="description">
            Job Description
          </label>
          <Textarea
            id="description"
            rows={10}
            {...register('description', { required: 'Job description is required' })}
            error={errors.description?.message}
          />
        </div>

        <Button
          type="submit"
          className="w-full sm:w-auto"
          disabled={processJob.isPending}
        >
          {processJob.isPending ? 'Processing...' : 'Process Job Description'}
        </Button>
      </form>

      {processJob.isSuccess && processJob.data && (
        <div className="rounded-md bg-green-50 p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-green-800">Success</h3>
              <div className="mt-2 text-sm text-green-700">
                <p>Job description processed successfully!</p>
                <p>Job ID: {processJob.data.job_id}</p>
                <p>Summary: {processJob.data.summary}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {processJob.isError && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>Failed to process job description. {processJob.error?.message || 'Please try again.'}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}