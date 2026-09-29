import React, { useState } from 'react';
import { CheckCircle2, Save, Send } from 'lucide-react';
import type { IncidentResolution } from '../types/incident';

interface ResolutionFormProps {
  currentIncidentId?: string;
  onResolve: (data: IncidentResolution) => Promise<void>;
  resolving: boolean;
  successMessage: string | null;
}

export const ResolutionForm: React.FC<ResolutionFormProps> = ({
  currentIncidentId,
  onResolve,
  resolving,
  successMessage,
}) => {
  const [incidentId, setIncidentId] = useState(currentIncidentId || '');
  const [rootCause, setRootCause] = useState('');
  const [resolution, setResolution] = useState('');
  const [outcome, setOutcome] = useState('Resolved');
  const [resolutionTime, setResolutionTime] = useState<number>(11);

  // Sync with current incident ID if updated
  React.useEffect(() => {
    if (currentIncidentId) {
      setIncidentId(currentIncidentId);
    }
  }, [currentIncidentId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!incidentId || !rootCause || !resolution) return;

    await onResolve({
      incident_id: incidentId,
      root_cause: rootCause,
      resolution,
      outcome,
      resolution_time_minutes: Number(resolutionTime) || undefined,
    });
  };

  return (
    <div className="bg-[#111827] rounded-xl border border-purple-900/60 p-5 shadow-xl hindsight-glow">
      <div className="flex items-center justify-between mb-4 border-b border-gray-800 pb-3">
        <div className="flex items-center gap-2">
          <Save className="w-5 h-5 text-purple-400" />
          <h2 className="text-base font-semibold text-white">Record Resolution & Store Experience</h2>
        </div>
        <span className="text-xs text-purple-300 font-mono">Step 2: Learn Loop</span>
      </div>

      {successMessage && (
        <div className="mb-4 p-3 bg-emerald-950/80 border border-emerald-700 rounded-lg text-emerald-200 text-xs flex items-center gap-2 font-medium">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>{successMessage}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">Incident ID</label>
            <input
              type="text"
              value={incidentId}
              onChange={(e) => setIncidentId(e.target.value)}
              placeholder="e.g. INC-1050"
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-purple-300 font-mono focus:outline-none focus:border-purple-500"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">Outcome</label>
            <select
              value={outcome}
              onChange={(e) => setOutcome(e.target.value)}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500"
            >
              <option value="Resolved">✅ Resolved</option>
              <option value="Mitigated">⚠️ Mitigated</option>
              <option value="Workaround Applied">🔧 Workaround Applied</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">Resolution Time (Mins)</label>
            <input
              type="number"
              min="1"
              value={resolutionTime}
              onChange={(e) => setResolutionTime(Number(e.target.value))}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500"
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-300 mb-1">
            Verified Root Cause <span className="text-purple-400">*</span>
          </label>
          <input
            type="text"
            placeholder="e.g. Connection leak introduced in v2.4.1 database pool handler."
            value={rootCause}
            onChange={(e) => setRootCause(e.target.value)}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500"
            required
          />
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-300 mb-1">
            Successful Resolution Action Taken <span className="text-purple-400">*</span>
          </label>
          <textarea
            rows={2}
            placeholder="e.g. Rolled back deployment to v2.4.0 and restarted payment-api pods."
            value={resolution}
            onChange={(e) => setResolution(e.target.value)}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500"
            required
          />
        </div>

        <button
          type="submit"
          disabled={resolving || !incidentId || !rootCause || !resolution}
          className="w-full py-2.5 px-4 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 text-white font-medium text-sm rounded-lg shadow-lg shadow-purple-900/30 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
        >
          {resolving ? (
            <>
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              <span>Retaining Experience in Hindsight...</span>
            </>
          ) : (
            <>
              <Send className="w-4 h-4" />
              <span>🧠 Retain Experience in Hindsight Memory Bank</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
};
