import { useEffect, useState } from 'react';
import {
  analyzeIncident,
  getHindsightStatus,
  getHistory,
  resolveIncident,
} from './services/api';
import type {
  HindsightStatus,
  IncidentAnalysis,
  IncidentCreate,
  IncidentItem,
  IncidentResolution,
  MemoryMatch,
} from './types/incident';
import { Header } from './components/Header';
import { IncidentForm } from './components/IncidentForm';
import { MemoryPanel } from './components/MemoryPanel';
import { AnalysisPanel } from './components/AnalysisPanel';
import { RecommendationPanel } from './components/RecommendationPanel';
import { ResolutionForm } from './components/ResolutionForm';
import { IncidentHistory } from './components/IncidentHistory';
import { AlertTriangle, ArrowRight, Brain } from 'lucide-react';

export function App() {
  // State
  const [formData, setFormData] = useState<IncidentCreate>({
    service: 'payment-api',
    severity: 'HIGH',
    error: 'HTTP 503',
    logs: 'Database connection pool exhausted. Active connections: 100/100. Connection leak suspected.',
    version: 'v2.4.1',
  });

  const [currentIncidentId, setCurrentIncidentId] = useState<string>('INC-1050');
  const [analysis, setAnalysis] = useState<IncidentAnalysis | null>(null);
  const [memoryMatches, setMemoryMatches] = useState<MemoryMatch[]>([]);
  const [hindsightStatus, setHindsightStatus] = useState<HindsightStatus | null>(null);
  const [history, setHistory] = useState<IncidentItem[]>([]);

  const [loadingAnalysis, setLoadingAnalysis] = useState<boolean>(false);
  const [loadingResolving, setLoadingResolving] = useState<boolean>(false);
  const [loadingHistory, setLoadingHistory] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Fetch initial Hindsight status and history
  const loadInitialData = async () => {
    try {
      const statusData = await getHindsightStatus();
      setHindsightStatus(statusData);

      setLoadingHistory(true);
      const historyData = await getHistory();
      setHistory(historyData.incidents || []);
    } catch (err: any) {
      console.warn('Initial data load error:', err);
    } finally {
      setLoadingHistory(false);
    }
  };

  useEffect(() => {
    loadInitialData();
  }, []);

  // Primary Demo Scenario Loader
  const handleLoadDemoScenario = () => {
    setFormData({
      service: 'payment-api',
      severity: 'HIGH',
      error: 'HTTP 503',
      logs: 'Database connection pool exhausted. Active connections: 100/100. Connection leak suspected in v2.4.1.',
      version: 'v2.4.1',
    });
    setErrorMessage(null);
    setSuccessMessage('Loaded Primary Demo Incident (payment-api HTTP 503 v2.4.1)');
    setTimeout(() => setSuccessMessage(null), 4000);
  };

  // Analyze Incident Handler
  const handleAnalyze = async (data: IncidentCreate) => {
    setLoadingAnalysis(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      const res = await analyzeIncident(data);
      setCurrentIncidentId(res.incident_id);
      setAnalysis(res.analysis);
      setMemoryMatches(res.memory_matches || []);
      setSuccessMessage(`Analysis complete for ${res.incident_id}. Hindsight memory retrieved.`);
      setTimeout(() => setSuccessMessage(null), 5000);
    } catch (err: any) {
      setErrorMessage(err.message || 'Error analyzing incident');
    } finally {
      setLoadingAnalysis(false);
    }
  };

  // Resolve Incident Handler
  const handleResolve = async (data: IncidentResolution) => {
    setLoadingResolving(true);
    setErrorMessage(null);

    try {
      const res = await resolveIncident(data);
      setSuccessMessage(
        `🧠 Memory Stored! Incident ${res.incident_id} retained into Hindsight memory bank.`
      );
      // Refresh history list
      const updatedHistory = await getHistory();
      setHistory(updatedHistory.incidents || []);
    } catch (err: any) {
      setErrorMessage(err.message || 'Error resolving incident');
    } finally {
      setLoadingResolving(false);
    }
  };

  const handleSelectHistoryItem = (item: IncidentItem) => {
    setFormData({
      service: item.service,
      severity: item.severity,
      error: item.error,
      logs: item.logs,
      version: item.version || '',
    });
    setCurrentIncidentId(item.id);
  };

  return (
    <div className="min-h-screen bg-[#0b0f19] text-gray-100 flex flex-col font-sans">
      {/* Header */}
      <Header
        hindsightStatus={hindsightStatus}
        onLoadDemoScenario={handleLoadDemoScenario}
      />

      {/* Main Content Dashboard */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-6 sm:px-6 lg:px-8 space-y-6">
        {/* Banner highlighting the Hindsight Memory Loop */}
        <div className="bg-gradient-to-r from-purple-950/80 via-indigo-950/60 to-blue-950/80 border border-purple-800/60 rounded-xl p-4 shadow-xl flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-purple-600/30 rounded-lg text-purple-300 border border-purple-500/40">
              <Brain className="w-5 h-5 text-purple-300" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-white">The Hindsight Memory Loop</h3>
              <p className="text-xs text-purple-200/80">
                Incident Telemetry &rarr; Hindsight Memory Recall &rarr; AI Recommendation &rarr; Resolution Retained for Future Use
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 text-xs font-mono text-purple-300 bg-purple-900/40 px-3 py-1.5 rounded-lg border border-purple-700/50">
            <span>Incident</span>
            <ArrowRight className="w-3 h-3 text-purple-400" />
            <span>Recall</span>
            <ArrowRight className="w-3 h-3 text-purple-400" />
            <span>Resolve</span>
            <ArrowRight className="w-3 h-3 text-purple-400" />
            <span>Retain</span>
          </div>
        </div>

        {/* Global Error Banner */}
        {errorMessage && (
          <div className="p-4 bg-red-950/80 border border-red-800 rounded-xl text-red-200 text-sm flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-red-400" />
              <span>{errorMessage}</span>
            </div>
            <button
              onClick={() => setErrorMessage(null)}
              className="text-xs text-red-400 hover:text-red-200"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Two-Column Grid Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column: Intake & Resolution Forms */}
          <div className="lg:col-span-5 space-y-6">
            <IncidentForm
              onSubmit={handleAnalyze}
              loading={loadingAnalysis}
              formData={formData}
              setFormData={setFormData}
            />

            <ResolutionForm
              currentIncidentId={currentIncidentId}
              onResolve={handleResolve}
              resolving={loadingResolving}
              successMessage={successMessage}
            />
          </div>

          {/* Right Column: Hindsight Memory, AI Analysis, Actions, History */}
          <div className="lg:col-span-7 space-y-6">
            {/* 🧠 HINDSIGHT MEMORY PANEL */}
            <MemoryPanel
              matches={memoryMatches}
              loading={loadingAnalysis}
              incidentId={currentIncidentId}
            />

            {/* AI Incident Analysis */}
            <AnalysisPanel
              analysis={analysis}
              loading={loadingAnalysis}
            />

            {/* Recommended Actions */}
            {analysis && (
              <RecommendationPanel
                actions={analysis.recommended_actions}
                loading={loadingAnalysis}
              />
            )}

            {/* Organizational Incident History Log */}
            <IncidentHistory
              incidents={history}
              loading={loadingHistory}
              onSelectIncident={handleSelectHistoryItem}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-4 bg-[#0a0d14] text-center text-xs text-gray-500">
        <p>
          Recall-Ops &bull; HackwithHyderabad 3.0 MVP &bull; Built with Hindsight Persistent Memory + Groq LLM + FastAPI + React
        </p>
      </footer>
    </div>
  );
}

export default App;
