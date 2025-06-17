<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PDF Study Assistant - Features</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 20px auto;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        }
        h1, h2, h3 {
            color: #2c3e50;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
            margin-top: 30px;
        }
        h1 {
            text-align: center;
            font-size: 2.5em;
            color: #4CAF50;
            border-bottom: none;
            padding-bottom: 0;
            margin-bottom: 20px;
        }
        h2 {
            font-size: 1.8em;
        }
        h3 {
            font-size: 1.4em;
            color: #34495e;
            border-bottom: 1px dashed #ccc;
            padding-bottom: 5px;
            margin-top: 25px;
        }
        .feature-section {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 6px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.03);
        }
        .feature-section p {
            margin-bottom: 10px;
        }
        .feature-section ul {
            list-style-type: disc;
            margin-left: 20px;
            padding-left: 0;
        }
        .feature-section ul li {
            margin-bottom: 8px;
        }
        .icon {
            font-size: 1.2em;
            margin-right: 8px;
            color: #4CAF50;
        }
        .note {
            background-color: #ecf0f1;
            border-left: 5px solid #3498db;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
            color: #2c3e50;
        }
        .code-example {
            background-color: #eee;
            border-left: 3px solid #f39c12;
            padding: 10px;
            margin: 10px 0;
            font-family: 'Courier New', Courier, monospace;
            white-space: pre-wrap;
            word-break: break-all;
            border-radius: 4px;
        }
    </style>
</head>
<body>

    <h1>📚 PDF Study Assistant</h1>
    <p style="text-align: center; font-size: 1.1em; color: #555;">Your intelligent companion for mastering PDF study materials.</p>

    <div class="note">
        This document outlines the core functionalities of the PDF Study Assistant, designed to enhance your learning experience through AI-powered tools.
    </div>

    <h2>🌟 Key Functionalities</h2>

    <div class="feature-section">
        <h3><span class="icon">📁</span> Robust PDF Processing</h3>
        <p>The application is equipped with advanced PDF handling capabilities, ensuring that your study materials are accurately processed regardless of their format.</p>
        <ul>
            <li><b>Standard Text Extraction:</b> Leverages `pdfplumber` to extract text from standard, text-based PDFs efficiently.</li>
            <li><b>Optical Character Recognition (OCR):</b> If direct text extraction fails (e.g., for scanned documents or image-based PDFs), the application seamlessly switches to `pytesseract` to perform OCR, converting images within the PDF into searchable and readable text. This ensures comprehensive coverage and accessibility for diverse document types.</li>
            <li><b>Temporary File Management:</b> Securely handles uploaded files using temporary storage, ensuring privacy and efficient resource management.</li>
        </ul>
    </div>

    <div class="feature-section">
        <h3><span class="icon">💬</span> Interactive Chat with PDF</h3>
        <p>Engage in a dynamic conversation with your PDF document. This feature allows you to ask specific questions about the content and receive relevant, detailed answers.</p>
        <ul>
            <li><b>Context-Aware Responses:</b> Utilizes `LangChain` and `FAISS` to create a vector store from your PDF content, enabling the AI to retrieve and reference the most relevant sections of the document when answering your questions.</li>
            <li><b>Conversation History:</b> Maintains a memory of your chat, allowing for follow-up questions and more coherent discussions.</li>
            <li><b>LaTeX Support:</b> Automatically renders mathematical formulas and equations in beautiful LaTeX format ($$E=mc^2$$) within the chat responses, making it ideal for technical and scientific documents.</li>
            <li><b>Direct Commands:</b> Supports special commands within the chat for quick actions:
                <div class="code-example">
                    /summary<br>
                    /quiz<br>
                    Explain the concept of [topic]
                </div>
            </li>
        </ul>
    </div>

    <div class="feature-section">
        <h3><span class="icon">📝</span> Comprehensive Summary Generation</h3>
        <p>Quickly grasp the essence of your PDF content with an AI-generated summary. This feature is perfect for reviewing long documents or getting a high-level overview.</p>
        <ul>
            <li><b>Key Concepts & Main Ideas:</b> Extracts and presents the most important information.</li>
            <li><b>Formulas and Equations:</b> Identifies and includes crucial mathematical expressions, presented in LaTeX format for clarity.</li>
            <li><b>Critical Relationships:</b> Highlights dependencies and connections between different concepts discussed in the document.</li>
            <li><b>Practical Applications:</b> Points out real-world examples or applications mentioned within the text.</li>
            <li><b>Structured Output:</b> Delivers summaries with clear sections and bullet points for easy readability.</li>
        </ul>
    </div>

    <div class="feature-section">
        <h3><span class="icon">🧠</span> Dynamic Quiz Generation</h3>
        <p>Test your understanding with custom quizzes generated directly from your PDF. This interactive feature helps in active recall and self-assessment.</p>
        <ul>
            <li><b>Multiple Choice Questions:</b> Generates 3 to 7 multiple-choice questions with four options each.</li>
            <li><b>Correct Answer Indication:</b> Clearly marks the correct answer for each question.</li>
            <li><b>LaTeX Integration:</b> Questions and options can include mathematical formulas rendered in LaTeX.</li>
            <li><b>Interactive Quiz Interface:</b> Users can select answers directly within the application.</li>
            <li><b>Instant Feedback:</b> Upon submission, the application calculates and displays your score, and provides detailed feedback on correct and incorrect answers, including the correct solution.</li>
            <li><b>Quiz Retake Option:</b> Allows users to easily retry the quiz for repeated practice.</li>
        </ul>
    </div>

    <div class="feature-section">
        <h3><span class="icon">🚀</span> Powered by Modern AI</h3>
        <p>The PDF Study Assistant leverages state-of-the-art Large Language Models (LLMs) and embedding technologies to deliver intelligent and accurate responses.</p>
        <ul>
            <li><b>Google Generative AI Embeddings:</b> Used for creating dense vector representations of the PDF content, enabling efficient semantic search.</li>
            <li><b>Groq Chat API (`llama3-8b-8192`):</b> Powers the conversational and content generation capabilities, ensuring fast and relevant AI interactions.</li>
        </ul>
    </div>

    <div class="feature-section">
        <h3><span class="icon">✨</span> Intuitive User Interface (Streamlit)</h3>
        <p>Built with Streamlit, the application features a clean, responsive, and user-friendly interface for a seamless study experience.</p>
        <ul>
            <li><b>Clear Navigation:</b> Easy toggling between chat and PDF tools views.</li>
            <li><b>Session Management:</b> Intelligent session state handling ensures a smooth experience, especially when switching between different PDF files.</li>
            <li><b>Custom Styling:</b> Enhanced visual appeal with custom CSS for buttons, chat messages, and overall layout.</li>
        </ul>
    </div>

</body>
</html>
```


