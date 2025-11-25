import streamlit as st
import os
import json
from app_agents.study_agent import AgentCore

from dotenv import load_dotenv
from backend.modules.pdf_reader import extract_text_from_pdf
from app_agents.study_agent import AgentCore
load_dotenv()
# Configure page

st.set_page_config(
    page_title="PdfText Summarizer with Quiz Generators",
    page_icon="📒",
    layout="wide"
)

# Initialize Agent
@st.cache_resource
def get_agent():
    try:
        return AgentCore()
    except Exception as e:
        st.error(f"Failed to initialize Agent: {e}")
        return None

agent = get_agent()

def save_uploaded_file(uploaded_file):
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def save_text(text):
    if not os.path.exists("database/temp"):
        os.makedirs("database/temp")
    with open("database/temp/raw_text.txt", "w", encoding="utf-8") as f:
        f.write(text)

def save_output(filename, content):
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    with open(os.path.join("outputs", filename), "w", encoding="utf-8") as f:
        f.write(content)

# UI Layout
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #1e1e2f 0%, #2a2a40 100%);
        color: #e0e0e0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Headings */
    h1, h2, h3 {
        color: #ffffff;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    /* Tabs (Navbar) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #008080; /* Teal */
        font-weight: bold;
        border-radius: 4px;
        padding: 10px 20px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #ff4b4b; /* Red */
        background-color: rgba(255, 75, 75, 0.1);
    }
    .stTabs [aria-selected="true"] {
        color: #008080 !important;
        border-bottom-color: #008080 !important;
    }
    
    /* Cards */
    .card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .card:hover {
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Summary Section */
    .summary-box {
        background: rgba(40, 44, 52, 0.8);
        border-left: 4px solid #008080; /* Teal border */
        padding: 20px;
        border-radius: 0 8px 8px 0;
    }
    
    /* Quiz Options */
    .quiz-option {
        background: rgba(255, 255, 255, 0.05);
        padding: 10px 15px;
        border-radius: 6px;
        margin: 5px 0;
        border: 1px solid transparent;
        transition: all 0.2s;
    }
    .quiz-option:hover {
        background: rgba(255, 255, 255, 0.1);
        border-color: #008080; /* Teal border */
        cursor: pointer;
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("PdfText Summarizer with Quiz Generators")

with st.sidebar:
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    # Process PDF
    file_path = save_uploaded_file(uploaded_file)
    
    with st.spinner("Extracting text from PDF..."):
        text = extract_text_from_pdf(file_path)
        save_text(text)
    
    if text:
        st.success("PDF processed successfully!")
        
        # Tabs for Summary and Quiz
        tab1, tab2 = st.tabs(["📝 Summary", "❓ Quiz"])
        
        with tab1:
            st.subheader("Study Summary")
            if st.button("Generate Summary"):
                if agent:
                    with st.spinner("Generating summary..."):
                        summary = agent.generate_summary(text)
                        save_output("summary.md", summary)
                        
                        # Render summary in a nice HTML container
                        st.markdown(f"""
                        <div class="card summary-box">
                            {summary}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.error("Agent not initialized. Check API Key.")
        
        with tab2:
            st.subheader("Quiz Generator")
            if st.button("Create Quiz"):
                if agent:
                    with st.spinner("Generating quiz from original text..."):
                        quiz_json_str = agent.generate_quiz(text)
                        
                        # Clean the string if it has markdown code blocks
                        if "```json" in quiz_json_str:
                            quiz_json_str = quiz_json_str.split("```json")[1].split("```")[0].strip()
                        elif "```" in quiz_json_str:
                            quiz_json_str = quiz_json_str.split("```")[1].split("```")[0].strip()
                            
                        save_output("quiz.json", quiz_json_str)
                        
                        try:
                            quiz_data = json.loads(quiz_json_str)
                            if "questions" in quiz_data:
                                for i, q in enumerate(quiz_data["questions"]):
                                    # Use HTML for question card
                                    st.markdown(f"""
                                    <div class="card">
                                        <h4>Question {i+1}</h4>
                                        <p style="font-size: 1.1em;">{q.get('question', 'Unknown')}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Use expander for answer to keep it interactive/hidden
                                    with st.expander(f"Show Answer"):
                                        if q.get('type') == 'mcq':
                                            st.markdown('<div style="margin-left: 20px;">', unsafe_allow_html=True)
                                            for opt in q.get('options', []):
                                                st.markdown(f'<div class="quiz-option">{opt}</div>', unsafe_allow_html=True)
                                            st.markdown('</div>', unsafe_allow_html=True)
                                            st.success(f"**Correct Answer:** {q.get('answer')}")
                                        else:
                                            st.info(f"**Answer:** {q.get('answer')}")
                            else:
                                st.warning("Quiz format unexpected. Displaying raw output.")
                                st.json(quiz_data)
                        except json.JSONDecodeError:
                            st.error("Failed to parse quiz JSON. Displaying raw output.")
                            st.text(quiz_json_str)
                else:
                    st.error("Agent not initialized. Check API Key.")

    else:
        st.error("Could not extract text from the PDF.")

