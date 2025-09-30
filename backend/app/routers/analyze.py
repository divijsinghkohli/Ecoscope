from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.database import get_db, Company, Article, ESGEvent, RiskScore
from app.models import CompanyAnalysisResponse, ESGEventResponse, ArticleResponse, RiskScoreResponse
from app.services.news_service import NewsService
from app.services.simple_nlp import SimpleNLPService

router = APIRouter()
news_service = NewsService()
nlp_service = SimpleNLPService()

@router.get("/analyze", response_model=CompanyAnalysisResponse)
async def analyze_company(
    company: str = Query(..., description="Company name to analyze"),
    db: Session = Depends(get_db)
):
    """
    Analyze ESG risk for a company by scraping news and running NLP analysis
    """
    try:
        # Get or create company in database
        db_company = db.query(Company).filter(Company.name.ilike(f"%{company}%")).first()
        if not db_company:
            db_company = Company(name=company)
            db.add(db_company)
            db.commit()
            db.refresh(db_company)
        
        # Get news articles
        news_articles = news_service.get_company_news(company, limit=10)
        
        # Process each article
        all_events = []
        processed_articles = []
        
        for article_data in news_articles:
            # Analyze sentiment
            sentiment_score = nlp_service.analyze_sentiment(article_data['content'])
            
            # Detect ESG events
            events = nlp_service.detect_esg_events(article_data['content'])
            
            # Store article in database
            db_article = Article(
                title=article_data['title'],
                content=article_data['content'],
                url=article_data['url'],
                published_at=article_data['published_at'],
                sentiment_score=sentiment_score,
                company_id=db_company.id
            )
            db.add(db_article)
            db.commit()
            db.refresh(db_article)
            
            # Store ESG events
            for event in events:
                db_event = ESGEvent(
                    event_type=event.event_type,
                    description=event.description,
                    severity=event.severity,
                    article_id=db_article.id
                )
                db.add(db_event)
                all_events.append(event)
            
            # Create article response
            article_response = ArticleResponse(
                title=article_data['title'],
                content=article_data['content'],
                url=article_data['url'],
                published_at=article_data['published_at'],
                sentiment_score=sentiment_score,
                events=events
            )
            processed_articles.append(article_response)
        
        # Calculate risk scores
        risk_scores = nlp_service.calculate_risk_scores(news_articles, all_events)
        
        # Store risk score in database
        db_risk_score = RiskScore(
            company_id=db_company.id,
            overall_score=risk_scores['overall_score'],
            environmental_score=risk_scores['environmental_score'],
            social_score=risk_scores['social_score'],
            governance_score=risk_scores['governance_score']
        )
        db.add(db_risk_score)
        db.commit()
        
        # Create response
        response = CompanyAnalysisResponse(
            company=company,
            score=risk_scores['overall_score'],
            risk_breakdown=RiskScoreResponse(
                overall_score=risk_scores['overall_score'],
                environmental_score=risk_scores['environmental_score'],
                social_score=risk_scores['social_score'],
                governance_score=risk_scores['governance_score']
            ),
            events=all_events,
            articles=processed_articles,
            total_articles=len(processed_articles),
            analyzed_at=datetime.utcnow()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/companies", response_model=List[dict])
async def get_companies(db: Session = Depends(get_db)):
    """
    Get all analyzed companies with their latest risk scores
    """
    try:
        companies = db.query(Company).all()
        result = []
        
        for company in companies:
            # Get latest risk score
            latest_risk_score = db.query(RiskScore).filter(
                RiskScore.company_id == company.id
            ).order_by(RiskScore.calculated_at.desc()).first()
            
            if latest_risk_score:
                result.append({
                    'id': company.id,
                    'name': company.name,
                    'overall_score': latest_risk_score.overall_score,
                    'environmental_score': latest_risk_score.environmental_score,
                    'social_score': latest_risk_score.social_score,
                    'governance_score': latest_risk_score.governance_score,
                    'last_analyzed': latest_risk_score.calculated_at,
                    'total_articles': len(company.articles)
                })
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch companies: {str(e)}")

@router.get("/companies/{company_id}/details", response_model=CompanyAnalysisResponse)
async def get_company_details(company_id: int, db: Session = Depends(get_db)):
    """
    Get detailed analysis for a specific company
    """
    try:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        # Get latest risk score
        latest_risk_score = db.query(RiskScore).filter(
            RiskScore.company_id == company.id
        ).order_by(RiskScore.calculated_at.desc()).first()
        
        if not latest_risk_score:
            raise HTTPException(status_code=404, detail="No analysis found for this company")
        
        # Get articles and events
        articles = db.query(Article).filter(Article.company_id == company.id).all()
        processed_articles = []
        all_events = []
        
        for article in articles:
            events = db.query(ESGEvent).filter(ESGEvent.article_id == article.id).all()
            event_responses = [
                ESGEventResponse(
                    event_type=event.event_type,
                    description=event.description,
                    severity=event.severity
                ) for event in events
            ]
            
            article_response = ArticleResponse(
                title=article.title,
                content=article.content,
                url=article.url,
                published_at=article.published_at,
                sentiment_score=article.sentiment_score,
                events=event_responses
            )
            processed_articles.append(article_response)
            all_events.extend(event_responses)
        
        response = CompanyAnalysisResponse(
            company=company.name,
            score=latest_risk_score.overall_score,
            risk_breakdown=RiskScoreResponse(
                overall_score=latest_risk_score.overall_score,
                environmental_score=latest_risk_score.environmental_score,
                social_score=latest_risk_score.social_score,
                governance_score=latest_risk_score.governance_score
            ),
            events=all_events,
            articles=processed_articles,
            total_articles=len(processed_articles),
            analyzed_at=latest_risk_score.calculated_at
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch company details: {str(e)}")
