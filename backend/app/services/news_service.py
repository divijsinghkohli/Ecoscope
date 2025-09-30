import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime, timedelta
import random
import json

class NewsService:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Mock news data for demonstration
        self.mock_news_data = {
            'tesla': [
                {
                    'title': 'Tesla Faces New Labor Disputes at German Gigafactory',
                    'content': 'Tesla is facing renewed labor disputes at its German Gigafactory as workers demand better working conditions and higher wages. The company has been criticized for its approach to labor relations and workplace safety standards.',
                    'url': 'https://example.com/tesla-labor-disputes',
                    'published_at': datetime.now() - timedelta(days=2)
                },
                {
                    'title': 'Tesla Reports Record Carbon Emissions Despite EV Focus',
                    'content': 'Despite being an electric vehicle manufacturer, Tesla has reported record carbon emissions from its manufacturing processes. Environmental groups are calling for greater transparency in the company\'s environmental impact reporting.',
                    'url': 'https://example.com/tesla-emissions',
                    'published_at': datetime.now() - timedelta(days=5)
                },
                {
                    'title': 'Tesla Autopilot Under Regulatory Scrutiny After Accidents',
                    'content': 'Tesla\'s Autopilot system is facing increased regulatory scrutiny following several accidents. The National Highway Traffic Safety Administration is investigating potential safety violations.',
                    'url': 'https://example.com/tesla-autopilot',
                    'published_at': datetime.now() - timedelta(days=7)
                }
            ],
            'exxon': [
                {
                    'title': 'ExxonMobil Fined $2.5M for Environmental Violations',
                    'content': 'ExxonMobil has been fined $2.5 million for environmental violations at its Texas refinery. The company failed to properly report emissions and violated multiple environmental regulations.',
                    'url': 'https://example.com/exxon-fine',
                    'published_at': datetime.now() - timedelta(days=1)
                },
                {
                    'title': 'ExxonMobil Oil Spill Cleanup Costs Reach $50M',
                    'content': 'Cleanup costs for a recent oil spill at an ExxonMobil facility have reached $50 million. The spill has caused significant environmental damage and affected local communities.',
                    'url': 'https://example.com/exxon-spill',
                    'published_at': datetime.now() - timedelta(days=3)
                },
                {
                    'title': 'ExxonMobil Workers Strike Over Safety Concerns',
                    'content': 'Workers at ExxonMobil facilities are striking over safety concerns and inadequate protective equipment. The union claims the company has ignored multiple safety violations.',
                    'url': 'https://example.com/exxon-strike',
                    'published_at': datetime.now() - timedelta(days=6)
                }
            ],
            'google': [
                {
                    'title': 'Google Faces Antitrust Lawsuit Over Search Dominance',
                    'content': 'Google is facing a major antitrust lawsuit over its dominance in search and advertising markets. The lawsuit alleges anti-competitive practices and market manipulation.',
                    'url': 'https://example.com/google-antitrust',
                    'published_at': datetime.now() - timedelta(days=2)
                },
                {
                    'title': 'Google Data Center Emissions Under Scrutiny',
                    'content': 'Google\'s data centers are under scrutiny for their massive energy consumption and carbon emissions. Despite renewable energy commitments, the company\'s carbon footprint continues to grow.',
                    'url': 'https://example.com/google-emissions',
                    'published_at': datetime.now() - timedelta(days=4)
                },
                {
                    'title': 'Google Employees Protest Military Contracts',
                    'content': 'Google employees are protesting the company\'s military contracts, citing ethical concerns about AI technology being used in warfare. The protests highlight ongoing governance issues.',
                    'url': 'https://example.com/google-protests',
                    'published_at': datetime.now() - timedelta(days=8)
                }
            ],
            'amazon': [
                {
                    'title': 'Amazon Warehouse Workers File Safety Complaints',
                    'content': 'Amazon warehouse workers have filed numerous safety complaints about working conditions, including inadequate breaks and unsafe equipment. The company faces multiple workplace safety violations.',
                    'url': 'https://example.com/amazon-safety',
                    'published_at': datetime.now() - timedelta(days=1)
                },
                {
                    'title': 'Amazon Fined for Environmental Waste Management Violations',
                    'content': 'Amazon has been fined for improper waste management and environmental violations at its fulfillment centers. The company failed to properly dispose of hazardous materials.',
                    'url': 'https://example.com/amazon-waste',
                    'published_at': datetime.now() - timedelta(days=5)
                },
                {
                    'title': 'Amazon Unionization Efforts Gain Momentum',
                    'content': 'Unionization efforts at Amazon facilities are gaining momentum as workers demand better wages and working conditions. The company has been criticized for its anti-union practices.',
                    'url': 'https://example.com/amazon-union',
                    'published_at': datetime.now() - timedelta(days=9)
                }
            ]
        }

    def get_company_news(self, company_name: str, limit: int = 10) -> List[Dict]:
        """Get news articles for a company (mock implementation)"""
        company_key = company_name.lower().replace(' ', '').replace('inc', '').replace('corp', '')
        
        # Check if we have mock data for this company
        if company_key in self.mock_news_data:
            return self.mock_news_data[company_key][:limit]
        
        # Generate generic mock data for unknown companies
        return self._generate_mock_news(company_name, limit)

    def _generate_mock_news(self, company_name: str, limit: int) -> List[Dict]:
        """Generate mock news data for companies not in our dataset"""
        mock_templates = [
            {
                'title': f'{company_name} Reports Strong Q4 Earnings',
                'content': f'{company_name} has reported strong fourth-quarter earnings, beating analyst expectations. The company\'s performance has been driven by increased demand and operational efficiency improvements.',
                'url': f'https://example.com/{company_name.lower()}-earnings',
                'published_at': datetime.now() - timedelta(days=random.randint(1, 7))
            },
            {
                'title': f'{company_name} Announces New Sustainability Initiative',
                'content': f'{company_name} has announced a new sustainability initiative aimed at reducing its environmental impact. The company plans to invest in renewable energy and improve its carbon footprint.',
                'url': f'https://example.com/{company_name.lower()}-sustainability',
                'published_at': datetime.now() - timedelta(days=random.randint(1, 7))
            },
            {
                'title': f'{company_name} Faces Regulatory Scrutiny',
                'content': f'{company_name} is facing increased regulatory scrutiny over its business practices. Regulators are investigating potential compliance issues and market conduct violations.',
                'url': f'https://example.com/{company_name.lower()}-regulatory',
                'published_at': datetime.now() - timedelta(days=random.randint(1, 7))
            }
        ]
        
        return random.sample(mock_templates, min(limit, len(mock_templates)))

    def scrape_news(self, company_name: str, limit: int = 10) -> List[Dict]:
        """Scrape real news articles (placeholder for future implementation)"""
        # This would implement actual news scraping in a production environment
        # For now, we'll use mock data
        return self.get_company_news(company_name, limit)
