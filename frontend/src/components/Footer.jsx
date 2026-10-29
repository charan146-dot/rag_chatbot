import React from 'react';

/**
 * Technical footer bar with status telemetry indicators.
 */
export default function Footer() {
  return (
    <footer className="border-t border-zinc-800/80 px-4 sm:px-8 py-3 flex flex-wrap items-center justify-between gap-3 text-[11px] font-mono-tech text-zinc-400 uppercase tracking-widest bg-black/60">
      <div>Institutional Document Interface</div>
      <div className="flex items-center gap-2">
        <span className="w-1.5 h-1.5 rounded-full bg-red-600"></span>
        <span>PDF Parser: Ready</span>
      </div>
      <div>© Academic AI</div>
    </footer>
  );
}

