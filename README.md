# 🤖 SkillScout – AI HR Hiring Agent  

SkillScout is an Agentic AI application that helps HR professionals plan their startup hiring process. 
It leverages **LangGraph** for multi-step reasoning and state management, combined with **Streamlit** for an interactive frontend.   
The app asks clarifying questions, generates professional job descriptions, and creates structured hiring checklists with export options in Markdown or JSON.

---

## ✨ Features  

- Clarifying Questions – Automatically asks HR-specific questions (budget, timeline, skills, job type, location).

- Job Description Drafts – Generates professional, sentence-based JD drafts tailored to input & clarifications.

- Hiring Plan & Checklist – Creates an actionable hiring roadmap, from role definition to execution.

- Session Memory – Saves past sessions locally so you can resume where you left off.

- Professional Output – Presents results in polished Markdown or downloadable JSON.

Integrated Tools

 - 📧 Email Writer: Draft kickoff or follow-up emails

 - ✅ Checklist Builder: Generate role-specific hiring tasks

 - 🔎 Search Tool (stub): Placeholder for job board/market research integration
---

## 🏗️ Project Structure  

```bash
SkillScout/
│── app.py                 # Streamlit frontend (clarifier + tabs)
│── graph.py               # LangGraph workflow builder
│── state.py               # Shared AgentState (slots, artifacts, analytics)
│── memory.py              # Session-based memory (JSON storage)
│── requirements.txt       # Dependencies
│
├── nodes/                 # Reasoning nodes
│   ├── intake.py
│   ├── clarifier.py
│   ├── jd_generator.py
│   ├── plan_builder.py
│   ├── email_writer.py
│   └── presenter.py
│
├── tools/                 # Helper tools / integrations
│   ├── checklist_tool.py  # Adaptive hiring plan builder
│   ├── email_tool.py      # Kickoff email generator
│   ├── search_tool.py     # (stub for job board / search APIs)
│   └── ollama_llm.py      # (optional LLM integration)
│
├── data/
│   └── roles.yml          # Seed role templates
│
├── storage/
│   └── sessions/          # Saved session states (JSON)
│
├── prompts/
│   ├── clarifier.md
│   ├── jd.md
│   ├── email.md
│   └── plan.md
│
└── tests/                 # Unit tests
    ├── test_graph.py
    ├── test_slots.py
    └── test_unknown_role.py

```

---

**🧠 Tech Stack**

🐍 Python 3.9+ → Core programming language

🔗 LangGraph → Multi-step reasoning graphs & agent state management

🦜 LangChain (core) → Utilities for LLM tool integration (future-ready)

📊 Streamlit → Interactive web frontend for HR workflow

✅ Pydantic → Data validation & structured state handling (AgentState)

📄 PyYAML → Parse role templates (roles.yml)

📦 JSON → Structured exports & session persistence

⚙️ Git + GitHub → Version control & collaboration

---
## ⚡ Getting Started
```
1. Clone the repo
   git clone https://github.com/Slakkimsetty/SkillScout.git
   cd SkillScout

2. Create a virtual environment
  python -m venv .venv
  source .venv/Scripts/activate   # (Windows PowerShell)
  # OR
  source .venv/bin/activate       # (Mac/Linux)

3. pip install -r requirements.txt #installiing dependencies
 
4. streamlit run app.py  # running the app
```
---
**🔮 Future Improvements**

🔗 Integrate real job board APIs for live market research

📧 Send kickoff emails directly (SMTP or HRIS integration)

📊 Analytics dashboard (usage trends, roles tracked)

🔒 Add user authentication for HR teams


---
Stay Tuned for Updates !
---

