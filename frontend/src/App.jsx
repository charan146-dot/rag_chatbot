import React, { useState } from 'react';
import Header from './components/Header';
import PdfUploader from './components/PdfUploader';
import InquiryConsole from './components/InquiryConsole';
import Footer from './components/Footer';

export default function App() {
  const [pdfFile, setPdfFile] = useState(null);

  const handleReset = () => {
    setPdfFile(null);
  };

  return (
    <div className="min-h-screen bg-[#070708] text-zinc-100 flex flex-col justify-between selection:bg-red-600 selection:text-white relative overflow-hidden">
      {/* Background Architectural Vector Arcs (Subtle CAD / Blueprint Effect) */}
      <svg
        className="absolute inset-0 w-full h-full pointer-events-none opacity-20"
        xmlns="http://www.w3.org/2000/svg"
      >
        <circle
          cx="20%"
          cy="40%"
          r="480"
          fill="none"
          stroke="#ef4444"
          strokeWidth="0.7"
          strokeDasharray="4 6"
        />
        <circle
          cx="85%"
          cy="70%"
          r="620"
          fill="none"
          stroke="#71717a"
          strokeWidth="0.5"
        />
        <circle
          cx="90%"
          cy="10%"
          r="340"
          fill="none"
          stroke="#dc2626"
          strokeWidth="0.5"
          strokeDasharray="2 4"
        />
      </svg>

      {/* Top Header Bar */}
      <Header pdfFile={pdfFile} onReset={handleReset} />

      {/* Main Workspace Frame */}
      <main className="flex-1 flex items-center justify-center p-4 sm:p-6 lg:p-10 z-10">
        <div className="w-full max-w-7xl grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-stretch">
          
          {/* Left Column: Document Source & Main Heading (5 Cols) */}
          <div className="lg:col-span-5 flex flex-col justify-between space-y-8">
            <div className="space-y-6">
              {/* Index Tag */}
              <div className="font-mono-tech text-xs tracking-wider uppercase text-red-500 font-medium">
                01 / Document Source
              </div>

              {/* Bold Typographic Headline matching template */}
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight uppercase leading-[0.95] text-zinc-100">
                Campus —<br />
                <span className="text-zinc-200">Knowledge</span><br />
                <span className="text-red-500">Assistant</span>
              </h1>

              {/* Editorial Description */}
              <p className="text-sm sm:text-base text-zinc-400 leading-relaxed max-w-md font-normal">
                Upload your college syllabus, academic handbook, or lecture PDF and
                enter your question below for instant, grounded answers.
              </p>
            </div>

            {/* PDF Uploader Card */}
            <div className="pt-2">
              <PdfUploader
                pdfFile={pdfFile}
                onFileSelect={(file) => setPdfFile(file)}
                onFileRemove={() => setPdfFile(null)}
              />
            </div>
          </div>

          {/* Right Column: Inquiry Console (7 Cols) */}
          <div className="lg:col-span-7 flex flex-col">
            <InquiryConsole pdfFile={pdfFile} />
          </div>

        </div>
      </main>

      {/* Bottom Technical Footer Bar */}
      <Footer />
    </div>
  );
}
