# state.py
from __future__ import annotations
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class RoleSpec(BaseModel):
    title: str
    must_have: List[str] = []
    nice_to_have: List[str] = []

class Slots(BaseModel):
    roles: List[RoleSpec] = []
    budget: Optional[str] = None
    timeline: Optional[str] = None
    location: Optional[str] = None
    hiring_type: Optional[str] = None
    skills_hint: List[str] = []
    company_name: Optional[str] = None  # <-- NEW

class Artifacts(BaseModel):
    jds: Dict[str, str] = Field(default_factory=dict)
    plan_json: List[Dict] = Field(default_factory=list)
    plan_markdown: str = ""
    email_draft: Optional[str] = None
    summary_md: str = ""

class AgentState(BaseModel):
    session_id: str
    user_query: str
    slots: Slots = Field(default_factory=Slots)
    artifacts: Artifacts = Field(default_factory=Artifacts)
    analytics: Dict[str, int] = Field(default_factory=lambda: {"roles_created": 0, "checklist_items": 0, "sessions": 1})
