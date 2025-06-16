# ===============================
# 📦 Imports & Initial Setup
# ===============================
import os
import re
import tempfile
import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import AIMessage, HumanMessage
from PIL import Image
import pdfplumber
import pytesseract

# Document loaders
from langchain_community.document_loaders import (
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
    TextLoader
)

# ===============================
# 🌐 Environment Variables
# ===============================
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
google_api_key = os.getenv("GOOGLE_API_KEY")

# ===============================
# 🧠 Chatbot Functions
# ===============================
def generate_response(command, text_content, llm, vectorstore=None, chat_history=None):
    """
    Generate response based on user command with chat history context
    """
    command = command.lower().strip()
    if command.startswith(("/quiz", "generate quiz", "create quiz")):
        return generate_quiz(text_content, llm)
    elif command.startswith(("/summary", "generate summary", "summarize")):
        return generate_summary(text_content, llm)
    else:
        return answer_question(command, text_content, llm, vectorstore, chat_history)

def generate_quiz(text_content, llm):
    prompt_qa = PromptTemplate(
        template=(
            "Generate 3 to 7 multiple choice questions with 4 options each from the content below.\n"
            "Focus exclusively on conceptual questions only.\n"
            "Number them sequentially as Q1, Q2, etc.\n"
            "Mark the correct option clearly using '<-- correct'.\n"
            "Format each question exactly like this example:\n"
            "Q1: What is the capital of France?\n"
            "A. London\n"
            "B. Paris <-- correct\n"
            "C. Berlin\n"
            "D. Madrid\n"
            "For mathematical questions, use LaTeX format surrounded by $ symbols.\n\n"
            "Content:\n{text}"
        ),
        input_variables=["text"]
    )
    formatted_prompt = prompt_qa.format(text=text_content[:12000])
    response = llm.invoke(formatted_prompt)
    return response.content

def generate_summary(text_content, llm):
    summary_prompt = PromptTemplate(
        template=(
            "Generate a comprehensive summary of the following content. Include:\n"
            "1. Key concepts and main ideas\n"
            "2. Important formulas and equations (presented in LaTeX format between $$ symbols)\n"
            "3. Critical relationships and dependencies\n"
            "4. Practical applications or examples mentioned\n\n"
            "Structure the summary with clear sections and bullet points.\n\n"
            "Content:\n{text}"
        ),
        input_variables=["text"]
    )
    formatted_prompt = summary_prompt.format(text=text_content[:10000])
    response = llm.invoke(formatted_prompt)
    return response.content

def answer_question(question, text_content, llm, vectorstore, chat_history=None):
    """
    Answer user question with context from document and chat history
    """
    # Prepare conversation history context
    history_context = ""
    if chat_history:
        # Format: [Human/AI]: message
        for msg in chat_history:
            if isinstance(msg, HumanMessage):
                history_context += f"Human: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                history_context += f"AI: {msg.content}\n"
    
    # Get document context
    if vectorstore:
        related_docs = vectorstore.invoke(question)
        context = "\n\n".join(doc.page_content for doc in related_docs)
    else:
        context = text_content[:8000]
    
    # Create prompt with history and document context
    qa_prompt = PromptTemplate(
        template=(
            "Use the following conversation history and document context to answer the question.\n\n"
            "CONVERSATION HISTORY:\n{history}\n\n"
            "DOCUMENT CONTEXT:\n{context}\n\n"
            "QUESTION: {question}\n\n"
            "Answer in detail with relevant formulas in LaTeX format ($$...$$). "
            "If unsure, say you don't know."
        ),
        input_variables=["history", "context", "question"]
    )
    
    formatted_prompt = qa_prompt.format(
        history=history_context[:2000],  # Limit history length
        context=context,
        question=question
    )
    
    response = llm.invoke(formatted_prompt)
    return response.content

