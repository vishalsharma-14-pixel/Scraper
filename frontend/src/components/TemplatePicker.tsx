import { useEffect, useState } from 'react'
import { listTemplates } from '../api/templates'
import type { Template } from '../api/types'

export default function TemplatePicker({ onApply }: { onApply: (template: Template) => void }) {
  const [templates, setTemplates] = useState<Template[]>([])
  const [selectedKey, setSelectedKey] = useState('')

  useEffect(() => {
    listTemplates().then(setTemplates).catch(() => setTemplates([]))
  }, [])

  return (
    <div className="flex items-center gap-2">
      <select
        className="rounded border border-gray-300 px-2 py-1.5 text-sm"
        value={selectedKey}
        onChange={(e) => setSelectedKey(e.target.value)}
      >
        <option value="">Start from a template…</option>
        {templates.map((t) => (
          <option key={t.key} value={t.key}>
            {t.name}
          </option>
        ))}
      </select>
      <button
        type="button"
        disabled={!selectedKey}
        onClick={() => {
          const template = templates.find((t) => t.key === selectedKey)
          if (template) onApply(template)
        }}
        className="rounded-md bg-blue-600 px-3 py-1.5 text-sm text-white disabled:opacity-40"
      >
        Apply
      </button>
    </div>
  )
}
