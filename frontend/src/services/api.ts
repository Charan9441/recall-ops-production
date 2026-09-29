import type {
  HindsightStatus,
  HistoryResponse,
  IncidentCreate,
  IncidentResolution,
  IncidentResolutionResponse,
  IncidentResponse,
} from '../types/incident';

const API_BASE =
  import.meta.env.VITE_API_URL ||
  (typeof window !== 'undefined' && window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1'
    ? '/api'
    : 'http://localhost:8000/api');

export async function analyzeIncident(payload: IncidentCreate): Promise<IncidentResponse> {
  const res = await fetch(`${API_BASE}/incidents/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Analysis failed' }));
    throw new Error(err.detail || 'Failed to analyze incident');
  }
  return res.json();
}

export async function resolveIncident(
  payload: IncidentResolution
): Promise<IncidentResolutionResponse> {
  const res = await fetch(`${API_BASE}/incidents/resolve`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Resolution recording failed' }));
    throw new Error(err.detail || 'Failed to resolve incident');
  }
  return res.json();
}

export async function getHistory(): Promise<HistoryResponse> {
  const res = await fetch(`${API_BASE}/incidents/history`);
  if (!res.ok) {
    throw new Error('Failed to fetch incident history');
  }
  return res.json();
}

export async function getHindsightStatus(): Promise<HindsightStatus> {
  const res = await fetch(`${API_BASE}/hindsight/status`);
  if (!res.ok) {
    return {
      connected: false,
      bank_id: 'recall-ops-production',
      message: 'Hindsight backend unreachable',
    };
  }
  return res.json();
}
