# resume-analyzer
AI Resume Analyzer FastApi + Classifier (ML) (with Web UI)- React
<div align="center">

# 📄 Resume Analyzer
### AI-Powered Resume Parsing & Role Classification System

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-Vite-61DAFB?style=for-the-badge&logo=react)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn)
![spaCy](https://img.shields.io/badge/spaCy-NLP-09A3D5?style=for-the-badge&logo=spacy)

<p align="center">
  <a href="#-about-the-project">About</a> •
  <a href="#-key-features">Features</a> •
  <a href="#-system-architecture">Architecture</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-local-setup">Setup</a>
</p>

</div>

---

## 🧠 About the Project

**Resume Analyzer** is an AI + NLP powered web application designed to bridge the gap between candidate resumes and job descriptions. It parses resumes (PDF/Text), extracts structured data, and intelligently classifies candidates into professional roles using a **hybrid Machine Learning + Rule-Based approach.**

Unlike rigid parsers, this project handles real-world variability in resume formatting, making it a robust tool for automated screening.






---

## ✨ Key Features

| Feature | Description |
| :--- | :--- |
| **📂 Resume Upload** | Drag & drop PDF support with instant preview and replace options. |
| **🧠 Smart Extraction** | Extracts Name, Email, Phone, and Skills using hybrid NLP logic. |
| **📊 Experience Engine** | Calculates total experience years from varied date formats (e.g., "Jan 2020 - Present", "2019-2023"). |
| **🎯 Role Classification** | Predicts roles (e.g., "Python Developer") using **TF-IDF + Classifier** with keyword boosting. |
| **🖥️ Modern UI** | Clean React interface with loading spinners, confidence bars, and JSON result displays. |

---

## 🏗️ System Architecture

mermaid 
    A[User / Client] -->|Upload PDF| B(React Frontend);
    B -->|REST API Request| C{FastAPI Backend};
    C -->|1. Parse PDF| D[pdfplumber];
    C -->|2. Extract Entities| E[spaCy NLP];
    C -->|3. Predict Role| F[ML Model + Rules];
    F -->|Result JSON| B;
## 🧱 Tech Stack

### 🔧 Backend
* **FastAPI:** High-performance REST API.
* **scikit-learn:** TF-IDF Vectorization and Classification models.
* **spaCy:** NLP for Named Entity Recognition (NER) and noun chunks.
* **pdfplumber:** Robust PDF text extraction.
* **Joblib:** Model persistence and loading.

### 🎨 Frontend
* **React (Vite):** Fast, modern frontend framework.
* **Axios:** HTTP client for API communication.
* **CSS Modules:** Scoped styling for clean UI components.

### ☁️ Deployment
* **Frontend:** Vercel
* **Backend:** Railway / Fly.io

---

## 🔍 Logic & Algorithms

### 1. Skill Extraction Strategy (Hybrid)
We avoid rigid matching by combining two methods:
* **Primary (High Precision):** Dictionary-based matching with word-boundary safety (avoids matching "Go" in "Good").
* **Fallback (NLP-Based):** spaCy noun-phrase extraction with noise filtering/blacklisting.

### 2. Role Classification (The "Brain")
A hybrid decision system ensures high accuracy:
1.  **ML Prediction:** TF-IDF vectorizes the resume text $\rightarrow$ Probabilistic Classifier predicts the role.
2.  **Rule-Based Boosting:** Domain-specific keywords boost the score.
    * *Example:* If ML predicts "Data Scientist" but keywords strictly match "Frontend", the system adjusts the confidence.

### 3. Experience Levels

| Years of Experience | Level |
| :--- | :--- |
| **< 1** | Fresher |
| **1 – 3** | Junior |
| **3 – 6** | Mid-Level |
| **6 – 10** | Senior |
| **10+** | Lead / Architect |

---

## ⚙️ Local Setup

Follow these steps to run the project locally.

### 1. Backend Setup

```bash
cd backend
python -m venv venv

# Activate Virtual Environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```
### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```
Status: Frontend runs at http://localhost:5173🧪 API ReferenceMethodEndpointDescriptionPOST/analyzeUpload a resume file for analysisRequest: multipart/form-data (File)Response:
```
JSON{
  "name": "John Doe",
  "email": "john@gmail.com",
  "phone": "+88017xxxxxxx",
  "skills": ["Python", "FastAPI", "Machine Learning"],
  "experience_years": 3.7,
  "experience_level": "Mid",
  "classification": "AI/ML Engineer",
  "confidence": 0.89
}
```
## 🚧 Limitations & Future Roadmap

**Current Constraints:**
* ⚠️ Resume formats vary widely; OCR is not yet implemented for image-based PDFs.
* ⚠️ Experience calculation relies on explicitly stated dates.

**🔮 Roadmap:**
* [ ] Add confidence scoring for individual skills.
* [ ] Resume section segmentation (Education vs. Work).
* [ ] Multi-language support.
* [ ] Dockerized deployment.

---

<div align="center">

## 👨‍💻 Author

**Md Sakib**
<br>
*Undergraduate CSE Student & AI/Full-Stack Enthusiast*

<a href="https://github.com/mdsakib-dr">
  <img src="https://img.shields.io/badge/GitHub-@mdsakib--dr-181717?style=for-the-badge&logo=github" alt="GitHub" />
</a>

<br><br>

⭐ <b>Liked this project?</b>
<br>
<i>Give it a star to show your support!</i>

</div>
