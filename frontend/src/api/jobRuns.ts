import { apiClient } from './client'
import type { JobRun, JobStatus } from './types'

export async function listJobRuns(
  opts: { trackerId?: string; status?: JobStatus; limit?: number } = {},
): Promise<JobRun[]> {
  const res = await apiClient.get<JobRun[]>('/api/job-runs', {
    params: { tracker_id: opts.trackerId, status: opts.status, limit: opts.limit ?? 50 },
  })
  return res.data
}

export async function getJobRun(id: string): Promise<JobRun> {
  const res = await apiClient.get<JobRun>(`/api/job-runs/${id}`)
  return res.data
}
