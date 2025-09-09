# 🤖 SkillScout – AI HR Hiring Agent  

SkillScout is an Agentic AI application that helps HR professionals plan their startup hiring process. 
It leverages **LangGraph** for multi-step reasoning and state management, combined with **Streamlit** for an interactive frontend.   
The app asks clarifying questions, generates professional job descriptions, and creates structured hiring checklists with export options in Markdown or JSON.

---

## ✨ Features  

- **Clarifying Questions**: Automatically asks HR-specific questions (budget, timeline, skills, role type, location).  
- **Professional Job Descriptions**: Generates recruiter-ready JDs in paragraph format instead of bullet points.  
- **Hiring Plan & Checklist**: Creates a structured hiring roadmap, from defining roles to onboarding.  
- **Session Memory**: Saves past sessions locally so you can revisit or continue planning.  
- **Multi-Step Reasoning**: Uses LangGraph nodes (`intake → clarifier → JD generator → plan builder → presenter`).  
- **Tool Integration**:  
  - 📧 Email Writer (draft kickoff emails)  
  - 📋 Checklist Builder (role-based hiring tasks)  
  - 🔍 Search Stub (placeholder for future job board integrations)  
- **Frontend with Streamlit**: Modern, responsive UI with tabs for questions, JDs, and checklists.  
- **Export Options**: Download results as **Markdown or JSON** for sharing or documentation.  

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

**🔮 Future Improvements**

🔗 Integrate real job board APIs for live market research

📧 Send kickoff emails directly (SMTP or HRIS integration)

📊 Analytics dashboard (usage trends, roles tracked)

🔒 Add user authentication for HR teams

Stay Tuned for Updates !
