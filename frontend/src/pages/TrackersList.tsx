import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { listTrackers } from '../api/trackers'
import { apiErrorMessage } from '../api/client'
import type { Tracker } from '../api/types'
import TrackerCard from '../components/TrackerCard'
import ChangesFeed from '../components/ChangesFeed'

export default function TrackersList() {
  const [trackers, setTrackers] = useState<Tracker[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    listTrackers()
      .then(setTrackers)
      .catch((e) => setError(apiErrorMessage(e)))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="mx-auto max-w-5xl px-4 py-8">
      <div className="flex items-center justify-between">
        <h1 className="text-xl font-semibold text-gray-900">Trackers</h1>
        <Link
          to="/trackers/new"
          className="rounded-md bg-blue-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-blue-700"
        >
          + New Tracker
        </Link>
      </div>

      <div className="mt-6 grid grid-cols-1 gap-6 md:grid-cols-3">
        <div className="md:col-span-2 space-y-3">
          {loading && <p className="text-sm text-gray-400">Loading trackers…</p>}
          {error && <p className="text-sm text-red-500">{error}</p>}
          {!loading && trackers.length === 0 && (
            <p className="text-sm text-gray-400">No trackers yet — create one to get started.</p>
          )}
          {trackers.map((tracker) => (
            <TrackerCard key={tracker.id} tracker={tracker} />
          ))}
        </div>
        <div className="rounded-lg border border-gray-200 bg-white p-4">
          <h2 className="mb-2 text-sm font-semibold text-gray-700">Recent changes</h2>
          <ChangesFeed />
        </div>
      </div>
    </div>
  )
}
