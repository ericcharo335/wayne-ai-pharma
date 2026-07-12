# Wayne AI Pharma 🧬

**Clinical trials 10x faster. 20x cheaper. Built for Africa.**

Wayne AI Pharma is a production-ready SaaS web app that helps African hospitals and pharmaceutical companies run clinical trials faster and cheaper than traditional consultancies like McKinsey.

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Add your Codex API key
Copy the secrets template and add your Codex, OpenAI API key:
```bash
# Edit .streamlit/secrets.toml
CODEWX_API_KEY = "sk-cs4-your-key-here"
```

Get your API key at: https://console.anthropic.com/

### 3. Run the app
```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## 🔒 Security Features

| Feature | Implementation |
|---|---|
| **Authentication** | Email + Password with bcrypt hashing |
| **Data Isolation** | Every query filtered by `user_id` |
| **File Encryption** | AES (Fernet) encryption before saving to SQLite |
| **PHI Redaction** | Auto-redacts names, emails, phones before AI API |
| **Auto-Delete** | Configurable 90-day data retention policy |
| **No AI Training** | Your data is never used to train models |
| **HTTPS** | Provided by Streamlit Cloud / Replit |

---

## 📋 Features

### 1. Authentication System
- Signup with email + strong password
- Login / Logout with session management
- Password hashing with bcrypt

### 2. Main Dashboard
- Quick access to all features
- Stats overview (total analyses, avg confidence)
- Recent analyses preview

### 3. Trial Analyzer (Core)
Upload PDF or DOCX documents and get:
1. **Predicted Timeline** — vs McKinsey average (18 months)
2. **Predicted Cost** — vs McKinsey average ($4.2M)
3. **Top 5 Risks in Africa** — with specific mitigation strategies
4. **PPB/NAFDAC/SAHPRA/EDA Compliance Scores** — with checklist
5. **Patient Recruitment Rates** — by country (Kenya, Nigeria, SA, Egypt)
6. **Why This Beats McKinsey** — Africa-specific advantage analysis

### 4. Downloadable PDF Reports
- Professionally formatted PDF with fpdf2
- Includes all 6 analysis sections
- Encrypted before storage

### 5. Account Settings
- Data retention controls
- View data stats
- "Delete All My Data" button

---

## 🏗️ Tech Stack

| Component | Technology |
|---|---|
| **Frontend** | Streamlit |
| **AI** | OpenAI-compatible API (Codex) via `openai` SDK |
| **Database** | SQLite3 with WAL mode |
| **Auth** | bcrypt password hashing |
| **PDF Extract** | PyPDF2 |
| **DOCX Extract** | python-docx |
| **PDF Generate** | fpdf2 |
| **Encryption** | cryptography (Fernet / AES) |
| **PHI Redaction** | Regex-based redaction |

---

## 📁 Project Structure

```
wayne-ai-pharma/
├── app.py                  # Main entry point + page router
├── config.py               # Constants, colors, benchmarks
├── database.py             # SQLite operations + Fernet encryption
├── auth.py                 # Login/signup + password hashing
├── document_processor.py   # PDF/DOCX extraction + PHI redaction
├── claude_client.py        # OpenAI-compatible API integration
├── pdf_report.py           # fpdf2 report generator
├── ui_components.py        # Shared UI: CSS, cards, metrics
├── pages_login.py          # Login / Signup page
├── pages_dashboard.py      # Main dashboard page
├── pages_analyzer.py      # Trial Analyzer page (core)
├── pages_history.py       # Past analyses page
├── pages_settings.py      # Account settings page
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── secrets.toml        # API key configuration
└── wayne_pharma.db         # SQLite database (auto-created)
```

---

## 🌍 African Regulatory Focus

The app provides compliance analysis for:
- **PPB** — Pharmacy and Poisons Board (Kenya)
- **NAFDAC** — National Agency for Food and Drug Administration and Control (Nigeria)
- **SAHPRA** — South African Health Products Regulatory Authority
- **EDA** — Egyptian Drug Authority

---

## 📜 Disclaimer

All data encrypted. We do not train AI on your data. HIPAA/PPB aligned. This tool provides AI-generated analysis for informational purposes only and does not constitute legal or regulatory advice.
