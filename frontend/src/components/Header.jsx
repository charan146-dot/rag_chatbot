import React from 'react';
import { LayoutGrid, RotateCcw } from 'lucide-react';

/**
 * Top navigation bar with academic branding, status badge, and reset control.
 */
export default function Header({ pdfFile, onReset }) {
  return (
    <header className="border-b border-zinc-800/80 px-4 sm:px-8 py-3.5 flex items-center justify-between bg-black/60 backdrop-blur-sm sticky top-0 z-20">
      {/* Left Branding */}
      <div className="flex items-center gap-2.5">
        <div className="w-5 h-5 grid grid-cols-2 gap-0.5 p-0.5 border border-zinc-700 rounded-sm">
          <div className="bg-red-600 rounded-[1px]"></div>
          <div className="bg-zinc-400 rounded-[1px]"></div>
          <div className="bg-zinc-400 rounded-[1px]"></div>
          <div className="bg-red-600 rounded-[1px]"></div>
        </div>
        <span className="font-mono-tech text-xs sm:text-sm font-semibold tracking-[0.2em] uppercase text-zinc-200">
          Academic Portal
        </span>
      </div>

      {/* Center Title */}
      <div className="hidden md:block font-mono-tech text-xs tracking-[0.45em] uppercase text-zinc-400 font-medium">
        C O L L E G E
      </div>

      {/* Right Controls: Status & Reset */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-2 px-2.5 py-1 rounded border border-zinc-800 bg-zinc-950/80">
          <span
            className={`w-2 h-2 rounded-full ${
              pdfFile ? 'bg-red-500 animate-pulse' : 'bg-zinc-600'
            }`}
          />
          <span className="font-mono-tech text-[11px] sm:text-xs uppercase tracking-wider text-zinc-300">
            {pdfFile ? '1 PDF Loaded' : 'No PDF Loaded'}
          </span>
        </div>

        <button
          onClick={onReset}
          title="Reset document and question"
          className="flex items-center gap-1.5 px-3 py-1 rounded text-xs font-mono-tech uppercase tracking-wider border border-zinc-800 hover:border-red-600/70 hover:text-red-400 text-zinc-400 hover:bg-red-950/20 transition-all cursor-pointer"
        >
          <RotateCcw className="w-3 h-3" />
          <span>Reset</span>
        </button>
      </div>
    </header>
  );
}

