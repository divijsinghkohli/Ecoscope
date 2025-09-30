import re
from typing import List, Dict
from app.models import ESGEventResponse

class SimpleNLPService:
    def __init__(self):
        # ESG-related keywords and their categories
        self.esg_keywords = {
            'environmental': [
                'emissions', 'carbon footprint', 'climate change', 'pollution', 'oil spill',
                'deforestation', 'waste management', 'renewable energy', 'sustainability',
                'greenhouse gas', 'environmental impact', 'ecological', 'biodiversity'
            ],
            'social': [
                'labor strike', 'layoffs', 'workplace safety', 'human rights', 'diversity',
                'employee treatment', 'community impact', 'child labor', 'working conditions',
                'discrimination', 'harassment', 'union', 'wage', 'benefits'
            ],
            'governance': [
                'regulatory fine', 'lawsuit', 'corruption', 'bribery', 'fraud', 'scandal',
                'compliance', 'ethics', 'transparency', 'board', 'executive compensation',
                'audit', 'whistleblower', 'regulatory violation', 'legal action'
            ]
        }
        
        # Risk severity mapping
        self.severity_keywords = {
            'high': ['lawsuit', 'fine', 'strike', 'spill', 'scandal', 'fraud', 'corruption'],
            'medium': ['violation', 'concern', 'issue', 'problem', 'controversy'],
            'low': ['improvement', 'initiative', 'program', 'effort', 'commitment']
        }

    def analyze_sentiment(self, text: str) -> float:
        """Simple sentiment analysis based on keyword matching"""
        text_lower = text.lower()
        
        # Positive keywords
        positive_words = ['good', 'great', 'excellent', 'positive', 'improvement', 'success', 'growth', 'profit']
        negative_words = ['bad', 'terrible', 'negative', 'problem', 'issue', 'concern', 'violation', 'fine', 'strike']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count + negative_count == 0:
            return 0.0
        
        # Return sentiment between -1 and 1
        return (positive_count - negative_count) / (positive_count + negative_count)

    def detect_esg_events(self, text: str) -> List[ESGEventResponse]:
        """Detect ESG-related events in text using simple keyword matching"""
        events = []
        text_lower = text.lower()
        
        for category, keywords in self.esg_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # Find context around the keyword
                    context = self._extract_context(text, keyword)
                    
                    # Determine severity
                    severity = self._calculate_severity(text_lower, keyword)
                    
                    # Create event
                    event = ESGEventResponse(
                        event_type=f"{category}_{keyword.replace(' ', '_')}",
                        description=context,
                        severity=severity
                    )
                    events.append(event)
        
        # Remove duplicates and return
        return self._deduplicate_events(events)

    def _extract_context(self, text: str, keyword: str, context_length: int = 100) -> str:
        """Extract context around a keyword"""
        text_lower = text.lower()
        keyword_lower = keyword.lower()
        
        if keyword_lower not in text_lower:
            return ""
        
        start_idx = text_lower.find(keyword_lower)
        start_context = max(0, start_idx - context_length)
        end_context = min(len(text), start_idx + len(keyword) + context_length)
        
        return text[start_context:end_context].strip()

    def _calculate_severity(self, text: str, keyword: str) -> float:
        """Calculate severity score based on keywords and context"""
        base_severity = 0.5  # Default medium severity
        
        # Check for high severity indicators
        for high_severity_word in self.severity_keywords['high']:
            if high_severity_word in text:
                base_severity = max(base_severity, 0.8)
        
        # Check for medium severity indicators
        for medium_severity_word in self.severity_keywords['medium']:
            if medium_severity_word in text:
                base_severity = max(base_severity, 0.6)
        
        # Check for low severity indicators
        for low_severity_word in self.severity_keywords['low']:
            if low_severity_word in text:
                base_severity = min(base_severity, 0.3)
        
        return base_severity

    def _deduplicate_events(self, events: List[ESGEventResponse]) -> List[ESGEventResponse]:
        """Remove duplicate events based on event type"""
        seen_types = set()
        unique_events = []
        
        for event in events:
            if event.event_type not in seen_types:
                seen_types.add(event.event_type)
                unique_events.append(event)
        
        return unique_events

    def calculate_risk_scores(self, articles: List[Dict], events: List[ESGEventResponse]) -> Dict[str, float]:
        """Calculate overall risk scores based on articles and events"""
        if not articles:
            return {
                'overall_score': 0.0,
                'environmental_score': 0.0,
                'social_score': 0.0,
                'governance_score': 0.0
            }
        
        # Calculate average sentiment (negative sentiment = higher risk)
        sentiment_scores = [article.get('sentiment_score', 0) for article in articles]
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
        
        # Convert sentiment to risk (negative sentiment = higher risk)
        sentiment_risk = (1 - avg_sentiment) / 2  # Convert from [-1,1] to [0,1]
        
        # Calculate event-based risk
        event_risk = 0.0
        if events:
            event_severities = [event.severity for event in events]
            event_risk = sum(event_severities) / len(event_severities)
        
        # Calculate category-specific scores
        category_scores = {'environmental': 0.0, 'social': 0.0, 'governance': 0.0}
        
        for event in events:
            category = event.event_type.split('_')[0]
            if category in category_scores:
                category_scores[category] = max(category_scores[category], event.severity)
        
        # Overall score is weighted combination
        overall_score = (sentiment_risk * 0.4) + (event_risk * 0.6)
        
        return {
            'overall_score': min(1.0, overall_score),
            'environmental_score': category_scores['environmental'],
            'social_score': category_scores['social'],
            'governance_score': category_scores['governance']
        }
