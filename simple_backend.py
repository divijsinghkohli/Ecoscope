#!/usr/bin/env python3
"""
Simple ESG Risk Analyzer Backend - No complex dependencies
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime
from companies_data import COMPANIES_DATA

# Mock data - this will be updated when new companies are analyzed
MOCK_COMPANIES = COMPANIES_DATA.copy()

MOCK_ANALYSIS = {
    "tesla": {
        "company": "Tesla",
        "score": 0.73,
        "risk_breakdown": {
            "overall_score": 0.73,
            "environmental_score": 0.65,
            "social_score": 0.80,
            "governance_score": 0.75
        },
        "events": [
            {
                "event_type": "social_labor_strike",
                "description": "Tesla is facing renewed labor disputes at its German Gigafactory as workers demand better working conditions and higher wages.",
                "severity": 0.8
            },
            {
                "event_type": "environmental_emissions",
                "description": "Tesla has reported record carbon emissions from its manufacturing processes despite being an electric vehicle manufacturer.",
                "severity": 0.7
            }
        ],
        "articles": [
            {
                "title": "Tesla Faces New Labor Disputes at German Gigafactory",
                "content": "Tesla is facing renewed labor disputes at its German Gigafactory as workers demand better working conditions and higher wages.",
                "url": "https://example.com/tesla-labor-disputes",
                "published_at": "2024-01-13T10:00:00Z",
                "sentiment_score": -0.3,
                "events": []
            }
        ],
        "total_articles": 3,
        "analyzed_at": "2024-01-15T10:30:00Z"
    }
}

class ESGRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Handle CORS
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        if self.path == '/':
            response = {"message": "ESG Risk Analyzer API is running"}
        elif self.path == '/health':
            response = {"status": "healthy"}
        elif self.path == '/api/companies':
            response = MOCK_COMPANIES
        elif self.path.startswith('/api/analyze'):
            # Parse query parameters
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            company = query_params.get('company', [''])[0].lower()
            
            if company in MOCK_ANALYSIS:
                response = MOCK_ANALYSIS[company]
            else:
                # Generate mock analysis for new company
                company_title = company.title()
                new_company_data = {
                    "id": len(MOCK_COMPANIES) + 1,
                    "name": company_title,
                    "overall_score": 0.55,
                    "environmental_score": 0.50,
                    "social_score": 0.60,
                    "governance_score": 0.55,
                    "last_analyzed": datetime.now().isoformat() + "Z",
                    "total_articles": 1
                }
                
                # Add new company to the list
                MOCK_COMPANIES.append(new_company_data)
                
                response = {
                    "company": company_title,
                    "score": 0.55,
                    "risk_breakdown": {
                        "overall_score": 0.55,
                        "environmental_score": 0.50,
                        "social_score": 0.60,
                        "governance_score": 0.55
                    },
                    "events": [
                        {
                            "event_type": "governance_regulatory_fine",
                            "description": f"{company_title} is facing regulatory scrutiny over compliance issues.",
                            "severity": 0.6
                        }
                    ],
                    "articles": [
                        {
                            "title": f"{company_title} Reports Strong Q4 Earnings",
                            "content": f"{company_title} has reported strong fourth-quarter earnings, beating analyst expectations.",
                            "url": f"https://example.com/{company}-earnings",
                            "published_at": "2024-01-15T10:00:00Z",
                            "sentiment_score": 0.2,
                            "events": []
                        }
                    ],
                    "total_articles": 1,
                    "analyzed_at": datetime.now().isoformat() + "Z"
                }
        else:
            response = {"error": "Not found"}
        
        self.wfile.write(json.dumps(response).encode())

    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    server = HTTPServer(('localhost', 8001), ESGRequestHandler)
    print("🚀 ESG Risk Analyzer Backend running on http://localhost:8001")
    print("📊 Frontend should be on http://localhost:3000")
    print("🛑 Press Ctrl+C to stop")
    server.serve_forever()
