import React from 'react';
import { ArrowRightCircle, CheckSquare } from 'lucide-react';

interface RecommendationPanelProps {
  actions: string[];
  loading: boolean;
}

export const RecommendationPanel: React.FC<RecommendationPanelProps> = ({ actions, loading }) => {
  if (loading) return null;
  if (!actions || actions.length === 0) return null;

  return (
    <div className="bg-[#111827] rounded-xl border border-emerald-900/60 p-5 shadow-xl">
      <div className="flex items-center gap-2 mb-4 border-b border-gray-800 pb-3">
        <CheckSquare className="w-5 h-5 text-emerald-400" />
        <h2 className="text-base font-semibold text-white">Recommended Response Actions</h2>
        <span className="text-xs text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-800 font-mono">
          Memory-Informed Guidance
        </span>
      </div>

      <div className="space-y-2.5">
        {actions.map((action, idx) => (
          <div
            key={idx}
            className="flex items-start gap-3 p-3 bg-emerald-950/20 border border-emerald-800/40 rounded-lg hover:border-emerald-600/50 transition-all text-xs sm:text-sm text-emerald-100"
          >
            <ArrowRightCircle className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <span className="leading-snug">{action}</span>
          </div>
        ))}
      </div>
    </div>
  );
};
