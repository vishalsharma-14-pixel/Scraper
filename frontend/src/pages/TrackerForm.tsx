import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { createTracker, getTracker, updateTracker } from '../api/trackers'
import { apiErrorMessage } from '../api/client'
import type { Template } from '../api/types'
import FieldConfigEditor, { configToRows, rowsToConfig, type FieldRow } from '../components/FieldConfigEditor'
import TemplatePicker from '../components/TemplatePicker'

export default function TrackerForm() {
  const { id } = useParams()
  const isEditing = Boolean(id)
  const navigate = useNavigate()

  const [name, setName] = useState('')
  const [url, setUrl] = useState('')
  const [requiresJs, setRequiresJs] = useState<'' | 'true' | 'false'>('')
  const [pollIntervalSeconds, setPollIntervalSeconds] = useState(3600)
  const [isActive, setIsActive] = useState(true)
  const [notes, setNotes] = useState('')
  const [rows, setRows] = useState<FieldRow[]>([{ name: '', config: { selector: '', type: 'text' } }])
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  useEffect(() => {
    if (!id) return
    getTracker(id).then((tracker) => {
      setName(tracker.name)
      setUrl(tracker.url)
      setRequiresJs(tracker.requires_js === null ? '' : tracker.requires_js ? 'true' : 'false')
      setPollIntervalSeconds(tracker.poll_interval_seconds)
      setIsActive(tracker.is_active)
      setNotes(tracker.notes ?? '')
      setRows(configToRows(tracker.extraction_config))
    })
  }, [id])

  function applyTemplate(template: Template) {
    setRows(configToRows(template.extraction_config))
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError('')
    setSaving(true)
    try {
      const input = {
        name,
        url,
        extraction_config: rowsToConfig(rows),
        requires_js: requiresJs === '' ? null : requiresJs === 'true',
        poll_interval_seconds: pollIntervalSeconds,
        is_active: isActive,
        notes: notes || null,
      }
      if (isEditing && id) {
        await updateTracker(id, input)
      } else {
        await createTracker(input)
      }
      navigate('/')
    } catch (err) {
      setError(apiErrorMessage(err))
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="mx-auto max-w-3xl px-4 py-8">
      <h1 className="text-xl font-semibold text-gray-900">
        {isEditing ? 'Edit Tracker' : 'New Tracker'}
      </h1>

      <form onSubmit={handleSubmit} className="mt-6 space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Name</label>
          <input
            required
            className="mt-1 w-full rounded border border-gray-300 px-3 py-1.5 text-sm"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">URL</label>
          <input
            required
            type="url"
            className="mt-1 w-full rounded border border-gray-300 px-3 py-1.5 text-sm"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
          />
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Poll interval (seconds)</label>
            <input
              required
              type="number"
              className="mt-1 w-full rounded border border-gray-300 px-3 py-1.5 text-sm"
              value={pollIntervalSeconds}
              onChange={(e) => setPollIntervalSeconds(Number(e.target.value))}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Requires JS rendering?</label>
            <select
              className="mt-1 w-full rounded border border-gray-300 px-3 py-1.5 text-sm"
              value={requiresJs}
              onChange={(e) => setRequiresJs(e.target.value as '' | 'true' | 'false')}
            >
              <option value="">Auto-detect</option>
              <option value="true">Always (headless)</option>
              <option value="false">Never</option>
            </select>
          </div>
        </div>

        <label className="flex items-center gap-2 text-sm text-gray-700">
          <input type="checkbox" checked={isActive} onChange={(e) => setIsActive(e.target.checked)} />
          Active
        </label>

        <div>
          <label className="block text-sm font-medium text-gray-700">Notes</label>
          <textarea
            className="mt-1 w-full rounded border border-gray-300 px-3 py-1.5 text-sm"
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </div>

        <div>
          <div className="mb-2 flex items-center justify-between">
            <label className="block text-sm font-medium text-gray-700">Fields to extract</label>
            <TemplatePicker onApply={applyTemplate} />
          </div>
          <FieldConfigEditor rows={rows} onChange={setRows} />
        </div>

        {error && <p className="text-sm text-red-500">{error}</p>}

        <div className="flex gap-2">
          <button
            type="submit"
            disabled={saving}
            className="rounded-md bg-blue-600 px-4 py-1.5 text-sm font-medium text-white disabled:opacity-50"
          >
            {saving ? 'Saving…' : 'Save Tracker'}
          </button>
          <button
            type="button"
            onClick={() => navigate('/')}
            className="rounded-md border border-gray-300 px-4 py-1.5 text-sm text-gray-700"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}
