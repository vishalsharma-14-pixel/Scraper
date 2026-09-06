import { apiClient } from './client'
import type { Template } from './types'

export async function listTemplates(): Promise<Template[]> {
  const res = await apiClient.get<Template[]>('/api/templates')
  return res.data
}
