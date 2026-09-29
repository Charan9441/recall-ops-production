import React from 'react';
import { Brain, Cpu, Sparkles } from 'lucide-react';
import type { HindsightStatus } from '../types/incident';

interface HeaderProps {
  hindsightStatus: HindsightStatus | null;
  onLoadDemoScenario: () => void;
}

export const Header: React.FC<HeaderProps> = ({ hindsightStatus, onLoadDemoScenario }) => {
  const isConnected = hindsightStatus?.connected ?? false;

  return (
    <header className="border-b border-gray-800 bg-[#0f172a]/80 backdrop-blur sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 py-3 sm:px-6 lg:px-8 flex flex-col md:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-gradient-to-br from-purple-600 to-blue-600 rounded-xl shadow-lg shadow-purple-500/20">
            <Brain className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold tracking-tight text-white">RECALL-OPS</h1>
              <span className="text-xs px-2 py-0.5 rounded-full bg-purple-950 text-purple-300 border border-purple-800/50 font-mono">
                HackwithHyderabad 3.0 MVP
              </span>
            </div>
            <p className="text-xs text-gray-400">
              Production Incident Intelligence powered by Persistent Hindsight Memory
            </p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Demo Button */}
          <button
            onClick={onLoadDemoScenario}
            className="flex items-center gap-1.5 text-xs font-semibold px-3 py-1.5 rounded-lg bg-purple-600/20 text-purple-300 border border-purple-500/40 hover:bg-purple-600/30 transition-all shadow-sm"
            title="Load the primary demo incident (payment-api v2.4.1 HTTP 503)"
          >
            <Sparkles className="w-3.5 h-3.5 text-purple-400" />
            Load Primary Demo Incident
          </button>

          {/* Hindsight Status Badge */}
          <div
            className={`flex items-center gap-2 px-3 py-1.5 rounded-lg border text-xs font-medium ${
              isConnected
                ? 'bg-purple-950/60 border-purple-700/60 text-purple-200'
                : 'bg-amber-950/60 border-amber-700/60 text-amber-200'
            }`}
          >
            <span className="relative flex h-2 w-2">
              <span
                className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${
                  isConnected ? 'bg-purple-400' : 'bg-amber-400'
                }`}
              ></span>
              <span
                className={`relative inline-flex rounded-full h-2 w-2 ${
                  isConnected ? 'bg-purple-500' : 'bg-amber-500'
                }`}
              ></span>
            </span>
            <span className="font-mono">
              {isConnected ? '🧠 HINDSIGHT CONNECTED' : '🧠 HINDSIGHT READY'}
            </span>
          </div>

          {/* LLM Status Badge */}
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-950/60 border border-blue-700/60 text-blue-200 text-xs font-mono">
            <Cpu className="w-3.5 h-3.5 text-blue-400" />
            GROQ LLM ONLINE
          </div>
        </div>
      </div>
    </header>
  );
};
