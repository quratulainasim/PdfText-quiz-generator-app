# PdfText Summarizer with Quiz Generators

A Streamlit application that extracts text from PDF files, generates summaries, and creates quizzes using AI agents.

## Features

- **PDF Text Extraction**: Upload any PDF to extract its text content.
- **AI Summary**: Generate concise summaries of the document.
- **Quiz Generator**: Create interactive quizzes (MCQ and Open-ended) based on the content.
- **Interactive UI**: Clean and modern interface built with Streamlit.

## Local Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd PdfText-quiz-generator-app
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_api_key_here
    ```

5.  **Run the application:**
    ```bash
    streamlit run app.py
    ```

## Deployment on Streamlit Cloud

1.  Push your code to a GitHub repository.
2.  Log in to [Streamlit Cloud](https://streamlit.io/cloud).
3.  Click "New app".
4.  Select your repository, branch, and main file (`app.py`).
5.  **Advanced Settings:**
    - Go to "Secrets" and add your `OPENAI_API_KEY`:
      ```toml
      OPENAI_API_KEY = "sk-..."
      ```
6.  Click "Deploy".

## Requirements

- Python 3.13+
- OpenAI API Key
