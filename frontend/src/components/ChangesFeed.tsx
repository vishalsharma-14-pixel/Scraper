import { useEffect, useState } from 'react'
import { listChangeEvents } from '../api/changeEvents'
import type { ChangeEvent } from '../api/types'

function formatValue(value: unknown): string {
  if (value === null || value === undefined) return '—'
  return String(value)
}

export default function ChangesFeed({ trackerId }: { trackerId?: string }) {
  const [events, setEvents] = useState<ChangeEvent[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    listChangeEvents({ trackerId, limit: 20 })
      .then((data) => {
        if (!cancelled) setEvents(data)
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [trackerId])

  if (loading) return <p className="text-sm text-gray-400">Loading changes…</p>
  if (events.length === 0) return <p className="text-sm text-gray-400">No changes detected yet.</p>

  return (
    <ul className="divide-y divide-gray-100">
      {events.map((event) => (
        <li key={event.id} className="py-2 text-sm">
          <div className="flex items-center justify-between">
            <span className="font-medium text-gray-800">{event.field_name}</span>
            <span className="text-xs text-gray-400">{new Date(event.detected_at).toLocaleString()}</span>
          </div>
          <p className="text-gray-500">
            {event.change_type === 'first_seen' ? (
              <>baseline: {formatValue(event.new_value)}</>
            ) : (
              <>
                {formatValue(event.old_value)} → {formatValue(event.new_value)}
              </>
            )}
          </p>
        </li>
      ))}
    </ul>
  )
}
