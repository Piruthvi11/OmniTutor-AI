# 🎓 OmniTutor: Source-Grounded Multimodal Study Assistant
### Multimodal AI Hackathon 2026 (IIT Mandi, Augli.ai, PurpleRain, LDV Labs)
**Track D: Personalized Tutoring & Adaptive Learning**

---

## 👥 Team & Institutional Details

- **Team Name:** **CODEFORGE**
- **Institution:** Bannari Amman Institute of Technology, Sathyamangalam
- **Department:** Department of Electrical and Electronics Engineering (EEE)

| Role | Member Name | Roll / Reg Number | Year & Branch |
| :--- | :--- | :--- | :--- |
| **Team Leader** | **PIRUTHVI M K** | `7376241EE166` | 3rd Year EEE |
| **Member 2** | **SRIRAM B** | `7376241EE195` | 3rd Year EEE |
| **Member 3** | **VIKAS P** | `7376241EE212` | 3rd Year EEE |
| **Member 4** | **GOBUNATH D** | `7376241EE125` | 3rd Year EEE |

- **Faculty Mentor:** **Prof. SRITHA P** (Staff ID: `EE1747`), Department of EEE

---

## 🌟 Project Overview
**OmniTutor** is an intelligent multimodal study companion built to solve the **Fragmented Study Paradox** in engineering education. It unifies lecture videos, slide presentations, and syllabus question bank PDFs into a single source-grounded session.

### 🚀 Key Capabilities
1. **Multimodal Ingestion Pipeline:** Natively parses MP4 video recordings, MP3 audio waveforms, and PDF course question banks.
2. **Zero-Hallucination Source Citations:** Every AI explanation cites exact video timestamps (`[Video: MM:SS]`) and document page numbers (`[Page: #]`).
3. **Agentic Adaptive Assessment:** Dynamically generates MCQs with automated difficulty adjustment (*Easy*, *Medium*, *Hard*) based on student accuracy.
4. **Automated Knowledge Gap Diagnosis:** Detects conceptual misconceptions and formulates customized 3-step remedial roadmaps.
5. **360° Competency Radar Profile:** Live visual analytics dashboard built with Chart.js and Plotly.

---

## 🏗️ System Architecture
```text
  [ Lecture Video (.mp4) ]   [ Slide Deck (.pdf) ]   [ Question Bank (.pdf) ]
                             │
                             ▼
         ┌───────────────────────────────────────┐
         │     Multimodal Ingestion Pipeline     │
         │ (Audio Transcripts + OCR + Embeddings)│
         └───────────────────┬───────────────────┘
                             │
                             ▼
         ┌───────────────────────────────────────┐
         │    Google Gemini Multimodal Engine    │
         │       (1M+ Token Context Window)      │
         └───────────────────┬───────────────────┘
                             │
            ┌────────────────┴────────────────┐
            ▼                                 ▼
   [ Source-Cited RAG ]             [ Agentic Diagnostic Engine ]
   - Video Timestamp Links          - Dynamic MCQ Generation
   - Slide/Page Grounding           - Knowledge Gap Mapping
            │                                 │
            └────────────────┬────────────────┘
                             ▼
          [ Modern Web UI / Streamlit Dashboard ]
          (Realtime Chat, Video Sync, Radar Analytics)
```

---

## 🛠️ Quick Start & Running the Application

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Modern Full-Stack Web App (Recommended)
```bash
python server.py
```
Open **`http://localhost:8000`** in your browser.

### 3. Run the Streamlit Interactive Dashboard
```bash
streamlit run app.py
```
Open **`http://localhost:8501`** in your browser.

---

## 📁 Key Submission Files
- **Final Pitch Deck (PowerPoint):** [`CODEFORGE_OmniTutor_Final_Submission.pptx`](./CODEFORGE_OmniTutor_Final_Submission.pptx)
- **Slide Script & Speaker Notes:** [`presentation_slides.md`](./presentation_slides.md)
- **FastAPI Backend Server:** [`server.py`](./server.py)
- **Modern Responsive Frontend:** [`static/index.html`](./static/index.html), [`static/app.js`](./static/app.js)
- **Streamlit Prototype:** [`app.py`](./app.py)
