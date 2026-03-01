# 🚀 AI Resume Optimizer

An AI-powered web application that helps candidates evaluate how well their resume matches a job description using **Natural Language Processing (NLP)** and **Deep Learning**.

🔗 **Live App:**  
https://resumeaioptimizer.streamlit.app/

---

## 📌 Project Overview

AI Resume Optimizer is designed to assist job seekers in improving their resumes before applying for jobs.

Instead of relying on simple keyword matching, this system uses **semantic AI analysis** to understand the meaning and context between a resume and a job description.

The application provides:

- Job fit score
- Skill match percentage
- Missing skills detection
- AI-based recommendations

---

## 🎯 Problem Statement

Many candidates apply for jobs without knowing whether their resume aligns with the job requirements.

Traditional systems rely on keyword matching, which often misses context and meaning.

This project solves that problem by using **semantic similarity models** to provide intelligent resume feedback.

---

## ⭐ Key Features

✔ Upload Resume (PDF / DOCX)  
✔ Semantic Resume vs Job Description Matching  
✔ Skill Gap Analysis  
✔ Final Job Fit Scoring System  
✔ AI Recommendation Engine  
✔ Modern Interactive Web Interface  

---

## 🧠 AI & NLP Concepts Used

- Sentence Transformers (SBERT)
- Semantic Similarity (Cosine Similarity)
- Text Preprocessing & Cleaning
- Skill Extraction Logic
- Weighted Scoring System

---

## 🏗️ System Architecture

```
Resume File (PDF/DOCX)
        ↓
Resume Parser
        ↓
Text Cleaning
        ↓
Skill Extraction
        ↓
Semantic Matching (Deep Learning)
        ↓
Skill Gap Analysis
        ↓
Scoring Engine
        ↓
AI Recommendation
        ↓
Streamlit Web Interface
```

---

## 🧩 Project Structure

```
AI_RESUME_OPTIMIZER/
│
├── app/
│   └── main.py                # Streamlit UI
│
├── core/
│   ├── matching_engine.py     # Semantic similarity model
│   ├── skill_gap.py           # Skill comparison logic
│   └── scoring.py             # Final scoring system
│
├── preprocessing/
│   ├── resume_parser.py       # PDF/DOCX parser
│   ├── text_cleaning.py       # NLP cleaning
│   └── skill_extractor.py     # Skill extraction
│
├── data/
│   └── skill_dictionary.json
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Technologies Used

### Programming Language
- Python

### Framework
- Streamlit

### AI / Machine Learning
- Sentence Transformers
- Scikit-learn
- PyTorch

### Data Processing
- NumPy
- Pandas

### Document Parsing
- PyPDF
- python-docx

---

## 🚀 How to Run Locally

### 1️⃣ Clone Repository

```bash
git clone https://github.com/suroora/AI-Resume-Optimizer.git
cd AI-Resume-Optimizer
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run Application

```bash
streamlit run app/main.py
```

---

## 🌐 Live Demo

🔗 https://resumeaioptimizer.streamlit.app/

---

## 💡 Future Improvements

- AI-based resume improvement suggestions
- Industry-specific skill intelligence
- Resume rewrite assistant
- Downloadable analysis report
- Advanced visualization dashboard

---

## 👩‍💻 Author

**Suroora Fathima**  
AI / Data Science Project

---

## 📄 License

This project is for educational and portfolio purposes.

