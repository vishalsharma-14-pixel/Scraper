import { apiClient } from './client'
import type { ChangeEvent, JobRun, Snapshot, Tracker, TrackerInput } from './types'

export async function listTrackers(): Promise<Tracker[]> {
  const res = await apiClient.get<Tracker[]>('/api/trackers')
  return res.data
}

export async function getTracker(id: string): Promise<Tracker> {
  const res = await apiClient.get<Tracker>(`/api/trackers/${id}`)
  return res.data
}

export async function createTracker(input: TrackerInput): Promise<Tracker> {
  const res = await apiClient.post<Tracker>('/api/trackers', input)
  return res.data
}

export async function updateTracker(id: string, input: TrackerInput): Promise<Tracker> {
  const res = await apiClient.put<Tracker>(`/api/trackers/${id}`, input)
  return res.data
}

export async function deleteTracker(id: string): Promise<void> {
  await apiClient.delete(`/api/trackers/${id}`)
}

export async function runTrackerNow(id: string): Promise<JobRun> {
  const res = await apiClient.post<JobRun>(`/api/trackers/${id}/run`)
  return res.data
}

export async function listTrackerSnapshots(id: string, limit = 50): Promise<Snapshot[]> {
  const res = await apiClient.get<Snapshot[]>(`/api/trackers/${id}/snapshots`, { params: { limit } })
  return res.data
}

export async function getLatestSnapshot(id: string): Promise<Snapshot | null> {
  try {
    const res = await apiClient.get<Snapshot>(`/api/trackers/${id}/snapshots/latest`)
    return res.data
  } catch {
    return null
  }
}

export async function listTrackerChanges(id: string, limit = 50): Promise<ChangeEvent[]> {
  const res = await apiClient.get<ChangeEvent[]>(`/api/trackers/${id}/changes`, { params: { limit } })
  return res.data
}

export async function listTrackerJobs(id: string, limit = 50): Promise<JobRun[]> {
  const res = await apiClient.get<JobRun[]>(`/api/trackers/${id}/jobs`, { params: { limit } })
  return res.data
}
