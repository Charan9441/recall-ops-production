export type Severity = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface IncidentCreate {
  service: string;
  severity: Severity;
  error: string;
  logs: string;
  version?: string;
}

export interface MemoryMatch {
  id: string;
  service: string;
  error: string;
  root_cause: string;
  resolution: string;
  relevance_label: string;
  version?: string;
  outcome?: string;
  snippet?: string;
}

export interface IncidentAnalysis {
  summary: string;
  likely_root_cause: string;
  recommended_actions: string[];
  historical_evidence: string[];
  reasoning: string;
}

export interface IncidentResponse {
  incident_id: string;
  analysis: IncidentAnalysis;
  memory_matches: MemoryMatch[];
  hindsight_status: string;
}

export interface IncidentResolution {
  incident_id: string;
  root_cause: string;
  resolution: string;
  outcome: string;
  resolution_time_minutes?: number;
}

export interface IncidentResolutionResponse {
  success: boolean;
  incident_id: string;
  memory_status: string;
  message: string;
}

export interface IncidentItem {
  id: string;
  timestamp: string;
  service: string;
  severity: Severity;
  error: string;
  logs: string;
  version?: string;
  root_cause?: string;
  resolution?: string;
  outcome?: string;
  resolution_time_minutes?: number;
  status: 'open' | 'resolved';
}

export interface HistoryResponse {
  incidents: IncidentItem[];
  total: number;
}

export interface HindsightStatus {
  connected: boolean;
  bank_id: string;
  message: string;
}
