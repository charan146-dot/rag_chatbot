import React, { useRef, useState } from 'react';
import { FileText, ArrowUpRight, CheckCircle2, X, AlertCircle } from 'lucide-react';

/**
 * PDF Upload Component matching the editorial template layout.
 * Restricts input strictly to PDF files and displays the selected filename.
 */
export default function PdfUploader({ pdfFile, onFileSelect, onFileRemove }) {
  const fileInputRef = useRef(null);
  const [isDragging, setIsDragging] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    validateAndSelect(file);
    e.target.value = ''; // Reset input so same file can be re-selected if needed
  };

  const validateAndSelect = (file) => {
    setErrorMessage('');
    if (!file) return;

    // Strict validation for PDF only
    const isPdf = file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf');
    if (!isPdf) {
      setErrorMessage('Invalid file format. Please upload a PDF file only.');
      return;
    }

    onFileSelect(file);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    validateAndSelect(file);
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  return (
    <div className="w-full">
      {/* Hidden File Input strictly accepting PDFs */}
      <input
        ref={fileInputRef}
        type="file"
        accept="application/pdf,.pdf"
        className="hidden"
        onChange={handleFileChange}
      />

      {/* Upload Box Container */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`relative border rounded-lg p-5 transition-all duration-200 bg-zinc-950/70 ${
          isDragging
            ? 'border-red-500 bg-red-950/20'
            : pdfFile
            ? 'border-red-900/60 bg-zinc-950/90'
            : 'border-dashed border-zinc-800 hover:border-zinc-700'
        }`}
      >
        {/* Top Header Row: Icon, Title, and Step */}
        <div className="flex items-start justify-between gap-3 mb-4">
          <div className="flex items-center gap-3">
            <div
              className={`w-10 h-10 rounded-md flex items-center justify-center border ${
                pdfFile
                  ? 'border-red-600/60 bg-red-950/30 text-red-400'
                  : 'border-zinc-800 bg-zinc-900 text-zinc-400'
              }`}
            >
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-mono-tech text-xs sm:text-sm font-semibold uppercase tracking-wider text-zinc-200">
                Upload PDF Document
              </h3>
              <p className="text-xs text-zinc-400 mt-0.5">
                {pdfFile
                  ? 'Document ready for querying'
                  : 'Drag & drop a .pdf file here or click to browse'}
              </p>
            </div>
          </div>
          <span className="font-mono-tech text-xs text-zinc-400 tracking-widest">
            01 / 02
          </span>
        </div>

        {/* Selected File Display or Drag State */}
        {pdfFile ? (
          <div className="my-3 p-3 rounded-md bg-zinc-900/80 border border-zinc-800 flex items-center justify-between gap-3">
            <div className="flex items-center gap-2.5 min-w-0">
              <CheckCircle2 className="w-4 h-4 text-red-500 shrink-0" />
              <div className="min-w-0">
                <p className="text-sm font-medium text-zinc-100 truncate font-mono-tech">
                  {pdfFile.name}
                </p>
                <p className="text-[11px] text-zinc-400 font-mono-tech">
                  {formatFileSize(pdfFile.size)} • PDF Attached
                </p>
              </div>
            </div>
            <button
              onClick={onFileRemove}
              title="Remove file"
              className="p-1 text-zinc-400 hover:text-red-400 hover:bg-zinc-800 rounded transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        ) : null}

        {/* Error Notification */}
        {errorMessage && (
          <div className="my-2 p-2.5 rounded bg-red-950/40 border border-red-800/80 flex items-center gap-2 text-xs text-red-300 font-mono-tech">
            <AlertCircle className="w-4 h-4 text-red-400 shrink-0" />
            <span>{errorMessage}</span>
          </div>
        )}

        {/* Bottom Bar: Format Tag & Choose PDF Button */}
        <div className="pt-3 mt-3 border-t border-zinc-900 flex items-center justify-between gap-2">
          <span className="font-mono-tech text-[11px] uppercase tracking-wider text-red-500/90 font-medium">
            Format: PDF Only
          </span>

          <button
            type="button"
            onClick={triggerFileInput}
            className="group flex items-center gap-1.5 px-3 py-1.5 rounded text-xs font-mono-tech uppercase tracking-wider bg-zinc-900 hover:bg-red-600 border border-zinc-750 hover:border-red-500 text-zinc-200 hover:text-white transition-all duration-200 cursor-pointer shadow-sm"
          >
            <span>{pdfFile ? 'Change PDF' : 'Choose PDF'}</span>
            <ArrowUpRight className="w-3.5 h-3.5 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
          </button>
        </div>
      </div>
    </div>
  );
}

