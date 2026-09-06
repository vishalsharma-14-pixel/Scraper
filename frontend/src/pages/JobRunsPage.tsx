import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listJobRuns } from '../api/jobRuns'
import type { JobRun } from '../api/types'
import JobStatusBadge from '../components/JobStatusBadge'

export default function JobRunsPage() {
  const [jobs, setJobs] = useState<JobRun[]>([])

  useEffect(() => {
    function load() {
      listJobRuns({ limit: 100 }).then(setJobs)
    }
    load()
    const interval = setInterval(load, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <h1 className="text-xl font-semibold text-gray-900">Job Runs</h1>
      <div className="mt-4 overflow-x-auto rounded-lg border border-gray-200 bg-white">
        <table className="min-w-full text-sm">
          <thead>
            <tr className="border-b border-gray-100 text-left text-xs text-gray-400">
              <th className="px-4 py-2">Tracker</th>
              <th className="px-4 py-2">Status</th>
              <th className="px-4 py-2">Trigger</th>
              <th className="px-4 py-2">Method</th>
              <th className="px-4 py-2">Created</th>
              <th className="px-4 py-2">Error</th>
            </tr>
          </thead>
          <tbody>
            {jobs.map((job) => (
              <tr key={job.id} className="border-b border-gray-50">
                <td className="px-4 py-2">
                  <Link to={`/trackers/${job.tracker_id}`} className="text-blue-600">
                    {job.tracker_id.slice(0, 8)}…
                  </Link>
                </td>
                <td className="px-4 py-2">
                  <JobStatusBadge status={job.status} />
                </td>
                <td className="px-4 py-2 text-gray-500">{job.trigger}</td>
                <td className="px-4 py-2 text-gray-500">{job.fetch_method_used ?? '—'}</td>
                <td className="px-4 py-2 text-gray-500">{new Date(job.created_at).toLocaleString()}</td>
                <td className="px-4 py-2 text-red-500">{job.error_message ?? ''}</td>
              </tr>
            ))}
            {jobs.length === 0 && (
              <tr>
                <td colSpan={6} className="px-4 py-4 text-center text-gray-400">
                  No job runs yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}
