import { Button } from '@/components/ui/button';
import { BriefcaseIcon, FileTextIcon, UsersIcon } from 'lucide-react';
import { Link } from 'react-router-dom';

export function HomePage() {
  return (
    <div className="relative isolate">
      <div className="mx-auto max-w-4xl text-center">
        <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
          AI-Powered Recruitment System
        </h1>
        <p className="mt-6 text-lg leading-8 text-gray-600">
          Streamline your recruitment process with our advanced AI system. Process job descriptions,
          analyze CVs, and match candidates automatically.
        </p>
        <div className="mt-10 flex items-center justify-center gap-x-6">
          <Link to="/jobs">
            <Button size="lg" className="gap-2">
              <BriefcaseIcon className="h-5 w-5" />
              Process Job Description
            </Button>
          </Link>
          <Link to="/cvs">
            <Button size="lg" variant="outline" className="gap-2">
              <FileTextIcon className="h-5 w-5" />
              Submit CV
            </Button>
          </Link>
        </div>
      </div>

      <div className="mx-auto mt-16 max-w-7xl px-6 lg:px-8">
        <div className="mx-auto grid max-w-lg grid-cols-1 gap-8 sm:grid-cols-3">
          <div className="flex flex-col items-center gap-3 rounded-xl bg-white p-6 shadow">
            <BriefcaseIcon className="h-10 w-10 text-blue-600" />
            <h3 className="text-lg font-semibold">Job Processing</h3>
            <p className="text-center text-sm text-gray-600">
              Upload and analyze job descriptions to extract key requirements and responsibilities.
            </p>
          </div>
          <div className="flex flex-col items-center gap-3 rounded-xl bg-white p-6 shadow">
            <FileTextIcon className="h-10 w-10 text-blue-600" />
            <h3 className="text-lg font-semibold">CV Analysis</h3>
            <p className="text-center text-sm text-gray-600">
              Process candidate CVs to identify skills, experience, and qualifications.
            </p>
          </div>
          <div className="flex flex-col items-center gap-3 rounded-xl bg-white p-6 shadow">
            <UsersIcon className="h-10 w-10 text-blue-600" />
            <h3 className="text-lg font-semibold">Smart Matching</h3>
            <p className="text-center text-sm text-gray-600">
              Automatically match candidates to jobs based on requirements and qualifications.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}