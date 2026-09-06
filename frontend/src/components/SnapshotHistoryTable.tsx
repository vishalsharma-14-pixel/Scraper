import type { Snapshot } from '../api/types'

function formatValue(value: unknown): string {
  if (value === null || value === undefined) return '—'
  return String(value)
}

export default function SnapshotHistoryTable({ snapshots }: { snapshots: Snapshot[] }) {
  if (snapshots.length === 0) {
    return <p className="text-sm text-gray-400">No snapshots yet.</p>
  }

  const fieldNames = Array.from(
    new Set(snapshots.flatMap((s) => Object.keys(s.normalized_values))),
  )

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full text-sm">
        <thead>
          <tr className="text-left text-xs text-gray-400">
            <th className="py-1 pr-4">Scraped at</th>
            <th className="py-1 pr-4">Method</th>
            {fieldNames.map((name) => (
              <th key={name} className="py-1 pr-4">
                {name}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {snapshots.map((snapshot) => (
            <tr key={snapshot.id} className="border-t border-gray-100">
              <td className="py-1 pr-4 whitespace-nowrap">
                {new Date(snapshot.scraped_at).toLocaleString()}
              </td>
              <td className="py-1 pr-4 text-gray-500">{snapshot.fetch_method}</td>
              {fieldNames.map((name) => (
                <td key={name} className="py-1 pr-4">
                  {formatValue(snapshot.normalized_values[name])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
