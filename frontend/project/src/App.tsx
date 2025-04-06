import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import { Navbar } from './components/layout/navbar';
import { HomePage } from './pages/home';
import { JobDescriptionPage } from './pages/jobs';
import { CVPage } from './pages/cvs';
import { MatchesPage } from './pages/matches';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/jobs" element={<JobDescriptionPage />} />
              <Route path="/cvs" element={<CVPage />} />
              <Route path="/matches" element={<MatchesPage />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;