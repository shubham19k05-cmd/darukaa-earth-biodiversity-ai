from typing import Any,Dict,List,Optional
from pydantic import BaseModel,EmailStr,Field

class RegisterIn(BaseModel):
    full_name:str
    email:EmailStr
    password:str=Field(min_length=8)
class LoginIn(BaseModel):
    email:EmailStr
    password:str
class TokenOut(BaseModel):
    access_token:str
    token_type:str="bearer"
class ChatIn(BaseModel):
    conversation_id:Optional[int]=None
    message:str
    environment:Dict[str,Any]={}
class AnalyzeIn(BaseModel):
    environment:Dict[str,Any]
class Evidence(BaseModel):
    organization:str
    title:str
    url:str
class Recommendation(BaseModel):
    action:str
    why_it_works:str
    impacted_metrics:List[str]
    time_horizon:str
    confidence:str
    evidence:List[Evidence]
class ChatOut(BaseModel):
    conversation_id:int
    needs_clarification:bool
    clarification_question:Optional[str]=None
    response:str
    recommendations:List[Recommendation]
    retrieved_knowledge:List[Dict[str,Any]]
