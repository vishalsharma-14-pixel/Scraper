import { apiClient } from './client'
import type { ChangeEvent } from './types'

export async function listChangeEvents(opts: { trackerId?: string; limit?: number } = {}): Promise<ChangeEvent[]> {
  const res = await apiClient.get<ChangeEvent[]>('/api/change-events', {
    params: { tracker_id: opts.trackerId, limit: opts.limit ?? 50 },
  })
  return res.data
}
