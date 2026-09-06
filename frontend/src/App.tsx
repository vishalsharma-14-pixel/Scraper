import { BrowserRouter, Link, Navigate, Route, Routes } from 'react-router-dom'
import TrackersList from './pages/TrackersList'
import TrackerDetail from './pages/TrackerDetail'
import TrackerForm from './pages/TrackerForm'
import JobRunsPage from './pages/JobRunsPage'

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-50">
        <nav className="border-b border-gray-200 bg-white px-4 py-3">
          <div className="mx-auto flex max-w-5xl items-center gap-6">
            <Link to="/" className="font-semibold text-gray-900">
              Scraping + Tracking
            </Link>
            <Link to="/" className="text-sm text-gray-600 hover:text-gray-900">
              Trackers
            </Link>
            <Link to="/jobs" className="text-sm text-gray-600 hover:text-gray-900">
              Job Runs
            </Link>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={<TrackersList />} />
          <Route path="/trackers/new" element={<TrackerForm />} />
          <Route path="/trackers/:id" element={<TrackerDetail />} />
          <Route path="/trackers/:id/edit" element={<TrackerForm />} />
          <Route path="/jobs" element={<JobRunsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
