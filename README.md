# 🤖 AI-Powered Study Assistant

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue" alt="Python">
  <img src="https://img.shields.io/badge/Framework-Streamlit-red" alt="Streamlit">
  <img src="https://img.shields.io/badge/LLM-Llama3--8b-brightgreen" alt="Llama3">
  <img src="https://img.shields.io/badge/OCR-Tesseract-yellowgreen" alt="Tesseract">
  <br>
  <strong>Transform your study materials into interactive learning experiences</strong>
</div>

## 🌟 Introduction
The AI-Powered Study Assistant is an intelligent application that processes various document formats to create interactive learning experiences. Using advanced AI models, OCR technology, and natural language processing, it transforms static study materials into dynamic, engaging content with quizzes, summaries, and Q&A capabilities.

![App Workflow](https://via.placeholder.com/800x400.png?text=Document+Processing+Workflow+Diagram)

## 🚀 Key Features

### 📁 Multi-Format Document Processing
- **PDF Documents**: Text extraction with OCR fallback for scanned documents
- **Microsoft Office**: Full support for PPTX, PPT, DOCX, and DOC files
- **Images**: Text extraction from JPG, PNG using OCR
- **Text Files**: Direct processing of TXT files

```python
# File processing function snippet
def process_uploaded_file(uploaded_file, file_type):
    if file_type == ".pdf":
        # PDF processing logic
    elif file_type in [".pptx", ".ppt"]:
        # PowerPoint processing
    elif file_type in [".jpg", ".jpeg", ".png"]:
        # Image OCR processing
