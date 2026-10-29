import React, { useState } from 'react';
import { ArrowUpRight } from 'lucide-react';

/**
 * Inquiry Console Component matching the template console.
 * Contains the question input and Send button.
 */
export default function InquiryConsole({ pdfFile }) {
  const [question, setQuestion] = useState('');
  const [lastQuery, setLastQuery] = useState('');

  const handleSend = (e) => {
    e?.preventDefault();
    if (!question.trim()) return;

    // Record query for simple visual feedback (RAG backend not connected yet)
    setLastQuery(question.trim());
    setQuestion('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex flex-col justify-between h-full bg-zinc-950/60 border border-zinc-800/90 rounded-lg p-5 sm:p-7 relative overflow-hidden backdrop-blur-xs">
      {/* Top Header of Console */}
      <div className="flex items-center justify-between border-b border-zinc-900 pb-4 mb-6">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-red-600 animate-pulse"></span>
          <span className="font-mono-tech text-xs uppercase tracking-wider text-zinc-300 font-medium">
            02 / Inquiry Console
          </span>
        </div>
        <span className="font-mono-tech text-xs text-zinc-400 uppercase tracking-widest">
          {pdfFile ? 'PDF Active' : '00 Messages'}
        </span>
      </div>

      {/* Middle Content: System Ready Instruction & Status */}
      <div className="space-y-6 my-auto py-4">
        {/* Editorial Accent Callout */}
        <div className="border-l-2 border-red-600 pl-4 py-1">
          <span className="font-mono-tech text-[11px] font-semibold tracking-widest uppercase text-red-500 block mb-1">
            System Ready
          </span>
          <p className="text-sm text-zinc-300 leading-relaxed max-w-xl">
            Welcome to the College Document Assistant. Please upload a course or
            institutional PDF on the left, then type your question in the text
            field below.
          </p>
        </div>

        {/* Temporary Query Feedback (Placeholder for future RAG response) */}
        {lastQuery && (
          <div className="p-3.5 rounded bg-zinc-900/70 border border-zinc-800 text-xs font-mono-tech space-y-1.5 animate-fadeIn">
            <div className="text-zinc-400">
              <span className="text-red-400 font-semibold">QUERY:</span> "{lastQuery}"
            </div>
            <div className="text-zinc-400 text-[11px]">
              STATUS: Input received. RAG retrieval & LLM pipeline will be connected in future stages.
            </div>
          </div>
        )}
      </div>

      {/* Bottom Input Area */}
      <div className="pt-6">
        <form onSubmit={handleSend} className="space-y-2">
          {/* Input Box with Send Button Beside */}
          <div className="relative flex items-center bg-zinc-900/90 border border-zinc-800 focus-within:border-red-600 focus-within:ring-1 focus-within:ring-red-600/50 rounded-lg p-1.5 pl-4 transition-all">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything about your PDF..."
              className="w-full bg-transparent text-sm text-zinc-100 placeholder-zinc-400 focus:outline-none"
            />

            <button
              type="submit"
              disabled={!question.trim()}
              title="Send question"
              className={`w-10 h-10 rounded-md flex items-center justify-center shrink-0 transition-all cursor-pointer ${
                question.trim()
                  ? 'bg-red-600 hover:bg-red-500 text-white shadow-md shadow-red-950/50'
                  : 'bg-zinc-800 text-zinc-400 cursor-not-allowed'
              }`}
            >
              <ArrowUpRight className="w-5 h-5" />
            </button>
          </div>

          {/* Under-Input Guidance Matching Template */}
          <div className="flex items-center justify-between text-[11px] font-mono-tech text-zinc-400 px-1 pt-1">
            <span>Attach a PDF document and enter text to query the assistant.</span>
            <span className="hidden sm:inline tracking-wider">PRESS ENTER ↵</span>
          </div>
        </form>
      </div>
    </div>
  );
}

