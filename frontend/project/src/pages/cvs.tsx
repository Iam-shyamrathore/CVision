import { PageHeader } from '@/components/layout/page-header'; // Adjusted import path
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { recruitmentApi } from '@/lib/api';
import { useMutation } from '@tanstack/react-query';
import { useForm } from 'react-hook-form';

interface CVFormData {
  name: string;
  email: string;
  phone?: string;
  cv_text: string;
}

export function CVPage() {
  const { register, handleSubmit, reset, formState: { errors } } = useForm<CVFormData>();

  const processCV = useMutation({
    mutationFn: recruitmentApi.processCV,
    onSuccess: (data) => {
      reset();
      console.log('CV processed:', data);
    },
    onError: (error) => {
      console.error('Error processing CV:', error);
    },
  });

  const onSubmit = (data: CVFormData) => {
    processCV.mutate(data);
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="CV Management"
        description="Upload and manage your CVs to match with job opportunities."
      />

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="name">
            Name
          </label>
          <Input
            id="name"
            {...register('name', { required: 'Name is required' })}
            error={errors.name?.message}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="email">
            Email
          </label>
          <Input
            id="email"
            {...register('email', { 
              required: 'Email is required', 
              pattern: {
                value: /^\S+@\S+\.\S+$/,
                message: 'Invalid email format'
              }
            })}
            error={errors.email?.message}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="phone">
            Phone (Optional)
          </label>
          <Input
            id="phone"
            {...register('phone')}
            error={errors.phone?.message}
          />
        </div>
        <div className="space-y-2">
          <label className="text-sm font-medium" htmlFor="cv_text">
            CV Text
          </label>
          <Textarea
            id="cv_text"
            rows={10}
            {...register('cv_text', { required: 'CV text is required' })}
            error={errors.cv_text?.message}
          />
        </div>

        <Button
          type="submit"
          className="w-full sm:w-auto"
          disabled={processCV.isPending}
        >
          {processCV.isPending ? 'Processing...' : 'Upload CV'}
        </Button>
      </form>

      {processCV.isSuccess && processCV.data && (
        <div className="rounded-md bg-green-50 p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-green-800">Success</h3>
              <div className="mt-2 text-sm text-green-700">
                <p>CV uploaded successfully!</p>
                <p>Candidate ID: {processCV.data.candidate_id}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {processCV.isError && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="flex">
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Error</h3>
              <div className="mt-2 text-sm text-red-700">
                <p>Failed to upload CV. {processCV.error?.message || 'Please try again.'}</p>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}