# ===============================
# 📄 File Processing Function
# ===============================
def process_uploaded_file(uploaded_file, file_type):
    text = ""
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_type) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    try:
        if file_type in [".pdf"]:
            text = ""
            with pdfplumber.open(tmp_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
            if not text.strip():
                st.warning("⚠️ No text extracted from PDF. Trying OCR-based extraction...")
                from pdf2image import convert_from_path
                images = convert_from_path(tmp_path)
                for i, image in enumerate(images):
                    img_path = f"temp_page_{i}.jpg"
                    image.save(img_path, "JPEG")
                    page_text = pytesseract.image_to_string(img_path)
                    text += page_text + "\n\n"
                    os.remove(img_path)

        elif file_type in [".pptx", ".ppt"]:
            loader = UnstructuredPowerPointLoader(tmp_path)
            pages = loader.load()
            text = "\n\n".join([p.page_content for p in pages])

        elif file_type in [".docx", ".doc"]:
            loader = UnstructuredWordDocumentLoader(tmp_path)
            pages = loader.load()
            text = "\n\n".join([p.page_content for p in pages])

        elif file_type in [".txt"]:
            loader = TextLoader(tmp_path)
            pages = loader.load()
            text = pages[0].page_content

        elif file_type in [".jpg", ".jpeg", ".png"]:
            image = Image.open(tmp_path)
            text = pytesseract.image_to_string(image)
            debug_img_path = "ocr_debug.jpg"
            image.save(debug_img_path)
            st.session_state.debug_img_path = debug_img_path
            if not text.strip():
                st.warning("⚠️ No text detected in the image. Please try a clearer image.")
                return None

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None
    finally:
        os.unlink(tmp_path)

    return text

# ===============================
# 🖥️ Streamlit UI Setup
# ===============================
st.set_page_config(page_title="Multi-Format Study Assistant", layout="wide")
st.title("📚 Multi-Format Study Assistant")

# ===============================
# 🧠 Streamlit Session State Init
# ===============================
# Initialize session state variables
session_defaults = {
    "quiz_submitted": False,
    "quiz_score": 0,
    "user_answers": [],
    "questions": [],
    "summary": "",
    "current_file": None,
    "file_type": None,
    "show_summary": False,
    "show_quiz": False,
    "show_chat": False,
    "chat_history": [],
    "text_content": "",
    "vectorstore": None,
    "llm": None,
    "debug_img_path": None
}

for key, default in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ===============================
# 🎨 Custom CSS for Better UI
# ===============================
st.markdown("""
<style>
/* Button styling */
.stButton>button {
    border-radius: 8px;
    border: 1px solid #4CAF50;
    color: white;
    background-color: #4CAF50;
    padding: 10px 24px;
    font-weight: bold;
    transition: all 0.3s;
    margin: 5px;
}

.stButton>button:hover {
    background-color: #45a049;
    transform: scale(1.05);
    border: 1px solid #45a049;
}

/* Chat input styling */
.stChatInput {
    position: fixed;
    bottom: 20px;
    width: 80%;
    left: 10%;
    border-radius: 20px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

/* Header bar */
.header-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    margin-bottom: 20px;
    border-bottom: 1px solid #eee;
}

/* Action buttons container */
.action-buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 20px 0;
}

/* Updated message styling with better contrast */
.user-message {
    background-color: #e3f2fd;
    border-left: 4px solid #2196f3;
    color: #000000;   /* Black text */
    padding: 12px;
    border-radius: 0px 10px 10px 0px;
}

.ai-message {
    background-color: #f1f8e9;
    border-left: 4px solid #4caf50;
    color: #000000;   /* Black text */
    padding: 12px;
    border-radius: 0px 10px 10px 0px;
}

/* Added padding and contrast for chat messages */
[data-testid="stChatMessage"] {
    padding: 5px 0;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 🔝 Header Bar with Chat Toggle
# ===============================
header = st.container()
with header:
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.subheader("Upload documents and interact with AI assistant")
    with col2:
        st.write("")  # Placeholder for chat toggle

# ===============================
# 📁 File Upload UI
# ===============================
uploaded_file = st.file_uploader(
    "📁 Upload your study material (PDF, PPT, Word, Text, or Image)",
    type=["pdf", "pptx", "docx", "doc", "txt"]
)

# ===============================
# 📊 Main Processing Pipeline
# ===============================
if uploaded_file:
    file_name = uploaded_file.name
    file_ext = os.path.splitext(file_name)[1].lower()

    # 🔄 Reset state if a new file is uploaded
    if file_name != st.session_state.current_file:
        for key in session_defaults:
            if key != "debug_img_path":  # Preserve debug image path
                st.session_state[key] = session_defaults[key]
        st.session_state.current_file = file_name
        st.session_state.file_type = file_ext

    with st.spinner(f"Processing {file_name}..."):
        text_content = process_uploaded_file(uploaded_file, file_ext)

    if not text_content:
        st.warning("Failed to extract content from the file. Please try another file.")
        st.stop()

    st.success(f"✅ Successfully processed {file_name}")
    st.session_state.text_content = text_content

    # ✂️ Text Splitting
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_text(text_content)

    # 🧬 Embeddings + FAISS Vectorstore
    embedding = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", google_api_key=google_api_key
    )
    vectorstore = FAISS.from_texts(chunks, embedding=embedding)
    st.session_state.vectorstore = vectorstore.as_retriever(search_kwargs={"k": 4})
    
    # 🧠 Initialize LLM
    st.session_state.llm = ChatGroq(model="llama3-8b-8192", temperature=0.3, groq_api_key=groq_api_key)

    # ===============================
    # 🔝 Update Header with Chat Toggle
    # ===============================
    with header:
        col1, col2 = st.columns([0.8, 0.2])
        with col1:
            st.subheader(f"Working with: {file_name}")
        with col2:
            button_label = "💬 Chat with Document" if not st.session_state.show_chat else "⬅️ Back to Document"
            if st.button(button_label, key="chat_toggle", use_container_width=True):
                st.session_state.show_chat = not st.session_state.show_chat
                if st.session_state.show_chat and not st.session_state.chat_history:
                    welcome_msg = "Hello! I'm your document assistant. Ask me anything about the uploaded document."
                    st.session_state.chat_history.append(AIMessage(content=welcome_msg))
                st.rerun()

# ===============================
# 💬 CHATBOT INTERFACE (PRIMARY VIEW WHEN ACTIVE)
# ===============================
if st.session_state.get("show_chat", False):
    st.subheader("💬 Document Chat Assistant")
    
    # Chat instructions
    with st.expander("How to use the chat", expanded=False):
        st.markdown("""
        - Ask questions about the document
        - Use commands:
            - `/summary` - Generate document summary
            - `/quiz` - Create conceptual quiz
        - Formulas will be displayed in proper mathematical notation
        """)
        st.markdown("**Example commands:**")
        st.code("/summary\n/quiz\nExplain quantum entanglement")
    
    # Display chat history
    for msg in st.session_state.chat_history:
        if isinstance(msg, HumanMessage):
            with st.chat_message("user"):
                st.markdown(f'<div class="user-message">{msg.content}</div>', unsafe_allow_html=True)
        elif isinstance(msg, AIMessage):
            with st.chat_message("assistant"):
                content = msg.content
                # Render LaTeX properly
                content = re.sub(r'\$\$(.*?)\$\$', r'$$\1$$', content, flags=re.DOTALL)
                content = re.sub(r'\$(.*?)\$', r'$\1$', content)
                st.markdown(f'<div class="ai-message">{content}</div>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.chat_input("Ask a question or type command...", key="chat_input")
    if user_input:
        # Add user message to history
        st.session_state.chat_history.append(HumanMessage(content=user_input))
        
        with st.spinner("Thinking..."):
            # Generate response with conversation history
            response = generate_response(
                user_input,
                st.session_state.text_content,
                st.session_state.llm,
                st.session_state.vectorstore,
                chat_history=st.session_state.chat_history[:-1]  # Exclude current message
            )
            # Add AI response to history
            st.session_state.chat_history.append(AIMessage(content=response))
            st.rerun()

# ===============================
# 📄 DOCUMENT PROCESSING VIEW (ONLY SHOWS WHEN CHAT IS INACTIVE)
# ===============================
elif uploaded_file and not st.session_state.show_chat:
    # ===============================
    # 🛠️ Action Buttons (Centered)
    # ===============================
    st.markdown('<div class="action-buttons">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("📝 Generate Summary", use_container_width=True):
            st.session_state.show_quiz = False
            st.session_state.quiz_submitted = False
            with st.spinner("Generating summary..."):
                prompt_summary = PromptTemplate(
                    template=(
                        "Summarize the following content into concise study notes. "
                        "Preserve mathematical equations in LaTeX format surrounded by $ symbols:\n\n"
                        "{text}"
                    ),
                    input_variables=["text"]
                )
                chain = prompt_summary | st.session_state.llm | StrOutputParser()
                st.session_state.summary = chain.invoke({"text": st.session_state.text_content[:10000]})
                st.session_state.show_summary = True

    with col2:
        if st.button("🧠 Generate Interactive Quiz", use_container_width=True):
            st.session_state.show_summary = False
            with st.spinner("Generating quiz..."):
                prompt_qa = PromptTemplate(
                    template=(
                        "Generate 3 to 7 multiple choice questions with 4 options each from the content below.\n"
                        "Number them sequentially as Q1, Q2, etc.\n"
                        "Mark the correct option clearly using '<-- correct'.\n"
                        "Format each question exactly like this example:\n"
                        "Q1: What is the capital of France?\n"
                        "A. London\n"
                        "B. Paris <-- correct\n"
                        "C. Berlin\n"
                        "D. Madrid\n"
                        "For mathematical questions, use LaTeX format surrounded by $ symbols.\n\n"
                        "Content:\n{text}"
                    ),
                    input_variables=["text"]
                )
                chain = prompt_qa | st.session_state.llm | StrOutputParser()
                quiz_raw = chain.invoke({"text": st.session_state.text_content[:12000]})

            # Parse quiz
            questions = []
            q_blocks = re.split(r"\n(?=Q\d+:)", quiz_raw.strip())
            for block in q_blocks:
                lines = block.strip().split("\n")
                if not lines or not lines[0].startswith("Q"):
                    continue

                question_text = lines[0].strip()
                options = []
                correct_answer = None

                for opt in lines[1:]:
                    if not opt.strip():
                        continue
                    clean_opt = opt.replace("<-- correct", "").strip()
                    if "<-- correct" in opt:
                        correct_answer = clean_opt
                    options.append(clean_opt)

                if question_text and options and correct_answer and len(options) >= 4:
                    questions.append({
                        "question": question_text,
                        "options": options[:4],
                        "answer": correct_answer
                    })

            if len(questions) < 3:
                st.warning(f"Only {len(questions)} questions were generated. Please try generating the quiz again.")
            else:
                st.session_state.questions = questions
                st.session_state.quiz_submitted = False
                st.session_state.user_answers = [None] * len(questions)
                st.session_state.quiz_score = 0
                st.session_state.show_quiz = True
    st.markdown('</div>', unsafe_allow_html=True)

    # ===============================
    # 🖼️ OCR Image Display
    # ===============================
    if st.session_state.debug_img_path and os.path.exists(st.session_state.debug_img_path):
        st.subheader("🔍 OCR Preview")
        st.image(st.session_state.debug_img_path, caption="Processed Image", use_column_width=True)
        st.caption("Preview of the image processed for text extraction")

    # ===============================
    # 📃 Summary Display
    # ===============================
    if st.session_state.show_summary and st.session_state.summary:
        st.subheader("📝 Study Notes")
        # Render LaTeX properly
        summary = st.session_state.summary
        summary = re.sub(r'\$\$(.*?)\$\$', r'$$\1$$', summary, flags=re.DOTALL)
        summary = re.sub(r'\$(.*?)\$', r'$\1$', summary)
        st.markdown(summary, unsafe_allow_html=True)

    # ===============================
    # 🧪 Quiz Display
    # ===============================
    if st.session_state.show_quiz and st.session_state.questions:
        st.subheader("🧪 Take the Quiz")
        with st.form("quiz_form"):
            for i, q in enumerate(st.session_state.questions):
                st.markdown(f"**{q['question']}**")
                selected = st.radio(
                    label="Choose your answer:",
                    options=q["options"],
                    key=f"question_{i}",
                    index=None
                )
                st.session_state.user_answers[i] = selected
                st.markdown("---")

            submitted = st.form_submit_button("✅ Submit Quiz")
            if submitted:
                score = 0
                for i, q in enumerate(st.session_state.questions):
                    if st.session_state.user_answers[i] == q["answer"]:
                        score += 1
                st.session_state.quiz_score = score
                st.session_state.quiz_submitted = True
                st.rerun()

    # ===============================
    # 📊 Quiz Results Display
    # ===============================
    if st.session_state.quiz_submitted and st.session_state.questions:
        st.subheader("📊 Quiz Results")
        total = len(st.session_state.questions)

        for i, q in enumerate(st.session_state.questions):
            user_ans = st.session_state.user_answers[i]
            correct_ans = q["answer"]
            is_correct = user_ans == correct_ans

            st.markdown(f"**{q['question']}**")
            st.markdown(f"Your answer: {user_ans or 'Not answered'} {'✅' if is_correct else '❌'}")

            if not is_correct:
                st.markdown(f"{correct_ans}")

            st.markdown("---")

        st.success(f"🎉 Your Score: {st.session_state.quiz_score} / {total}")
        st.balloons()