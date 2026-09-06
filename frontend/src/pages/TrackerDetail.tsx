import { useCallback, useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import {
  deleteTracker,
  getTracker,
  listTrackerJobs,
  listTrackerSnapshots,
  runTrackerNow,
} from '../api/trackers'
import { apiErrorMessage } from '../api/client'
import type { JobRun, Snapshot, Tracker } from '../api/types'
import ChangesFeed from '../components/ChangesFeed'
import JobStatusBadge from '../components/JobStatusBadge'
import SnapshotHistoryTable from '../components/SnapshotHistoryTable'
import SparklineChart from '../components/SparklineChart'

export default function TrackerDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()

  const [tracker, setTracker] = useState<Tracker | null>(null)
  const [snapshots, setSnapshots] = useState<Snapshot[]>([])
  const [jobs, setJobs] = useState<JobRun[]>([])
  const [error, setError] = useState('')
  const [running, setRunning] = useState(false)

  const load = useCallback(() => {
    if (!id) return
    getTracker(id).then(setTracker).catch((e) => setError(apiErrorMessage(e)))
    listTrackerSnapshots(id).then(setSnapshots)
    listTrackerJobs(id).then(setJobs)
  }, [id])

  useEffect(() => {
    load()
  }, [load])

  useEffect(() => {
    const hasInFlight = jobs.some((j) => j.status === 'pending' || j.status === 'running')
    if (!hasInFlight) return
    const interval = setInterval(load, 3000)
    return () => clearInterval(interval)
  }, [jobs, load])

  async function handleRunNow() {
    if (!id) return
    setRunning(true)
    try {
      await runTrackerNow(id)
      load()
    } catch (e) {
      setError(apiErrorMessage(e))
    } finally {
      setRunning(false)
    }
  }

  async function handleDelete() {
    if (!id) return
    if (!confirm('Delete this tracker and all its history?')) return
    await deleteTracker(id)
    navigate('/')
  }

  if (error) return <p className="mx-auto max-w-4xl px-4 py-8 text-sm text-red-500">{error}</p>
  if (!tracker) return <p className="mx-auto max-w-4xl px-4 py-8 text-sm text-gray-400">Loading…</p>

  const latest = snapshots[0]
  const priceFieldName = Object.entries(tracker.extraction_config).find(
    ([, cfg]) => cfg.type === 'price' || cfg.type === 'number',
  )?.[0]
  const priceHistory = priceFieldName
    ? snapshots
        .slice()
        .reverse()
        .map((s) => s.normalized_values[priceFieldName])
        .filter((v): v is number => typeof v === 'number' && !Number.isNaN(v))
    : []

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-xl font-semibold text-gray-900">{tracker.name}</h1>
          <a href={tracker.url} target="_blank" rel="noreferrer" className="text-sm text-blue-600">
            {tracker.url}
          </a>
        </div>
        <div className="flex gap-2">
          <button
            onClick={handleRunNow}
            disabled={running}
            className="rounded-md bg-blue-600 px-3 py-1.5 text-sm font-medium text-white disabled:opacity-50"
          >
            {running ? 'Running…' : 'Run now'}
          </button>
          <Link
            to={`/trackers/${tracker.id}/edit`}
            className="rounded-md border border-gray-300 px-3 py-1.5 text-sm text-gray-700"
          >
            Edit
          </Link>
          <button onClick={handleDelete} className="rounded-md border border-red-300 px-3 py-1.5 text-sm text-red-600">
            Delete
          </button>
        </div>
      </div>

      {latest && (
        <div className="mt-6 rounded-lg border border-gray-200 bg-white p-4">
          <h2 className="mb-2 text-sm font-semibold text-gray-700">Current values</h2>
          <div className="flex flex-wrap gap-6">
            {Object.entries(latest.normalized_values).map(([field, value]) => (
              <div key={field}>
                <p className="text-xs text-gray-400">{field}</p>
                <p className="text-lg font-medium text-gray-900">{String(value ?? '—')}</p>
              </div>
            ))}
          </div>
          {priceHistory.length >= 2 && (
            <div className="mt-4">
              <p className="mb-1 text-xs text-gray-400">{priceFieldName} history</p>
              <SparklineChart values={priceHistory} />
            </div>
          )}
        </div>
      )}

      <div className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-2">
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <h2 className="mb-2 text-sm font-semibold text-gray-700">Change history</h2>
          <ChangesFeed trackerId={tracker.id} />
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <h2 className="mb-2 text-sm font-semibold text-gray-700">Job runs</h2>
          <ul className="divide-y divide-gray-100 text-sm">
            {jobs.map((job) => (
              <li key={job.id} className="flex items-center justify-between py-2">
                <div>
                  <JobStatusBadge status={job.status} />
                  <span className="ml-2 text-gray-500">{job.trigger}</span>
                  {job.error_message && (
                    <p className="text-xs text-red-500">{job.error_message}</p>
                  )}
                </div>
                <span className="text-xs text-gray-400">
                  {new Date(job.created_at).toLocaleString()}
                </span>
              </li>
            ))}
            {jobs.length === 0 && <p className="text-sm text-gray-400">No jobs yet.</p>}
          </ul>
        </div>
      </div>

      <div className="mt-6 rounded-lg border border-gray-200 bg-white p-4">
        <h2 className="mb-2 text-sm font-semibold text-gray-700">Snapshot history</h2>
        <SnapshotHistoryTable snapshots={snapshots} />
      </div>
    </div>
  )
}
