#!/usr/bin/env python3
"""
Seed script to populate the database with sample ESG analysis data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from app.database import SessionLocal, Company, Article, ESGEvent, RiskScore
from app.services.simple_nlp import SimpleNLPService

def seed_database():
    """Seed the database with sample data"""
    db = SessionLocal()
    nlp_service = SimpleNLPService()
    
    try:
        # Sample companies and their data
        companies_data = [
            {
                'name': 'Tesla',
                'articles': [
                    {
                        'title': 'Tesla Faces New Labor Disputes at German Gigafactory',
                        'content': 'Tesla is facing renewed labor disputes at its German Gigafactory as workers demand better working conditions and higher wages. The company has been criticized for its approach to labor relations and workplace safety standards. Union representatives have raised concerns about excessive overtime and inadequate safety protocols.',
                        'url': 'https://example.com/tesla-labor-disputes',
                        'published_at': datetime.now() - timedelta(days=2)
                    },
                    {
                        'title': 'Tesla Reports Record Carbon Emissions Despite EV Focus',
                        'content': 'Despite being an electric vehicle manufacturer, Tesla has reported record carbon emissions from its manufacturing processes. Environmental groups are calling for greater transparency in the company\'s environmental impact reporting. The emissions are primarily from battery production and manufacturing facilities.',
                        'url': 'https://example.com/tesla-emissions',
                        'published_at': datetime.now() - timedelta(days=5)
                    },
                    {
                        'title': 'Tesla Autopilot Under Regulatory Scrutiny After Accidents',
                        'content': 'Tesla\'s Autopilot system is facing increased regulatory scrutiny following several accidents. The National Highway Traffic Safety Administration is investigating potential safety violations. Critics argue that the system may be overpromising its capabilities.',
                        'url': 'https://example.com/tesla-autopilot',
                        'published_at': datetime.now() - timedelta(days=7)
                    }
                ]
            },
            {
                'name': 'ExxonMobil',
                'articles': [
                    {
                        'title': 'ExxonMobil Fined $2.5M for Environmental Violations',
                        'content': 'ExxonMobil has been fined $2.5 million for environmental violations at its Texas refinery. The company failed to properly report emissions and violated multiple environmental regulations. This is the latest in a series of environmental compliance issues for the oil giant.',
                        'url': 'https://example.com/exxon-fine',
                        'published_at': datetime.now() - timedelta(days=1)
                    },
                    {
                        'title': 'ExxonMobil Oil Spill Cleanup Costs Reach $50M',
                        'content': 'Cleanup costs for a recent oil spill at an ExxonMobil facility have reached $50 million. The spill has caused significant environmental damage and affected local communities. Wildlife rescue efforts are ongoing as the environmental impact continues to be assessed.',
                        'url': 'https://example.com/exxon-spill',
                        'published_at': datetime.now() - timedelta(days=3)
                    },
                    {
                        'title': 'ExxonMobil Workers Strike Over Safety Concerns',
                        'content': 'Workers at ExxonMobil facilities are striking over safety concerns and inadequate protective equipment. The union claims the company has ignored multiple safety violations. The strike has affected production at several key facilities.',
                        'url': 'https://example.com/exxon-strike',
                        'published_at': datetime.now() - timedelta(days=6)
                    }
                ]
            },
            {
                'name': 'Google',
                'articles': [
                    {
                        'title': 'Google Faces Antitrust Lawsuit Over Search Dominance',
                        'content': 'Google is facing a major antitrust lawsuit over its dominance in search and advertising markets. The lawsuit alleges anti-competitive practices and market manipulation. This could have significant implications for the tech industry.',
                        'url': 'https://example.com/google-antitrust',
                        'published_at': datetime.now() - timedelta(days=2)
                    },
                    {
                        'title': 'Google Data Center Emissions Under Scrutiny',
                        'content': 'Google\'s data centers are under scrutiny for their massive energy consumption and carbon emissions. Despite renewable energy commitments, the company\'s carbon footprint continues to grow. The scale of AI training is driving unprecedented energy demands.',
                        'url': 'https://example.com/google-emissions',
                        'published_at': datetime.now() - timedelta(days=4)
                    },
                    {
                        'title': 'Google Employees Protest Military Contracts',
                        'content': 'Google employees are protesting the company\'s military contracts, citing ethical concerns about AI technology being used in warfare. The protests highlight ongoing governance issues and employee activism within the company.',
                        'url': 'https://example.com/google-protests',
                        'published_at': datetime.now() - timedelta(days=8)
                    }
                ]
            },
            {
                'name': 'Amazon',
                'articles': [
                    {
                        'title': 'Amazon Warehouse Workers File Safety Complaints',
                        'content': 'Amazon warehouse workers have filed numerous safety complaints about working conditions, including inadequate breaks and unsafe equipment. The company faces multiple workplace safety violations. Worker advocacy groups are calling for better protections.',
                        'url': 'https://example.com/amazon-safety',
                        'published_at': datetime.now() - timedelta(days=1)
                    },
                    {
                        'title': 'Amazon Fined for Environmental Waste Management Violations',
                        'content': 'Amazon has been fined for improper waste management and environmental violations at its fulfillment centers. The company failed to properly dispose of hazardous materials. Environmental groups are demanding stricter oversight.',
                        'url': 'https://example.com/amazon-waste',
                        'published_at': datetime.now() - timedelta(days=5)
                    },
                    {
                        'title': 'Amazon Unionization Efforts Gain Momentum',
                        'content': 'Unionization efforts at Amazon facilities are gaining momentum as workers demand better wages and working conditions. The company has been criticized for its anti-union practices. This represents a significant challenge to Amazon\'s labor model.',
                        'url': 'https://example.com/amazon-union',
                        'published_at': datetime.now() - timedelta(days=9)
                    }
                ]
            },
            {
                'name': 'Microsoft',
                'articles': [
                    {
                        'title': 'Microsoft Announces Major Carbon Negative Initiative',
                        'content': 'Microsoft has announced a major initiative to become carbon negative by 2030. The company is investing heavily in renewable energy and carbon capture technologies. This represents a significant commitment to environmental sustainability.',
                        'url': 'https://example.com/microsoft-carbon',
                        'published_at': datetime.now() - timedelta(days=3)
                    },
                    {
                        'title': 'Microsoft Faces Data Privacy Concerns in Europe',
                        'content': 'Microsoft is facing data privacy concerns in Europe over its cloud services. Regulators are investigating potential violations of GDPR regulations. The company has pledged to improve its data handling practices.',
                        'url': 'https://example.com/microsoft-privacy',
                        'published_at': datetime.now() - timedelta(days=6)
                    },
                    {
                        'title': 'Microsoft Commits to Responsible AI Development',
                        'content': 'Microsoft has committed to responsible AI development practices, including ethical guidelines and transparency measures. The company is working with industry partners to establish AI safety standards. This represents a positive step in AI governance.',
                        'url': 'https://example.com/microsoft-ai',
                        'published_at': datetime.now() - timedelta(days=10)
                    }
                ]
            }
        ]
        
        for company_data in companies_data:
            # Create or get company
            company = db.query(Company).filter(Company.name == company_data['name']).first()
            if not company:
                company = Company(name=company_data['name'])
                db.add(company)
                db.commit()
                db.refresh(company)
            
            # Process articles
            all_events = []
            for article_data in company_data['articles']:
                # Analyze sentiment
                sentiment_score = nlp_service.analyze_sentiment(article_data['content'])
                
                # Detect ESG events
                events = nlp_service.detect_esg_events(article_data['content'])
                
                # Create article
                article = Article(
                    title=article_data['title'],
                    content=article_data['content'],
                    url=article_data['url'],
                    published_at=article_data['published_at'],
                    sentiment_score=sentiment_score,
                    company_id=company.id
                )
                db.add(article)
                db.commit()
                db.refresh(article)
                
                # Create ESG events
                for event in events:
                    db_event = ESGEvent(
                        event_type=event.event_type,
                        description=event.description,
                        severity=event.severity,
                        article_id=article.id
                    )
                    db.add(db_event)
                    all_events.append(event)
            
            # Calculate risk scores
            articles_for_scoring = [
                {
                    'sentiment_score': article.sentiment_score,
                    'content': article.content
                } for article in company.articles
            ]
            risk_scores = nlp_service.calculate_risk_scores(articles_for_scoring, all_events)
            
            # Create risk score record
            risk_score = RiskScore(
                company_id=company.id,
                overall_score=risk_scores['overall_score'],
                environmental_score=risk_scores['environmental_score'],
                social_score=risk_scores['social_score'],
                governance_score=risk_scores['governance_score']
            )
            db.add(risk_score)
        
        db.commit()
        print("✅ Database seeded successfully with sample ESG data!")
        print(f"📊 Added {len(companies_data)} companies with articles and risk scores")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
