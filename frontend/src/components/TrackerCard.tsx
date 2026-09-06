import { Link } from 'react-router-dom'
import type { Tracker } from '../api/types'

export default function TrackerCard({ tracker }: { tracker: Tracker }) {
  return (
    <Link
      to={`/trackers/${tracker.id}`}
      className="block rounded-lg border border-gray-200 bg-white p-4 hover:border-blue-300 hover:shadow-sm transition"
    >
      <div className="flex items-center justify-between">
        <h3 className="font-medium text-gray-900">{tracker.name}</h3>
        <span
          className={`rounded-full px-2 py-0.5 text-xs font-medium ${
            tracker.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'
          }`}
        >
          {tracker.is_active ? 'active' : 'paused'}
        </span>
      </div>
      <p className="mt-1 truncate text-sm text-gray-500">{tracker.url}</p>
      <p className="mt-2 text-xs text-gray-400">
        Every {tracker.poll_interval_seconds}s
        {tracker.last_run_at ? ` · last run ${new Date(tracker.last_run_at).toLocaleString()}` : ' · never run'}
      </p>
    </Link>
  )
}
