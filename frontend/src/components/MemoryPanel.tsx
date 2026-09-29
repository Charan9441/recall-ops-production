import React from 'react';
import { Brain, CheckCircle2, History, Sparkles } from 'lucide-react';
import type { MemoryMatch } from '../types/incident';

interface MemoryPanelProps {
  matches: MemoryMatch[];
  loading: boolean;
  incidentId?: string;
}

export const MemoryPanel: React.FC<MemoryPanelProps> = ({ matches, loading, incidentId }) => {
  if (loading) {
    return (
      <div className="bg-[#111827] rounded-xl border border-purple-900/60 p-5 shadow-xl hindsight-glow animate-pulse">
        <div className="flex items-center gap-2 mb-3">
          <Brain className="w-5 h-5 text-purple-400 animate-spin" />
          <h3 className="text-base font-semibold text-purple-200">🧠 Querying Hindsight Memory Bank</h3>
        </div>
        <p className="text-xs text-purple-300/80">
          Searching organizational incident history using semantic & relational recall...
        </p>
      </div>
    );
  }

  const hasMatches = matches && matches.length > 0;

  return (
    <div
      className={`bg-[#111827] rounded-xl border p-5 shadow-xl transition-all ${
        hasMatches ? 'border-purple-600/60 hindsight-glow' : 'border-gray-800'
      }`}
    >
      <div className="flex items-center justify-between mb-4 border-b border-gray-800 pb-3">
        <div className="flex items-center gap-2">
          <div className="p-1.5 bg-purple-900/50 rounded-lg text-purple-400">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-semibold text-white flex items-center gap-2">
              🧠 HINDSIGHT MEMORY
              {hasMatches && (
                <span className="text-xs bg-purple-950 text-purple-300 border border-purple-800 px-2 py-0.5 rounded-full font-mono">
                  {matches.length} Match{matches.length > 1 ? 'es' : ''} Retrieved
                </span>
              )}
            </h2>
            <p className="text-xs text-gray-400">Persistent Organizational Incident Knowledge</p>
          </div>
        </div>
        {incidentId && (
          <span className="text-xs font-mono text-gray-400 bg-gray-900 px-2 py-1 rounded border border-gray-800">
            Target: {incidentId}
          </span>
        )}
      </div>

      {!hasMatches ? (
        <div className="p-4 bg-gray-900/50 rounded-lg border border-gray-800 text-center">
          <History className="w-8 h-8 text-gray-600 mx-auto mb-2" />
          <p className="text-sm font-medium text-gray-300">No strong historical match found</p>
          <p className="text-xs text-gray-500 mt-1">
            The AI recommendation is based primarily on current incident telemetry. Resolving this incident will retain a new memory entry.
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          <div className="text-xs text-purple-300/90 bg-purple-950/40 border border-purple-800/40 rounded-lg p-2.5 flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-purple-400 shrink-0" />
            <span>
              Hindsight retrieved relevant operational history before LLM synthesis:
            </span>
          </div>

          <div className="space-y-3">
            {matches.map((match, idx) => (
              <div
                key={match.id + idx}
                className="bg-gray-900/80 border border-purple-800/50 rounded-lg p-4 hover:border-purple-500/80 transition-all"
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-sm font-bold text-purple-300">
                      {match.id}
                    </span>
                    <span className="text-xs font-medium text-gray-300 bg-gray-800 px-2 py-0.5 rounded">
                      {match.service}
                    </span>
                    <span className="text-xs font-mono text-gray-400 bg-gray-800 px-1.5 py-0.5 rounded">
                      {match.error}
                    </span>
                  </div>
                  <span className="text-xs font-semibold px-2 py-0.5 rounded bg-purple-900/70 text-purple-200 border border-purple-700/50">
                    {match.relevance_label}
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs mt-3">
                  <div className="bg-[#0b0f19] p-2.5 rounded border border-gray-800">
                    <span className="text-amber-400 font-semibold block mb-1">
                      Historical Root Cause:
                    </span>
                    <p className="text-gray-300">{match.root_cause}</p>
                  </div>

                  <div className="bg-[#0b0f19] p-2.5 rounded border border-gray-800">
                    <span className="text-emerald-400 font-semibold block mb-1 flex items-center gap-1">
                      <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                      Previous Successful Fix:
                    </span>
                    <p className="text-gray-300">{match.resolution}</p>
                  </div>
                </div>

                {match.version && (
                  <div className="mt-2 text-[11px] text-gray-400 font-mono">
                    Associated Deployment: <span className="text-purple-300">{match.version}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
