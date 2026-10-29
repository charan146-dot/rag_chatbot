"""College PDF Chatbot - Academic Portal.

Styled after the academic workstation template with a Black & Red brutalist aesthetic.
Stage 2: PDF Text Extraction (PyPDF).
Stage 3: Text Chunking with metadata & unique chunk IDs.
"""

import streamlit as st
from src import config
from src.pdf_loader import extract_pages_from_pdf
from src.chunker import chunk_document_pages

# 1. Page Configuration
st.set_page_config(
    page_title="Academic Portal | College Document Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Bespoke Black & Red CSS Styling Matching Template
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700;800&display=swap');

    /* Global Reset & Dark Theme */
    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Space Grotesk', -apple-system, sans-serif !important;
        background-color: #060608 !important;
        color: #f4f4f5 !important;
    }

    /* Hide Streamlit Header, Toolbar, Footer & Sidebar toggle */
    header[data-testid="stHeader"], footer, #MainMenu, .stDeployButton, [data-testid="stSidebarCollapseButton"] {
        display: none !important;
        visibility: hidden !important;
        height: 0px !important;
    }
    
    [data-testid="stSidebar"] {
        display: none !important;
    }

    /* Page Container */
    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 1.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 1440px !important;
    }

    /* Typography Classes */
    .font-mono-tech {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Outer Workspace Frame */
    .academic-frame {
        border: 1px solid #222226;
        border-radius: 8px;
        background: #09090c;
        position: relative;
        overflow: hidden;
    }

    /* Top Nav Bar */
    .top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #1f1f23;
        padding: 0.9rem 1.6rem;
        background: rgba(10, 10, 13, 0.9);
        backdrop-filter: blur(8px);
    }
    .brand-mark {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        font-weight: 700;
        color: #e4e4e7;
    }
    .brand-squares {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 2px;
        width: 15px;
        height: 15px;
    }
    .brand-squares div:nth-child(1), .brand-squares div:nth-child(4) {
        background-color: #dc2626;
        border-radius: 1px;
    }
    .brand-squares div:nth-child(2), .brand-squares div:nth-child(3) {
        background-color: #52525b;
        border-radius: 1px;
    }
    .nav-center {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        letter-spacing: 0.45em;
        text-transform: uppercase;
        color: #71717a;
    }

    /* Card Panels */
    .source-card {
        background-color: #0e0e12;
        border: 1px dashed #27272a;
        border-radius: 8px;
        padding: 1.25rem;
        transition: border-color 0.2s ease;
    }
    .source-card:hover {
        border-color: #dc2626;
    }
    
    .console-card {
        background-color: #0c0c10;
        border: 1px solid #222226;
        border-radius: 8px;
        padding: 1.6rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    /* Callout with red left accent */
    .system-callout {
        border-left: 3px solid #dc2626;
        padding-left: 1rem;
        margin-bottom: 1.2rem;
    }

    /* File Uploader Customization */
    [data-testid="stFileUploader"] {
        background-color: #121217 !important;
        border: 1px dashed #27272a !important;
        border-radius: 6px !important;
        padding: 0.5rem !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #ef4444 !important;
    }
    [data-testid="stFileUploaderDropzone"] {
        background-color: transparent !important;
        border: none !important;
        padding: 0.6rem !important;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background-color: #1c1c22 !important;
        border: 1px solid #3f3f46 !important;
        color: #f4f4f5 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stFileUploaderDropzone"] button:hover {
        background-color: #dc2626 !important;
        border-color: #ef4444 !important;
        color: white !important;
    }

    /* Inputs */
    .stTextInput input {
        background-color: #131318 !important;
        border: 1px solid #27272a !important;
        color: #f4f4f5 !important;
        border-radius: 6px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        padding: 0.7rem 1rem !important;
    }
    .stTextInput input:focus {
        border-color: #dc2626 !important;
        box-shadow: 0 0 0 1px #dc2626 !important;
    }

    /* Primary Buttons */
    .stButton > button {
        background-color: #dc2626 !important;
        color: #ffffff !important;
        border: 1px solid #ef4444 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        border-radius: 6px !important;
        padding: 0.6rem 1.2rem !important;
        font-weight: 600 !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover {
        background-color: #b91c1c !important;
        border-color: #f87171 !important;
        transform: translateY(-1px);
    }

    /* Outline Reset Button */
    .reset-btn > button {
        background-color: transparent !important;
        border: 1px solid #27272a !important;
        color: #a1a1aa !important;
        font-size: 0.75rem !important;
        padding: 0.25rem 0.75rem !important;
    }
    .reset-btn > button:hover {
        border-color: #dc2626 !important;
        color: #ef4444 !important;
        background-color: rgba(220, 38, 38, 0.1) !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        color: #ef4444 !important;
        font-size: 1.35rem !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricLabel"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.12em !important;
        color: #71717a !important;
    }

    /* Text Area */
    .stTextArea textarea {
        background-color: #0b0b0e !important;
        border: 1px solid #222226 !important;
        color: #e4e4e7 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        line-height: 1.6 !important;
        border-radius: 6px !important;
    }

    /* Selectbox */
    [data-testid="stSelectbox"] > div > div {
        background-color: #121217 !important;
        border: 1px solid #27272a !important;
        color: #f4f4f5 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #111115 !important;
        border: 1px solid #222226 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        color: #d4d4d8 !important;
        border-radius: 6px !important;
    }

    /* Alerts */
    [data-testid="stAlert"] {
        background-color: #170d10 !important;
        border: 1px solid #7f1d1d !important;
        color: #fca5a5 !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        border-radius: 6px !important;
    }

    /* Footer */
    .bottom-footer {
        border-top: 1px solid #1f1f23;
        padding: 0.8rem 1.6rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        color: #71717a;
        background: #08080a;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Session State Initialization
if "uploaded_pdf" not in st.session_state:
    st.session_state.uploaded_pdf = None
if "last_question" not in st.session_state:
    st.session_state.last_question = ""

# 4. Top Header Bar Matching Template
top_col1, top_col2, top_col3 = st.columns([4, 4, 4])
with top_col1:
    st.markdown(
        """
        <div class="brand-mark" style="padding-top: 6px;">
            <div class="brand-squares">
                <div></div><div></div><div></div><div></div>
            </div>
            <span>Academic Portal</span>
        </div>
        """,
        unsafe_allow_html=True
    )
with top_col2:
    st.markdown(
        """
        <div class="nav-center" style="text-align: center; padding-top: 8px;">
            C O L L E G E
        </div>
        """,
        unsafe_allow_html=True
    )
with top_col3:
    status_subcol1, status_subcol2 = st.columns([2.8, 1.2])
    with status_subcol1:
        # Dynamic PDF Loaded Pill populated below
        pass
    with status_subcol2:
        st.markdown('<div class="reset-btn">', unsafe_allow_html=True)
        if st.button("RESET", key="reset_app_btn"):
            st.session_state.uploaded_pdf = None
            st.session_state.last_question = ""
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr style='border: none; border-bottom: 1px solid #1c1c20; margin: 0.6rem 0 1.6rem 0;'>", unsafe_allow_html=True)

# 5. Main Canvas - 2 Columns (Document Source vs. Inquiry Console)
col_source, col_console = st.columns([5, 7], gap="large")

extraction_result = None
chunking_result = None

# ==================== LEFT COLUMN: DOCUMENT SOURCE ====================
with col_source:
    st.markdown(
        """
        <div class="font-mono-tech" style="font-size: 0.72rem; color: #ef4444; letter-spacing: 0.18em; text-transform: uppercase; font-weight: 600; margin-bottom: 0.6rem;">
            01 / DOCUMENT SOURCE
        </div>
        <h1 style="font-size: 3.4rem; font-weight: 800; line-height: 0.92; letter-spacing: -0.03em; text-transform: uppercase; margin: 0 0 1rem 0; color: #f4f4f5;">
            CAMPUS —<br>
            <span style="color: #e4e4e7;">KNOWLEDGE</span><br>
            <span style="color: #ef4444;">ASSISTANT</span>
        </h1>
        <p style="color: #8a8a93; font-size: 0.92rem; line-height: 1.55; margin-bottom: 1.4rem; max-width: 440px;">
            Upload your college syllabus, academic handbook, or lecture PDF and enter your question below for instant, grounded answers.
        </p>
        """,
        unsafe_allow_html=True
    )

    # UPLOAD PDF DOCUMENT BOX
    st.markdown(
        """
        <div class="source-card">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.6rem;">
                <div style="display: flex; align-items: center; gap: 0.7rem;">
                    <div style="width: 32px; height: 32px; background: #18181d; border: 1px solid #27272a; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: #ef4444;">
                        📄
                    </div>
                    <div>
                        <div class="font-mono-tech" style="font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; color: #f4f4f5;">
                            Upload PDF Document
                        </div>
                        <div style="font-size: 0.72rem; color: #71717a;">
                            Drag & drop a .pdf file here or click to browse
                        </div>
                    </div>
                </div>
                <div class="font-mono-tech" style="font-size: 0.75rem; color: #52525b; letter-spacing: 0.1em;">
                    01 / 02
                </div>
            </div>
        """,
        unsafe_allow_html=True
    )

    # Streamlit PDF File Uploader (Restricted to PDF only)
    uploaded_file = st.file_uploader(
        label="PDF Upload",
        type=["pdf"],
        label_visibility="collapsed",
        key="college_pdf_uploader"
    )

    if uploaded_file is not None:
        st.session_state.uploaded_pdf = uploaded_file
        file_size_kb = len(uploaded_file.getvalue()) / 1024
        
        # Stage 2: Perform PDF extraction via src/pdf_loader.py
        extraction_result = extract_pages_from_pdf(uploaded_file)

        # Stage 3: Perform Chunking on the extracted pages
        if extraction_result["success"]:
            chunking_result = chunk_document_pages(
                pages=extraction_result["pages"],
                source_name=uploaded_file.name,
                chunk_size=config.DEFAULT_CHUNK_SIZE,
                chunk_overlap=config.DEFAULT_CHUNK_OVERLAP
            )

        st.markdown(
            f"""
            <div style="margin: 0.6rem 0; padding: 0.6rem 0.8rem; background: #131317; border: 1px solid #27272a; border-radius: 4px; display: flex; justify-content: space-between; align-items: center;">
                <div class="font-mono-tech" style="font-size: 0.78rem; color: #f4f4f5; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; max-width: 280px;">
                    📎 {uploaded_file.name}
                </div>
                <div class="font-mono-tech" style="font-size: 0.72rem; color: #ef4444;">
                    {file_size_kb:.1f} KB
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        """
            <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #1a1a20; padding-top: 0.6rem; margin-top: 0.6rem;">
                <span class="font-mono-tech" style="font-size: 0.68rem; color: #ef4444; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 600;">
                    FORMAT: PDF ONLY
                </span>
                <span class="font-mono-tech" style="font-size: 0.68rem; color: #71717a;">
                    SELECT FILE ↗
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Document Extraction & Chunking Summary Metrics
    if extraction_result is not None:
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
        if extraction_result["success"]:
            met1, met2, met3, met4 = st.columns(4)
            met1.metric("Pages", extraction_result["total_pages"])
            met2.metric("Readable", extraction_result["readable_pages"])
            met3.metric("Empty", extraction_result["empty_pages"])
            total_c = chunking_result["total_chunks"] if chunking_result else 0
            met4.metric("Chunks", total_c)
        else:
            st.error(f"Error: {extraction_result['error']}")

# Update Top Nav status dynamically based on uploaded PDF & chunks
with status_subcol1:
    if uploaded_file is not None and extraction_result and extraction_result["success"]:
        c_count = chunking_result["total_chunks"] if chunking_result else 0
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: flex-end; gap: 6px; padding-top: 6px;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #ef4444; display: inline-block;"></span>
                <span class="font-mono-tech" style="font-size: 0.72rem; color: #e4e4e7; letter-spacing: 0.08em; text-transform: uppercase;">
                    {extraction_result['total_pages']}P / {c_count} CHUNKS
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="display: flex; align-items: center; justify-content: flex-end; gap: 6px; padding-top: 6px;">
                <span style="width: 8px; height: 8px; border-radius: 50%; background: #52525b; display: inline-block;"></span>
                <span class="font-mono-tech" style="font-size: 0.72rem; color: #71717a; letter-spacing: 0.08em; text-transform: uppercase;">
                    NO PDF LOADED
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )


# ==================== RIGHT COLUMN: INQUIRY CONSOLE ====================
with col_console:
    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
            <div class="font-mono-tech" style="font-size: 0.72rem; color: #e4e4e7; letter-spacing: 0.18em; text-transform: uppercase; font-weight: 600; display: flex; align-items: center; gap: 6px;">
                <span style="width: 7px; height: 7px; border-radius: 50%; background: #dc2626; display: inline-block;"></span>
                02 / INQUIRY CONSOLE
            </div>
            <div class="font-mono-tech" style="font-size: 0.72rem; color: #71717a; letter-spacing: 0.12em; text-transform: uppercase;">
                {f"{chunking_result['total_chunks']} CHUNKS READY" if chunking_result and chunking_result['total_chunks'] > 0 else ('PDF READY' if uploaded_file else '00 MESSAGES')}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Console Card Container
    with st.container():
        # SYSTEM READY Callout
        st.markdown(
            """
            <div class="system-callout">
                <div class="font-mono-tech" style="font-size: 0.7rem; color: #ef4444; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 0.3rem;">
                    SYSTEM READY
                </div>
                <div style="color: #d4d4d8; font-size: 0.88rem; line-height: 1.55;">
                    Welcome to the College Document Assistant. Please upload a course or institutional PDF on the left, then type your question in the text field below.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # STAGE 2 & 3: Inspection Sections for Extracted Pages and Chunks
        if extraction_result is not None and extraction_result["success"]:
            # Warning for scanned / image-only documents
            if extraction_result["is_scanned_or_empty"]:
                st.warning(f"⚠️ {extraction_result['warning']}")
            elif extraction_result["warning"]:
                st.info(f"ℹ️ {extraction_result['warning']}")

            # STAGE 3 INSPECTOR: Inspect Generated Chunks
            if chunking_result is not None and chunking_result["total_chunks"] > 0:
                with st.expander(f"🧩 VERIFY GENERATED CHUNKS (STAGE 3 — {chunking_result['total_chunks']} CHUNKS)", expanded=True):
                    c_col1, c_col2, c_col3 = st.columns(3)
                    c_col1.metric("Total Chunks", chunking_result["total_chunks"])
                    c_col2.metric("Avg Chunk Size", f"{chunking_result['avg_chunk_size']} chars")
                    c_col3.metric("Size / Overlap", f"{chunking_result['chunk_size']} / {chunking_result['chunk_overlap']}")

                    # Select Chunk by unique identifier
                    chunk_opts = list(range(chunking_result["total_chunks"]))
                    selected_idx = st.selectbox(
                        label="Select Chunk to Inspect:",
                        options=chunk_opts,
                        format_func=lambda idx: (
                            f"[{chunking_result['chunks'][idx]['chunk_id']}] "
                            f"Page {chunking_result['chunks'][idx]['metadata']['page_number']} "
                            f"({chunking_result['chunks'][idx]['char_count']} chars)"
                        ),
                        key="chunk_inspector_select"
                    )

                    active_chunk = chunking_result["chunks"][selected_idx]
                    meta = active_chunk["metadata"]

                    # Chunk Metadata Badge
                    st.markdown(
                        f"""
                        <div style="margin: 0.4rem 0 0.6rem 0; padding: 0.45rem 0.8rem; background: #121217; border: 1px solid #27272a; border-radius: 4px; display: flex; flex-wrap: wrap; gap: 1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;">
                            <div><span style="color: #71717a;">CHUNK ID:</span> <span style="color: #ef4444; font-weight: 700;">{active_chunk['chunk_id']}</span></div>
                            <div><span style="color: #71717a;">PAGE:</span> <span style="color: #f4f4f5;">{meta['page_number']}</span></div>
                            <div><span style="color: #71717a;">CHARS:</span> <span style="color: #f4f4f5;">{active_chunk['char_count']}</span></div>
                            <div><span style="color: #71717a;">SPAN:</span> <span style="color: #a1a1aa;">[{meta['start_char']}:{meta['end_char']}]</span></div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Chunk Content View
                    st.text_area(
                        label=f"Content of {active_chunk['chunk_id']}:",
                        value=active_chunk["text"],
                        height=130,
                        disabled=True,
                        key=f"chunk_val_{active_chunk['chunk_id']}"
                    )

                    # View All Chunks Combined
                    with st.expander("📜 View All Chunks Combined", expanded=False):
                        for c in chunking_result["chunks"]:
                            st.markdown(
                                f"**`{c['chunk_id']}` (Page {c['metadata']['page_number']} — {c['char_count']} chars):**"
                            )
                            st.code(c["text"], language="text")

            # STAGE 2 INSPECTOR: Inspect Raw Extracted Pages
            if extraction_result["total_pages"] > 0:
                with st.expander("📄 VERIFY EXTRACTED TEXT (PAGE BY PAGE)", expanded=False):
                    page_options = [p["page_number"] for p in extraction_result["pages"]]
                    selected_page = st.selectbox(
                        label="Select Page to Inspect:",
                        options=page_options,
                        format_func=lambda num: f"Page {num} — {extraction_result['pages'][num - 1]['char_count']} characters",
                        key="page_inspector_select"
                    )

                    curr_page = extraction_result["pages"][selected_page - 1]
                    if curr_page["is_empty"]:
                        st.warning(f"Page {selected_page} contains no readable text (empty page or diagram).")
                    else:
                        st.text_area(
                            label=f"Text Extracted from Page {selected_page}:",
                            value=curr_page["text"],
                            height=140,
                            disabled=True,
                            key=f"page_text_{selected_page}"
                        )

        elif uploaded_file is None:
            # Subtle console placeholder aesthetic
            st.markdown(
                """
                <div style="height: 160px; border: 1px solid #1a1a20; border-radius: 6px; background: #08080a; display: flex; align-items: center; justify-content: center; color: #3f3f46; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; letter-spacing: 0.1em; text-transform: uppercase;">
                    [ Console Waiting for PDF Document Ingestion ]
                </div>
                """,
                unsafe_allow_html=True
            )

        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

        # Bottom Input Area Matching Template
        input_col, btn_col = st.columns([10, 2])
        with input_col:
            user_question = st.text_input(
                label="Ask Question",
                placeholder="Ask anything about your PDF...",
                label_visibility="collapsed",
                key="rag_question_input"
            )
        with btn_col:
            send_clicked = st.button("SEND ↗", key="send_question_btn", use_container_width=True)

        st.markdown(
            """
            <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 0.3rem;">
                <span style="font-size: 0.72rem; color: #71717a;">
                    Attach a PDF document and enter text to query the assistant.
                </span>
                <span class="font-mono-tech" style="font-size: 0.68rem; color: #52525b; letter-spacing: 0.1em;">
                    PRESS ENTER ↵
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Handling Question Submission (Clear Stage 3 placeholder feedback)
        if send_clicked or user_question:
            if not user_question.strip():
                st.warning("Please type a question before submitting.")
            elif uploaded_file is None:
                st.warning("Please upload a PDF document on the left first.")
            else:
                c_num = chunking_result["total_chunks"] if chunking_result else 0
                st.markdown(
                    f"""
                    <div style="margin-top: 1rem; padding: 0.8rem 1rem; background: #121217; border-left: 2px solid #ef4444; border-radius: 0 4px 4px 0;">
                        <div class="font-mono-tech" style="font-size: 0.75rem; color: #ef4444; text-transform: uppercase; font-weight: 700;">
                            QUESTION RECEIVED
                        </div>
                        <div style="color: #f4f4f5; font-size: 0.85rem; margin: 0.2rem 0;">
                            "{user_question}"
                        </div>
                        <div class="font-mono-tech" style="font-size: 0.7rem; color: #71717a;">
                            Text extraction (Stage 2) and chunking (Stage 3) complete with {c_num} chunks ready for embedding. Vector indexing and LLM retrieval will execute in upcoming stages.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# 6. Bottom Technical Footer Bar Matching Template
st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="bottom-footer">
        <div>INSTITUTIONAL DOCUMENT INTERFACE</div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="width: 6px; height: 6px; border-radius: 50%; background: #ef4444;"></span>
            <span>PDF PARSER: READY</span>
        </div>
        <div>© ACADEMIC AI</div>
    </div>
    """,
    unsafe_allow_html=True
)
