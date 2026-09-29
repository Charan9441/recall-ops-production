import React from 'react';
import { Activity, AlertTriangle, FileText, HelpCircle } from 'lucide-react';
import type { IncidentAnalysis } from '../types/incident';

interface AnalysisPanelProps {
  analysis: IncidentAnalysis | null;
  loading: boolean;
}

export const AnalysisPanel: React.FC<AnalysisPanelProps> = ({ analysis, loading }) => {
  if (loading) {
    return (
      <div className="bg-[#111827] rounded-xl border border-gray-800 p-5 shadow-xl animate-pulse">
        <div className="flex items-center gap-2 mb-3">
          <Activity className="w-5 h-5 text-blue-400 animate-spin" />
          <h2 className="text-base font-semibold text-gray-200">Synthesizing Incident Intelligence...</h2>
        </div>
        <div className="h-4 bg-gray-800 rounded w-3/4 mb-2"></div>
        <div className="h-4 bg-gray-800 rounded w-1/2"></div>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="bg-[#111827] rounded-xl border border-gray-800 p-6 shadow-xl text-center">
        <FileText className="w-10 h-10 text-gray-600 mx-auto mb-2" />
        <h3 className="text-sm font-semibold text-gray-300">Awaiting Incident Submission</h3>
        <p className="text-xs text-gray-500 mt-1">
          Submit incident telemetry above to trigger Hindsight memory retrieval and AI diagnosis.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-[#111827] rounded-xl border border-gray-800 p-5 shadow-xl space-y-4">
      <div className="flex items-center justify-between border-b border-gray-800 pb-3">
        <div className="flex items-center gap-2">
          <Activity className="w-5 h-5 text-blue-400" />
          <h2 className="text-base font-semibold text-white">AI Incident Analysis</h2>
        </div>
        <span className="text-xs text-blue-400 bg-blue-950 px-2 py-0.5 rounded border border-blue-800 font-mono">
          Groq Synthesis Complete
        </span>
      </div>

      {/* Summary */}
      <div className="bg-gray-900/60 p-3.5 rounded-lg border border-gray-800">
        <span className="text-xs font-semibold text-gray-400 uppercase tracking-wider block mb-1">
          Executive Summary
        </span>
        <p className="text-sm text-gray-200">{analysis.summary}</p>
      </div>

      {/* Likely Root Cause */}
      <div className="bg-amber-950/30 p-4 rounded-lg border border-amber-800/50">
        <div className="flex items-center gap-2 mb-1 text-amber-300 font-semibold text-sm">
          <AlertTriangle className="w-4 h-4 text-amber-400" />
          <span>Likely Root Cause</span>
        </div>
        <p className="text-sm text-amber-100 font-medium">{analysis.likely_root_cause}</p>
      </div>

      {/* Reasoning */}
      <div className="bg-gray-900/60 p-3.5 rounded-lg border border-gray-800 text-xs">
        <span className="text-gray-400 font-semibold flex items-center gap-1.5 mb-1.5">
          <HelpCircle className="w-3.5 h-3.5 text-purple-400" />
          Agent Reasoning & Evidence Synthesis:
        </span>
        <p className="text-gray-300 leading-relaxed">{analysis.reasoning}</p>
      </div>

      {/* Historical Evidence */}
      {analysis.historical_evidence && analysis.historical_evidence.length > 0 && (
        <div className="bg-purple-950/30 p-3.5 rounded-lg border border-purple-800/40 text-xs">
          <span className="text-purple-300 font-semibold block mb-2">
            Historical Memory Evidence Cited:
          </span>
          <ul className="space-y-1 text-gray-300 list-disc list-inside">
            {analysis.historical_evidence.map((ev, i) => (
              <li key={i} className="leading-snug">
                {ev}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
