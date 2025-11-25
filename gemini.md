# Project: Study Notes Summarizer & Quiz Generator Agent

**Objective:** Build an AI agent that extracts text from PDFs, generates study summaries, and creates quizzes based on the *original text*.

## 1. Core Functions

### A) PDF Summarizer
- **Input:** PDF file (uploaded by user).
- **Process:**
  - Extract text using `pypdf`.
  - Clean text (remove artifacts).
  - Generate a structured, learning-optimized summary.
- **Output:** Markdown summary compatible with Streamlit.

### B) Quiz Generator
- **Input:** *Original extracted text* (NOT the summary).
- **Process:**
  - Generate MCQs or mixed-style quizzes.
  - Provide an answer key.
- **Output:** JSON and Markdown formats.

## 2. Architecture & File Structure

```text
.
├── .env                  # API Keys (GEMINI_API_KEY)
├── app.py                # Streamlit UI
├── gemini.md             # Project Rules (This file)
├── pyproject.toml        # Dependencies
├── uploads/              # Raw PDF storage
├── outputs/              # Generated summaries and quizzes
│   ├── summary.md
│   ├── quiz.json
│   └── quiz.md
├── backend/
│   └── modules/
│       └── pdf_reader.py # PyPDF extractor
├── database/
│   └── temp/
│       └── raw_text.txt  # Intermediate text storage
└── agents/
    └── study_agent.py    # AgentCore logic (OpenAgents SDK)
```

## 3. Workflow Pipeline

1.  **Upload:** User uploads PDF -> Saved to `uploads/`.
2.  **Extract:** `backend/modules/pdf_reader.py` reads PDF -> Saves text to `database/temp/raw_text.txt`.
3.  **Process:** `agents/study_agent.py` reads `raw_text.txt`.
    - **Summarize:** Generates `outputs/summary.md`.
    - **Quiz:** Generates `outputs/quiz.json` & `outputs/quiz.md` (using raw text).
4.  **Display:** `app.py` reads outputs and renders UI.

## 4. Technical Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.13+
- **PDF Engine:** `pypdf`
- **AI Model:** Gemini (via `openai-agents` SDK)
- **Tools:** Context7 MCP (if applicable), OpenAgents SDK

## 5. UI Rules

- **Summary:** Display in card/block view or sections.
- **Quiz:** Display in collapsible sections.
- **Style:** Clean, academic, student-friendly.