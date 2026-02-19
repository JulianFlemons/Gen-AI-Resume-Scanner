# 🗂️ GenAI ATS Resume Scanner

An AI-powered resume scanner that analyzes resumes against job descriptions, providing real-time match scores, skill gap analysis, and AI-generated candidate insights — built with Streamlit and Mistral-7B via the Hugging Face Inference API.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Mistral--7B-yellow?logo=huggingface)
![License](https://img.shields.io/badge/License-MIT-green)
<img width="1434" height="854" alt="Screenshot 2026-02-19 at 2 50 02 PM" src="https://github.com/user-attachments/assets/223d89d3-a0cb-4f1f-866c-1be0ef0dcb52" />
<img width="1439" height="853" alt="Screenshot 2026-02-19 at 2 49 52 PM" src="https://github.com/user-attachments/assets/844f85f5-1542-427e-9e6d-fa910f0d4994" />
<img width="1437" height="852" alt="Screenshot 2026-02-19 at 2 50 53 PM" src="https://github.com/user-attachments/assets/368c64d9-c82e-4f82-be05-0a0edf3dde40" />

<img width="1435" height="804" alt="Screenshot 2026-02-19 at 2 53 43 PM" src="https://github.com/user-attachments/assets/a0237af8-97c8-4ba4-bf52-3fdd876fdd16" />

---

## 📸 Demo

> Upload a resume → Paste a job description → Get instant AI-powered analysis

---

## ✨ Features

- 📄 **Resume Parsing** — Supports PDF and DOCX file uploads
- 📊 **ATS Scoring Engine** — Scores resume against job description across Skills (50%), Experience (30%), and Education (20%)
- 🤖 **AI-Powered Analysis** — Uses Mistral-7B-Instruct to generate:
  - Overall fit rating (1–10)
  - Matched and missing skills
  - Candidate strengths
  - Actionable improvement suggestions
  - 2-3 sentence summary
- 📉 **Visual Dashboard** — Gauge chart, skill gap bar chart, and score breakdown powered by Plotly
- 🔒 **Privacy First** — Open-source model via HF API; no candidate data stored

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| AI Model | Mistral-7B-Instruct-v0.2 |
| AI Provider | Hugging Face Inference API |
| PDF Parsing | pdfplumber |
| DOCX Parsing | python-docx |
| Visualizations | Plotly |
| Language | Python 3.11 |

---

## 🚀 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/genai-resume-scanner.git
cd genai-resume-scanner
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a Hugging Face API token
- Go to [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- Create a new token with **"Make calls to Inference Providers"** permission
- Copy the token

### 4. Run the app
```bash
streamlit run app.py
```

### 5. Use the app
1. Upload a resume (PDF or DOCX) in the sidebar
2. Paste the job description
3. Enter your Hugging Face API token
4. Click **"Run AI Analysis"**

---

## 📁 Project Structure

```
genai-resume-scanner/
├── app.py              # Main Streamlit app (UI + AI logic)
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

---

## 📦 Requirements

```
streamlit
pdfplumber
python-docx
plotly
pandas
huggingface-hub
```

---

## 🧠 How It Works

1. **Text Extraction** — Resume text is extracted from PDF or DOCX using `pdfplumber` and `python-docx`
2. **Section Parsing** — Resume is split into sections (Skills, Experience, Education, Projects, Certifications) using keyword matching
3. **Scoring Engine** — Keywords from the job description are compared against resume sections using token matching with weighted scores
4. **AI Analysis** — Resume text and job description are sent to Mistral-7B-Instruct via the HF Inference API with a structured prompt engineering approach
5. **JSON Parsing** — A 3-layer fallback parser ensures reliable structured output from the LLM response
6. **Visualization** — Results are rendered as interactive Plotly charts in the Streamlit dashboard

---

## 🔑 Key Engineering Decisions

- **Chose Mistral-7B over GPT-4o** — Open-source model keeps candidate PII off proprietary model providers, reducing privacy risk
- **Migrated from local 20B model to HF Inference API** — Solved inference latency issues while maintaining open-source model benefits
- **3-layer JSON fallback parser** — Handles edge cases where the LLM wraps output in markdown or adds extra text, ensuring reliable parsing
- **Prompt engineering with low temperature (0.1)** — Keeps AI output deterministic and structured for consistent JSON responses

---

## 🔮 Future Improvements

- [ ] Add support for multiple resume uploads (batch scanning)
- [ ] Export results as PDF report
- [ ] Add LinkedIn profile URL parsing
- [ ] Deploy to Streamlit Cloud
- [ ] Add support for additional AI providers (OpenAI, Claude)

---

## 👤 Author

**Julian Flemons**
- LinkedIn: https://www.linkedin.com/in/julian-flemons-18689b228/


---

