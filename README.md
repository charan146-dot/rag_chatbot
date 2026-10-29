# College PDF Chatbot (RAG from Scratch)

A minimal, high-aesthetic application for learning Retrieval-Augmented Generation (RAG) practically from scratch.

---

## 🎨 UI Overview (React + Tailwind CSS)

Inspired by the academic workstation template with a **Black & Red** aesthetic:
- **01 / Document Source**: Editorial typography + PDF upload box with "Choose PDF" button (PDF-only restricted) and selected filename display.
- **02 / Inquiry Console**: System status callout + "Ask anything about your PDF..." input with adjacent Send button.
- **Header & Footer**: Clean technical telemetry bars (`ACADEMIC PORTAL`, `NO PDF LOADED` / `1 PDF LOADED`, `RESET`, `PDF PARSER: READY`).

---

## 📁 Project Structure

```text
ragchat/
├── frontend/                   # Modern React + Tailwind CSS UI
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx          # Top navigation & status pill
│   │   │   ├── PdfUploader.jsx     # Choose PDF button, drag & drop, filename display
│   │   │   ├── InquiryConsole.jsx  # Question input ("Ask anything about your PDF...") & Send button
│   │   │   └── Footer.jsx          # Bottom status & telemetry bar
│   │   ├── App.jsx                 # Main layout & architectural vector styling
│   │   ├── index.css               # Tailwind CSS imports & typography
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── app.py                      # (Optional) Python Streamlit UI prototype
├── requirements.txt            # Python dependencies
└── src/                        # Modular Python RAG backend placeholders
    ├── config.py
    ├── document_processor.py   # PDF text extraction & chunking stubs
    ├── embeddings.py           # Vector embedding stubs
    ├── vector_store.py         # Vector similarity search stubs
    └── rag_pipeline.py         # Retrieval + LLM orchestration stubs
```

---

## 🚀 How to Run the React UI

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Open your browser at the displayed local URL (default: `http://localhost:5173`).
