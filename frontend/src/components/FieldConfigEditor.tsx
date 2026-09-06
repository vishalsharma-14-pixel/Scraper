import type { FieldConfig } from '../api/types'

export interface FieldRow {
  name: string
  config: FieldConfig
}

const FIELD_TYPES = ['text', 'price', 'number', 'availability']

export function configToRows(config: Record<string, FieldConfig>): FieldRow[] {
  return Object.entries(config).map(([name, cfg]) => ({ name, config: cfg }))
}

export function rowsToConfig(rows: FieldRow[]): Record<string, FieldConfig> {
  const config: Record<string, FieldConfig> = {}
  for (const row of rows) {
    if (row.name.trim()) config[row.name.trim()] = row.config
  }
  return config
}

export default function FieldConfigEditor({
  rows,
  onChange,
}: {
  rows: FieldRow[]
  onChange: (rows: FieldRow[]) => void
}) {
  function updateRow(index: number, patch: Partial<FieldRow>) {
    const next = rows.slice()
    next[index] = { ...next[index], ...patch }
    onChange(next)
  }

  function updateFieldConfig(index: number, patch: Partial<FieldConfig>) {
    updateRow(index, { config: { ...rows[index].config, ...patch } })
  }

  function addRow() {
    onChange([...rows, { name: '', config: { selector: '', type: 'text' } }])
  }

  function removeRow(index: number) {
    onChange(rows.filter((_, i) => i !== index))
  }

  return (
    <div className="space-y-3">
      {rows.map((row, index) => (
        <div key={index} className="grid grid-cols-12 gap-2 rounded-md border border-gray-200 p-2">
          <input
            className="col-span-2 rounded border border-gray-300 px-2 py-1 text-sm"
            placeholder="field name"
            value={row.name}
            onChange={(e) => updateRow(index, { name: e.target.value })}
          />
          <input
            className="col-span-4 rounded border border-gray-300 px-2 py-1 text-sm"
            placeholder="CSS selector"
            value={row.config.selector ?? ''}
            onChange={(e) => updateFieldConfig(index, { selector: e.target.value })}
          />
          <input
            className="col-span-2 rounded border border-gray-300 px-2 py-1 text-sm"
            placeholder="xpath (optional)"
            value={row.config.xpath ?? ''}
            onChange={(e) => updateFieldConfig(index, { xpath: e.target.value })}
          />
          <select
            className="col-span-2 rounded border border-gray-300 px-2 py-1 text-sm"
            value={row.config.type}
            onChange={(e) => updateFieldConfig(index, { type: e.target.value })}
          >
            {FIELD_TYPES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>
          <input
            className="col-span-1 rounded border border-gray-300 px-2 py-1 text-sm"
            placeholder="attr"
            value={row.config.attribute ?? ''}
            onChange={(e) => updateFieldConfig(index, { attribute: e.target.value })}
          />
          <button
            type="button"
            onClick={() => removeRow(index)}
            className="col-span-1 rounded text-sm text-red-500 hover:text-red-700"
          >
            Remove
          </button>
        </div>
      ))}
      <button
        type="button"
        onClick={addRow}
        className="rounded-md border border-dashed border-gray-300 px-3 py-1.5 text-sm text-gray-600 hover:border-blue-400 hover:text-blue-600"
      >
        + Add field
      </button>
    </div>
  )
}
