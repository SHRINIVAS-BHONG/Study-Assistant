<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>📚 PDF Study Assistant - README</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      line-height: 1.6;
      margin: 2rem auto;
      max-width: 960px;
      padding: 1rem;
      background: #f9f9f9;
    }
    h1, h2, h3 {
      color: #2c3e50;
    }
    code {
      background: #eef;
      padding: 0.2em 0.4em;
      border-radius: 4px;
    }
    .section {
      margin-bottom: 2rem;
    }
  </style>
</head>
<body>
  <h1>📚 PDF Study Assistant - Streamlit App</h1>
  <p>This Streamlit-based application allows users to upload PDF documents and interact with them through summarization, quiz generation, and a powerful AI chatbot interface. It's designed to serve as a smart learning assistant.</p>

  <div class="section">
    <h2>1. 📄 PDF Processing</h2>
    <p>
      The function <code>process_pdf()</code> handles both text-based and image-based PDFs:
    </p>
    <ul>
      <li>First, it tries to extract text using <code>pdfplumber</code>.</li>
      <li>If no text is found, it falls back to OCR using <code>pytesseract</code> and <code>pdf2image</code>.</li>
    </ul>
  </div>

  <div class="section">
    <h2>2. 🖥️ Streamlit UI Setup</h2>
    <p>
      Sets up the app page using <code>st.set_page_config()</code> and initializes session state for handling:
    </p>
    <ul>
      <li>Uploaded files</li>
      <li>Generated summaries</li>
      <li>Quizzes and answers</li>
      <li>Chat history</li>
    </ul>
    <p>
      It also defines custom CSS for enhanced visuals, including styled buttons and message bubbles.
    </p>
  </div>

  <div class="section">
    <h2>3. 🔝 Header & File Upload</h2>
    <p>
      Displays a header and file uploader for PDF input:
    </p>
    <ul>
      <li><code>st.file_uploader()</code> lets users select a PDF document.</li>
      <li>The app resets session states if a new file is uploaded.</li>
    </ul>
  </div>

  <div class="section">
    <h2>4. 🚀 Main Processing Logic</h2>
    <p>
      Once the PDF is uploaded:
    </p>
    <ul>
      <li>The content is processed and chunked into smaller segments using <code>RecursiveCharacterTextSplitter</code>.</li>
      <li>Embeddings are generated with Google Generative AI.</li>
      <li>A vector store is created using FAISS for retrieval-augmented generation.</li>
      <li>LLM initialized via <code>ChatGroq</code> (LLaMA3).</li>
    </ul>
  </div>

  <div class="section">
    <h2>5. 💬 Chatbot Interface</h2>
    <p>
      Users can interact with the AI to ask questions or issue commands:
    </p>
    <ul>
      <li>Supported commands include <code>/summary</code> and <code>/quiz</code>.</li>
      <li>Responses maintain LaTeX support for formulas.</li>
      <li>Conversation history is styled and saved in session state.</li>
    </ul>
  </div>

  <div class="section">
    <h2>6. 📄 PDF Tools - Summary & Quiz Generator</h2>
    <p>
      Below the chatbot, two main functionalities are available:
    </p>
    <h3>📝 Generate Summary</h3>
    <ul>
      <li>Creates concise study notes using the LLM.</li>
      <li>Supports mathematical content via LaTeX rendering.</li>
    </ul>

    <h3>🧠 Generate Quiz</h3>
    <ul>
      <li>Generates 3-7 multiple choice questions.</li>
      <li>Each question includes 4 options, one marked as correct.</li>
      <li>Questions and answers are stored in session state.</li>
      <li>Score is calculated on submission and feedback is shown.</li>
    </ul>

    <h3>📊 Quiz Results</h3>
    <ul>
      <li>Displays user's score.</li>
      <li>Shows correct and incorrect answers with explanations.</li>
    </ul>
  </div>

  <div class="section">
    <h2>📦 Dependencies</h2>
    <p>Make sure to install the required packages:</p>
    <pre><code>streamlit
pdfplumber
pytesseract
pdf2image
langchain
langchain-core
langchain-community
google-generativeai
faiss-cpu
python-dotenv
</code></pre>
  </div>

  <div class="section">
    <h2>🚀 Getting Started</h2>
    <p>
      Run the application:
    </p>
    <pre><code>streamlit run app.py</code></pre>
  </div>

  <footer>
    <p>Made with ❤️ using Streamlit, LangChain, and Groq AI.</p>
  </footer>
</body>
</html>
