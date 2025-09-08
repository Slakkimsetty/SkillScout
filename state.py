from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class RoleSpec(BaseModel):
    title: str
    seniority: Optional[str] = None
    must_have: List[str] = Field(default_factory=list)
    nice_to_have: List[str] = Field(default_factory=list)

class Slots(BaseModel):
    roles: List[RoleSpec] = Field(default_factory=list)
    budget: Optional[str] = None
    timeline: Optional[str] = None
    location: Optional[str] = None       # remote | hybrid | onsite
    hiring_type: Optional[str] = None    # full-time | intern | contract

class Artifacts(BaseModel):
    result_markdown: Optional[str] = None
    jds: Dict[str, str] = Field(default_factory=dict)
    plan_markdown: Optional[str] = None
    plan_json: List[Dict[str, str]] = Field(default_factory=list)
    email_draft: Optional[str] = None

class AgentState(BaseModel):
    session_id: str
    user_query: str = ""
    slots: Slots = Field(default_factory=Slots)
    artifacts: Artifacts = Field(default_factory=Artifacts)
    pending_questions: List[str] = Field(default_factory=list)
    awaiting_answers: bool = False

    def missing_fields(self) -> List[str]:
        missing = []
        if not self.slots.roles: missing.append("roles")
        if not self.slots.budget: missing.append("budget")
        if not self.slots.timeline: missing.append("timeline")
        if not self.slots.location: missing.append("location")
        if not self.slots.hiring_type: missing.append("hiring_type")
        return missing
