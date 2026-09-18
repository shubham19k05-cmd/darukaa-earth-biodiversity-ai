from datetime import datetime
from sqlalchemy import Column,Integer,String,Text,DateTime,ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True)
    full_name=Column(String(120),nullable=False)
    email=Column(String(255),unique=True,index=True,nullable=False)
    password_hash=Column(String(255),nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)
    conversations=relationship("Conversation",back_populates="user")

class Conversation(Base):
    __tablename__="conversations"
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)
    title=Column(String(200),default="Biodiversity analysis")
    created_at=Column(DateTime,default=datetime.utcnow)
    updated_at=Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    user=relationship("User",back_populates="conversations")
    messages=relationship("Message",back_populates="conversation",cascade="all, delete-orphan")
    observations=relationship("EnvironmentalObservation",back_populates="conversation",cascade="all, delete-orphan")

class Message(Base):
    __tablename__="messages"
    id=Column(Integer,primary_key=True)
    conversation_id=Column(Integer,ForeignKey("conversations.id"),nullable=False)
    role=Column(String(30),nullable=False)
    content=Column(Text,nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)
    conversation=relationship("Conversation",back_populates="messages")

class EnvironmentalObservation(Base):
    __tablename__="environmental_observations"
    id=Column(Integer,primary_key=True)
    conversation_id=Column(Integer,ForeignKey("conversations.id"),nullable=False)
    metric_name=Column(String(100),nullable=False)
    metric_value=Column(String(255),nullable=False)
    unit=Column(String(50),default="")
    created_at=Column(DateTime,default=datetime.utcnow)
    conversation=relationship("Conversation",back_populates="observations")
