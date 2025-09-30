from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ESGEventResponse(BaseModel):
    event_type: str
    description: str
    severity: float

class ArticleResponse(BaseModel):
    title: str
    content: str
    url: str
    published_at: datetime
    sentiment_score: float
    events: List[ESGEventResponse] = []

class RiskScoreResponse(BaseModel):
    overall_score: float
    environmental_score: float
    social_score: float
    governance_score: float

class CompanyAnalysisResponse(BaseModel):
    company: str
    score: float
    risk_breakdown: RiskScoreResponse
    events: List[ESGEventResponse]
    articles: List[ArticleResponse]
    total_articles: int
    analyzed_at: datetime

class CompanyRequest(BaseModel):
    company_name: str
