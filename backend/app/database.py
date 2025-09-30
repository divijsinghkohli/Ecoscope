from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./esg_analyzer.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    articles = relationship("Article", back_populates="company")
    risk_scores = relationship("RiskScore", back_populates="company")

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    url = Column(String)
    published_at = Column(DateTime)
    sentiment_score = Column(Float)
    company_id = Column(Integer, ForeignKey("companies.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="articles")
    events = relationship("ESGEvent", back_populates="article")

class ESGEvent(Base):
    __tablename__ = "esg_events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String)  # e.g., "labor_strike", "oil_spill", "regulatory_fine"
    description = Column(Text)
    severity = Column(Float)  # 0.0 to 1.0
    article_id = Column(Integer, ForeignKey("articles.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    article = relationship("Article", back_populates="events")

class RiskScore(Base):
    __tablename__ = "risk_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    overall_score = Column(Float)  # 0.0 to 1.0
    environmental_score = Column(Float)
    social_score = Column(Float)
    governance_score = Column(Float)
    calculated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    company = relationship("Company", back_populates="risk_scores")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
