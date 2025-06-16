<h1>📚 Multi-Format Study Assistant</h1>

<p>Welcome to the <strong>Multi-Format Study Assistant</strong>, your AI-powered tool for uploading study materials (PDFs, PPTs, Word docs, images, etc.) and generating:</p>

<ul>
  <li>📝 Smart summaries</li>
  <li>🧠 Conceptual quizzes</li>
  <li>💬 Chat interface for interactive Q&A</li>
</ul>

<p>This app is built using <strong>Streamlit</strong> and <strong>LangChain</strong> with support from <strong>Google Generative AI</strong>, <strong>FAISS</strong>, and <strong>OCR</strong> libraries.</p>

<hr>

<h2>🚀 Features Overview</h2>

<h3>1. 🔄 Session Initialization</h3>
<ul>
  <li>Initializes <code>st.session_state</code> with default values for tracking uploaded file, extracted text, quiz, summary, chat history, and vector store.</li>
  <li>Ensures smooth multi-component state management.</li>
</ul>

<h3>2. 🎨 Styled UI and Header</h3>
<ul>
  <li>Custom CSS for buttons, messages, chat inputs.</li>
  <li>Header shows current file and a toggle between chat and document view.</li>
  <li><code>setup_ui()</code> and <code>show_header()</code> manage this.</li>
</ul>

<h3>3. 📂 Multi-Format File Uploader</h3>
<ul>
  <li>Supports: <code>.pdf</code>, <code>.pptx</code>, <code>.docx</code>, <code>.doc</code>, <code>.txt</code>, <code>.jpg</code>, <code>.jpeg</code>, <code>.png</code></li>
  <li>Automatically detects and uses OCR if PDFs/images lack extractable text.</li>
  <li><code>process_uploaded_file()</code> handles format detection and text extraction:</li>
  <ul>
    <li>PDF: <code>pdfplumber</code> and fallback to OCR using <code>pytesseract</code></li>
    <li>PPT/DOC/TXT: via <code>Unstructured</code> loaders</li>
    <li>Images: directly OCR with preview saved</li>
  </ul>
</ul>

<h3>4. 🧠 AI Interaction & Commands</h3>
<ul>
  <li>Central chat command handler using <code>generate_response()</code></li>
  <ul>
    <li><code>/summary</code> → calls <code>generate_summary()</code></li>
    <li><code>/quiz</code> → calls <code>generate_quiz()</code></li>
    <li>Custom questions → <code>answer_question()</code> uses vectorstore or full context</li>
  </ul>
  <li><strong>Summary Generator:</strong></li>
  <ul>
    <li>Extracts key concepts, equations, applications with LaTeX formatting</li>
  </ul>
  <li><strong>Quiz Generator:</strong></li>
  <ul>
    <li>3 to 7 multiple-choice conceptual questions</li>
    <li>Answers marked with <code>&lt;-- correct</code></li>
    <li>Supports LaTeX formatting for math</li>
  </ul>
  <li><strong>Chat Interface:</strong></li>
  <ul>
    <li>Fully styled conversation interface</li>
    <li>Retains chat history context for follow-ups</li>
    <li>Accepts commands and natural language questions</li>
  </ul>
</ul>

<h3>5. 📑 Document Interaction View</h3>
<ul>
  <li><code>show_document_processing_view()</code> provides:</li>
  <ul>
    <li>Summary view with sectioned notes</li>
    <li>Quiz generation form and evaluation</li>
    <li>Display of OCR processed image if used</li>
  </ul>
  <li><strong>Interactive quiz form:</strong></li>
  <ul>
    <li>Uses <code>st.form()</code> for user selections</li>
    <li>Calculates score and displays detailed results</li>
    <li>Celebratory balloons and scorecard</li>
  </ul>
</ul>

<hr>

<h2>🛠️ How It Works</h2>
<ol>
  <li><strong>Upload File:</strong> File is saved temporarily and detected by extension.</li>
  <li><strong>Text Extraction:</strong></li>
  <ul>
    <li>Uses <code>pdfplumber</code>, <code>Unstructured</code>, or <code>pytesseract</code></li>
    <li>Image fallback and OCR preview if needed</li>
  </ul>
  <li><strong>Text Saved:</strong> Extracted content saved to <code>st.session_state.text_content</code></li>
  <li><strong>LLM Invocations:</strong></li>
  <ul>
    <li>Summary and quiz generation use LangChain’s <code>PromptTemplate</code> + Google Generative AI</li>
    <li>Questions use retrieval-augmented generation (RAG) if <code>vectorstore</code> is present</li>
  </ul>
  <li><strong>Chat Memory:</strong></li>
  <ul>
    <li>Chat history (Human + AI messages) used to generate contextual answers</li>
    <li>Stored persistently across interactions</li>
  </ul>
</ol>

<hr>

<h2>✅ Requirements</h2>
<p>Make sure to install required packages:</p>
<pre><code>pip install streamlit langchain langchain-community langchain-core langchain-google-genai pdfplumber pytesseract pillow faiss-cpu
</code></pre>
<p>Ensure you have <a href="https://github.com/tesseract-ocr/tesseract">Tesseract-OCR</a> installed and accessible in PATH.</p>

<hr>

<h2>📌 Folder Structure</h2>
<pre><code>├── app.py                       # Main Streamlit launcher (not shown here)
├── session_state.py            # initialize_session_state()
├── ui.py                       # setup_ui(), show_header(), show_file_uploader()
├── file_processor.py           # process_uploaded_file()
├── chat.py                     # generate_response(), chat, summary, quiz logic
├── document_view.py            # show_document_processing_view()
└── README.md                   # This file
</code></pre>

<hr>

<h2>💡 Tips</h2>
<ul>
  <li>Use clear, structured documents for best results</li>
  <li>Images must be readable for OCR to work properly</li>
  <li>Use <code>/summary</code> or <code>/quiz</code> commands in chat for quick interaction</li>
</ul>

<hr>

<h2>🙌 Credits</h2>
<p>Made using:</p>
<ul>
  <li>OpenAI + LangChain + Google Generative AI</li>
  <li>Streamlit</li>
  <li>FAISS</li>
  <li>OCR (Tesseract)</li>
</ul>

<p>This project is ideal for students, educators, and learners who want to turn study material into interactive content.</p>

<hr>

<p>Happy Learning! ✨</p>

