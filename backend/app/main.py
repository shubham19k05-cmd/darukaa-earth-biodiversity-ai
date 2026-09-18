from fastapi import FastAPI,Depends,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base,engine,get_db
from .models import User,Conversation,Message,EnvironmentalObservation
from .schemas import RegisterIn,LoginIn,TokenOut,ChatIn,ChatOut,AnalyzeIn
from .auth import hash_password,verify_password,create_token,current_user
from .reasoning import analyze

app=FastAPI(title="Darukaa.Earth Biodiversity Intelligence API",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["*"],allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

@app.on_event("startup")
def startup(): Base.metadata.create_all(bind=engine)

@app.get("/")
def root(): return {"name":"Darukaa.Earth Biodiversity Intelligence API","status":"ok"}
@app.get("/health")
def health(): return {"status":"healthy"}

@app.post("/auth/register",response_model=TokenOut)
def register(p:RegisterIn,db:Session=Depends(get_db)):
    if db.query(User).filter(User.email==p.email).first(): raise HTTPException(409,"Email already registered")
    u=User(full_name=p.full_name,email=p.email,password_hash=hash_password(p.password));db.add(u);db.commit();db.refresh(u)
    return {"access_token":create_token(u.id),"token_type":"bearer"}

@app.post("/auth/login",response_model=TokenOut)
def login(p:LoginIn,db:Session=Depends(get_db)):
    u=db.query(User).filter(User.email==p.email).first()
    if not u or not verify_password(p.password,u.password_hash): raise HTTPException(401,"Invalid email or password")
    return {"access_token":create_token(u.id),"token_type":"bearer"}

@app.post("/analyze")
def analyze_json(p:AnalyzeIn,user=Depends(current_user)):
    n,q,r,k=analyze(p.environment,"environmental biodiversity analysis")
    return {"needs_clarification":n,"clarification_question":q,"recommendations":r,"retrieved_knowledge":k}

@app.post("/chat",response_model=ChatOut)
def chat(p:ChatIn,db:Session=Depends(get_db),user=Depends(current_user)):
    if p.conversation_id:
        c=db.get(Conversation,p.conversation_id)
        if not c or c.user_id!=user.id: raise HTTPException(404,"Conversation not found")
    else:
        c=Conversation(user_id=user.id,title=p.message[:80]);db.add(c);db.commit();db.refresh(c)
    db.add(Message(conversation_id=c.id,role="user",content=p.message))
    for k,v in p.environment.items(): db.add(EnvironmentalObservation(conversation_id=c.id,metric_name=k,metric_value=str(v)))
    n,q,r,k=analyze(p.environment,p.message)
    response=q if n else "The analysis combines soil condition, climate/water stress and land-use or habitat structure. Review the recommendation cards for the ecological mechanism, impacted metrics, time horizon and scientific evidence."
    db.add(Message(conversation_id=c.id,role="assistant",content=response));db.commit()
    return {"conversation_id":c.id,"needs_clarification":n,"clarification_question":q,"response":response,"recommendations":r,"retrieved_knowledge":k}
