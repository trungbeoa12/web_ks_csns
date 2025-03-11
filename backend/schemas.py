from pydantic import BaseModel
from typing import Optional

# Schema cho User
class UserCreate(BaseModel):
    username: str
    password: str
    role: str
    branch_id: Optional[int]

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    branch_id: Optional[int]

    class Config:
        orm_mode = True

# Schema cho Branch
class BranchCreate(BaseModel):
    branch_name: str

class BranchResponse(BaseModel):
    id: int
    branch_name: str

    class Config:
        orm_mode = True

# Schema cho Question
class QuestionCreate(BaseModel):
    content: str

class QuestionResponse(BaseModel):
    id: int
    content: str

    class Config:
        orm_mode = True

# Schema cho SurveyResponse
class SurveyResponseCreate(BaseModel):
    branch_id: int
    question_id: int
    selected: str
    suggestion: Optional[str]

class SurveyResponseView(BaseModel):
    id: int
    branch_id: int
    question_id: int
    selected: str
    suggestion: Optional[str]

    class Config:
        orm_mode = True

