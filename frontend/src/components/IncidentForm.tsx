import React, { useState } from 'react';
import { AlertCircle, Search, Terminal } from 'lucide-react';
import type { IncidentCreate, Severity } from '../types/incident';

interface IncidentFormProps {
  onSubmit: (data: IncidentCreate) => void;
  loading: boolean;
  formData: IncidentCreate;
  setFormData: React.Dispatch<React.SetStateAction<IncidentCreate>>;
}

export const IncidentForm: React.FC<IncidentFormProps> = ({
  onSubmit,
  loading,
  formData,
  setFormData,
}) => {
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.service.trim() || !formData.error.trim() || !formData.logs.trim()) {
      setErrorMsg('Please complete Service, Error, and Logs fields.');
      return;
    }
    setErrorMsg(null);
    onSubmit(formData);
  };

  return (
    <div className="bg-[#111827] rounded-xl border border-gray-800 p-5 shadow-xl">
      <div className="flex items-center justify-between mb-4 border-b border-gray-800 pb-3">
        <div className="flex items-center gap-2">
          <Terminal className="w-5 h-5 text-purple-400" />
          <h2 className="text-base font-semibold text-white">Incident Intake</h2>
        </div>
        <span className="text-xs text-gray-400">Step 1: Enter Telemetry</span>
      </div>

      {errorMsg && (
        <div className="mb-4 p-3 bg-red-950/60 border border-red-800 rounded-lg text-red-300 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-red-400 shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">
              Target Service <span className="text-purple-400">*</span>
            </label>
            <input
              type="text"
              placeholder="e.g. payment-api"
              value={formData.service}
              onChange={(e) => setFormData({ ...formData, service: e.target.value })}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">
              Severity Level <span className="text-purple-400">*</span>
            </label>
            <select
              value={formData.severity}
              onChange={(e) =>
                setFormData({ ...formData, severity: e.target.value as Severity })
              }
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
            >
              <option value="CRITICAL">🔴 CRITICAL</option>
              <option value="HIGH">🟠 HIGH</option>
              <option value="MEDIUM">🟡 MEDIUM</option>
              <option value="LOW">🔵 LOW</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">
              Error Title / Status Code <span className="text-purple-400">*</span>
            </label>
            <input
              type="text"
              placeholder="e.g. HTTP 503"
              value={formData.error}
              onChange={(e) => setFormData({ ...formData, error: e.target.value })}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
              required
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">
              Deployment Version (Optional)
            </label>
            <input
              type="text"
              placeholder="e.g. v2.4.1"
              value={formData.version || ''}
              onChange={(e) => setFormData({ ...formData, version: e.target.value })}
              className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500 font-mono"
            />
          </div>
        </div>

        <div>
          <label className="block text-xs font-medium text-gray-300 mb-1">
            Observed Log Telemetry / Symptoms <span className="text-purple-400">*</span>
          </label>
          <textarea
            rows={3}
            placeholder="Paste stacktrace, log snippet, or error message (e.g. Database connection pool exhausted...)"
            value={formData.logs}
            onChange={(e) => setFormData({ ...formData, logs: e.target.value })}
            className="w-full bg-gray-900 border border-gray-700 rounded-lg px-3 py-2 text-sm text-gray-200 font-mono focus:outline-none focus:border-purple-500 focus:ring-1 focus:ring-purple-500"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className="w-full py-2.5 px-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-500 hover:to-blue-500 text-white font-medium text-sm rounded-lg shadow-lg shadow-purple-900/30 transition-all flex items-center justify-center gap-2 disabled:opacity-50"
        >
          {loading ? (
            <>
              <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              <span>Querying Hindsight Memory Bank...</span>
            </>
          ) : (
            <>
              <Search className="w-4 h-4" />
              <span>Analyze Incident with Hindsight Memory</span>
            </>
          )}
        </button>
      </form>
    </div>
  );
};
