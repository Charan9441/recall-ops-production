import React from 'react';
import { CheckCircle, Database } from 'lucide-react';
import type { IncidentItem } from '../types/incident';

interface IncidentHistoryProps {
  incidents: IncidentItem[];
  loading: boolean;
  onSelectIncident?: (item: IncidentItem) => void;
}

export const IncidentHistory: React.FC<IncidentHistoryProps> = ({
  incidents,
  loading,
  onSelectIncident,
}) => {
  if (loading) {
    return (
      <div className="bg-[#111827] rounded-xl border border-gray-800 p-5 shadow-xl animate-pulse">
        <div className="h-5 bg-gray-800 rounded w-1/3 mb-4"></div>
        <div className="space-y-3">
          <div className="h-16 bg-gray-900 rounded"></div>
          <div className="h-16 bg-gray-900 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-[#111827] rounded-xl border border-gray-800 p-5 shadow-xl">
      <div className="flex items-center justify-between mb-4 border-b border-gray-800 pb-3">
        <div className="flex items-center gap-2">
          <Database className="w-5 h-5 text-gray-400" />
          <h2 className="text-base font-semibold text-white">Organizational Incident Log</h2>
        </div>
        <span className="text-xs text-gray-400 font-mono">
          {incidents.length} Incident{incidents.length !== 1 ? 's' : ''} Stored
        </span>
      </div>

      {incidents.length === 0 ? (
        <div className="p-6 text-center text-xs text-gray-500">
          No incident history available. Run seed script or submit an incident.
        </div>
      ) : (
        <div className="space-y-3 max-h-[400px] overflow-y-auto pr-1">
          {incidents.map((item) => (
            <div
              key={item.id}
              onClick={() => onSelectIncident && onSelectIncident(item)}
              className="p-3.5 bg-gray-900/70 border border-gray-800 rounded-lg hover:border-purple-600/50 transition-all cursor-pointer group"
            >
              <div className="flex items-center justify-between mb-1.5">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs font-bold text-purple-400 group-hover:text-purple-300">
                    {item.id}
                  </span>
                  <span className="text-xs font-semibold text-gray-200 bg-gray-800 px-2 py-0.5 rounded">
                    {item.service}
                  </span>
                  <span className="text-xs font-mono text-gray-400 bg-gray-800 px-1.5 py-0.5 rounded">
                    {item.error}
                  </span>
                  {item.version && (
                    <span className="text-[11px] font-mono text-purple-300 bg-purple-950/60 px-1.5 py-0.5 rounded border border-purple-800/40">
                      {item.version}
                    </span>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  <span
                    className={`text-[11px] font-semibold px-2 py-0.5 rounded ${
                      item.status === 'resolved'
                        ? 'bg-emerald-950 text-emerald-300 border border-emerald-800'
                        : 'bg-amber-950 text-amber-300 border border-amber-800'
                    }`}
                  >
                    {item.status === 'resolved' ? 'RESOLVED' : 'OPEN'}
                  </span>
                </div>
              </div>

              {item.root_cause && (
                <p className="text-xs text-gray-300 mb-1 line-clamp-1">
                  <span className="text-gray-400 font-medium">Root Cause:</span> {item.root_cause}
                </p>
              )}

              {item.resolution && (
                <p className="text-xs text-emerald-300 line-clamp-1 flex items-center gap-1">
                  <CheckCircle className="w-3 h-3 text-emerald-400 shrink-0" />
                  <span>{item.resolution}</span>
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
