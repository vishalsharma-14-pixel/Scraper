export type FieldType = 'price' | 'number' | 'text' | 'availability'

export interface FieldConfig {
  selector?: string | null
  xpath?: string | null
  type: FieldType | string
  attribute?: string | null
}

export type FetchMethod = 'http' | 'headless'
export type ChangeEventType = 'first_seen' | 'value_changed'
export type JobStatus = 'pending' | 'running' | 'success' | 'failed'
export type JobTrigger = 'scheduled' | 'manual'

export interface Tracker {
  id: string
  name: string
  url: string
  extraction_config: Record<string, FieldConfig>
  requires_js: boolean | null
  poll_interval_seconds: number
  is_active: boolean
  next_run_at: string | null
  last_run_at: string | null
  notes: string | null
  created_at: string
  updated_at: string
}

export interface TrackerInput {
  name: string
  url: string
  extraction_config: Record<string, FieldConfig>
  requires_js: boolean | null
  poll_interval_seconds: number
  is_active: boolean
  notes: string | null
}

export interface Snapshot {
  id: string
  tracker_id: string
  raw_values: Record<string, unknown>
  normalized_values: Record<string, unknown>
  fetch_method: FetchMethod
  scraped_at: string
}

export interface ChangeEvent {
  id: string
  tracker_id: string
  snapshot_id: string
  previous_snapshot_id: string | null
  field_name: string
  old_value: unknown
  new_value: unknown
  change_type: ChangeEventType
  detected_at: string
  notified: boolean
}

export interface JobRun {
  id: string
  tracker_id: string
  celery_task_id: string | null
  status: JobStatus
  trigger: JobTrigger
  fetch_method_used: FetchMethod | null
  snapshot_id: string | null
  started_at: string | null
  finished_at: string | null
  error_message: string | null
  created_at: string
}

export interface Template {
  key: string
  name: string
  description: string
  extraction_config: Record<string, FieldConfig>
}
