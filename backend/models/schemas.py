from pydantic import BaseModel
from typing import List, Optional, Dict

class ChildInfo(BaseModel):
    age: Optional[int]
    grades: List[str]
    hobbies: List[str]
    traits: List[str]
    strengths: List[str]

class HomeworkItem(BaseModel):
    subject: str
    content: str
    expectedTime: str

class FamilyMember(BaseModel):
    role: str
    subjectPreference: List[str]
    educationConcept: str

class SettingsPayload(BaseModel):
    child: ChildInfo
    homework: Dict[str, List[HomeworkItem]] 
    members: List[FamilyMember]

class ChatInput(BaseModel):
    message: str