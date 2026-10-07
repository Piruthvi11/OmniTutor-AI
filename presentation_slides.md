# 🎓 OmniTutor: Source-Grounded Multimodal Study Assistant
**IIT Mandi Multimodal AI Hackathon 2026** | **Track D: Personalized Tutoring & Adaptive Learning**

---

## 📌 Slide 1: Title Slide
- **Project Name:** OmniTutor: Source-Grounded Multimodal Study Assistant
- **Track:** Track D — Personalized Tutoring & Adaptive Learning
- **Team Name:** CODEFORGE
- **Team Leader:** PIRUTHVI M K (`7376241EE166`) — 3rd Year EEE
- **Team Members:**
  - SRIRAM B (`7376241EE195`) — 3rd Year EEE
  - VIKAS P (`7376241EE212`) — 3rd Year EEE
  - GOBUNATH D (`7376241EE125`) — 3rd Year EEE
- **Faculty Mentor:** Prof. SRITHA P (Staff ID: `EE1747`), Dept. of EEE
- **Institution:** Bannari Amman Institute of Technology, Sathyamangalam

> **🗣️ Speaker Notes:**  
> *"Good morning respected judges and mentors. We are Team CODEFORGE from Bannari Amman Institute of Technology. Today, we present OmniTutor — an autonomous multimodal study assistant designed to turn lecture videos, slides, and question bank PDFs into an interactive, source-grounded learning companion with exact video timestamps and adaptive quizzes."*

---

## 📌 Slide 2: Why We Built This: Real Student Pain Points
- **Time Wasted Finding Explanations:** Finding a 2-minute formula derivation in a 90-minute lecture video takes 20+ minutes of manual scrubbing.
- **Disconnected Course Materials:** Semester question banks, PPT slides, and recorded lecture videos exist in separate silos.
- **ChatGPT / Gemini Hallucinations:** Standard LLMs provide generic textbook answers that frequently do not match syllabus requirements.
- **Static Practice Tests:** Traditional question banks cannot identify root-cause misconceptions or adapt question difficulty to individual student weaknesses.

> **🗣️ Speaker Notes:**  
> *"As 3rd year engineering students, when exams approach, we waste hours scrubbing through long recordings just to find where a specific formula was derived. Generic AI chatbots fail to provide video proof or align with the specific syllabus taught by our professors."*

---

## 📌 Slide 3: Our Solution: How OmniTutor Works
- **All-in-One Multi-Format Ingestion:** Ingests MP4 video lectures, MP3 audio, and course question bank PDFs seamlessly.
- **Verified Timestamps & Page References:** Every explanation provides exact video markers like `[Video: 12:40]` and slide numbers `[Slide: 14]`.
- **Adaptive Practice Quizzes:** Generates dynamic MCQs by module and automatically scales difficulty (*Easy*, *Medium*, *Hard*).
- **Targeted Revision Plan:** Pinpoints missed questions and highlights the exact video timestamp range and slide page for remedial review.

> **🗣️ Speaker Notes:**  
> *"OmniTutor unifies lecture recordings and question bank PDFs, answers doubts with verified timestamp citations so you never waste time searching, and generates personalized quizzes that adapt to your mastery level."*

---

## 📌 Slide 4: System Pipeline & Implementation
- **1. Document Ingestion:** Extracts audio transcripts, slide text, and OCR diagrams via PyPDF and video frame parsers.
- **2. Multimodal RAG Engine:** Passes media handles to Gemini 1.5 (1M context) to retrieve answers grounded strictly on uploaded materials.
- **3. Diagnostic Agent:** Analyzes quiz submissions, calculates topic mastery percentages, and maps student weak spots.
- **4. Interactive Dashboard:** Responsive web frontend built with FastAPI, Tailwind CSS, and Chart.js for radar analytics.

> **🗣️ Speaker Notes:**  
> *"Our pipeline parses lecture media and PDFs, feeds them into a multimodal RAG engine for zero-hallucination citations, and uses an agentic evaluation module to track student mastery."*

---

## 📌 Slide 5: Core Features & Prototype Demo
- **Instant Citation Q&A:** Ask any conceptual or numerical doubt and get step-by-step math with verified video timecodes.
- **Topic Extraction:** Automatically identifies core syllabus modules from the uploaded PDF/video.
- **Interactive Quiz Engine:** Dynamic MCQs with immediate feedback, option explanations, and source references.
- **Competency Radar Chart:** Visual 360-degree graph showing exact proficiency across each course module.

> **🗣️ Speaker Notes:**  
> *"We tested OmniTutor with our departmental Question Bank (22EE501). The system accurately retrieved analytical formulas with page citations and updated our competency radar graph in real time."*

---

## 📌 Slide 6: Technical Stack & Reliability
- **AI Models:** Google Gemini 1.5 Flash (for high-speed multimodal reasoning) with auto-model fallback.
- **Backend Framework:** Python 3.14 + FastAPI + Uvicorn for lightweight REST API endpoints.
- **Local Document Fallback:** Built-in local PDF parser ensures the app works smoothly even in offline demo mode.
- **Frontend:** Modern HTML5, Tailwind CSS, Lucide icons, and Chart.js visualizations.

> **🗣️ Speaker Notes:**  
> *"We chose FastAPI and Python for low latency and high reliability. We also built an offline document fallback so the system never crashes during a live demo."*

---

## 📌 Slide 7: Future Scope & Conclusion
- **Voice Tutor Mode:** Adding speech-to-speech interaction for hands-free problem solving.
- **College LMS Integration:** Connecting directly to Moodle / Google Classroom so professors can see class-wide weak areas.
- **Exam Readiness Score:** Automated score predictor based on practice test consistency.
- **Summary:** OmniTutor saves student study time, eliminates AI hallucinations, and makes exam preparation personalized.

> **🗣️ Speaker Notes:**  
> *"Our future roadmap includes voice interaction and college LMS integration. Thank you for your time, and Team CODEFORGE is ready for your questions!"*
