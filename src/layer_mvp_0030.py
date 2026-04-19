"""
LAYER-MVP-0030: Regulatory Intelligence Risk Scanner

System for ingesting regulatory data from multiple sources, converting raw signals
into structured events with risk scoring, and providing dashboard visualization
with modular framework support including UK REACH.
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Union
import re
from dataclasses import dataclass, field
from collections import defaultdict
import json


@dataclass
class RegulatoryEvent:
    """Structured regulatory event with risk scoring"""
    event_id: str
    title: str = ""
    content: str = ""
    risk_score: float = 0.0
    category: str = ""
    source_url: str = ""
    framework: str = ""
    substance_id: str = ""
    regulation_type: str = ""
    created_at: datetime = field(default_factory=datetime.now)


class DataSource(ABC):
    """Abstract base class for regulatory data sources"""
    
    @abstractmethod
    def ingest(self) -> List[Dict[str, Any]]:
        """Ingest data from the source"""
        pass


class APIDataSource(DataSource):
    """Data source for regulatory APIs"""
    
    def __init__(self, endpoint: str, api_key: str = None):
        self.endpoint = endpoint
        self.api_key = api_key
    
    def ingest(self) -> List[Dict[str, Any]]:
        """Ingest data from API endpoint"""
        # This would normally make HTTP requests
        response = self.fetch_data()
        if "documents" in response:
            return response["documents"]
        return [response] if response else []
    
    def fetch_data(self) -> Dict[str, Any]:
        """Fetch data from API - to be mocked in tests"""
        # Placeholder for actual API implementation
        return {"documents": []}


class RSSDataSource(DataSource):
    """Data source for RSS feeds"""
    
    def __init__(self, feed_url: str):
        self.feed_url = feed_url
    
    def ingest(self) -> List[Dict[str, Any]]:
        """Ingest data from RSS feed"""
        return self.parse_feed()
    
    def parse_feed(self) -> List[Dict[str, Any]]:
        """Parse RSS feed - to be mocked in tests"""
        # Placeholder for actual RSS parsing implementation
        return []


class HTMLScrapingDataSource(DataSource):
    """Data source for HTML scraping"""
    
    def __init__(self, base_url: str, selectors: Dict[str, str] = None):
        self.base_url = base_url
        self.selectors = selectors or {}
    
    def ingest(self) -> List[Dict[str, Any]]:
        """Ingest data from HTML scraping"""
        return self.scrape_pages()
    
    def scrape_pages(self) -> List[Dict[str, Any]]:
        """Scrape HTML pages - to be mocked in tests"""
        # Placeholder for actual scraping implementation
        return []


class RiskScorer:
    """Calculate risk scores for regulatory signals"""
    
    def __init__(self):
        self.high_risk_keywords = [
            'immediate', 'emergency', 'critical', 'urgent', 'ban', 'banned', 
            'toxic', 'dangerous', 'health risks', 'carcinogenic', 'prohibited'
        ]
        self.medium_risk_keywords = [
            'restriction', 'limitation', 'warning', 'caution', 'update',
            'revised', 'compliance', 'deadline'
        ]
        self.severity_multipliers = {
            'immediate': 1.5,
            'emergency': 1.4,
            'critical': 1.3,
            'urgent': 1.2
        }
    
    def calculate_risk_score(self, signal: Dict[str, Any]) -> float:
        """Calculate risk score for a regulatory signal"""
        base_score = 0.1
        
        # Combine text fields for analysis
        text_content = " ".join([
            str(signal.get('title', '')),
            str(signal.get('content', '')),
            str(signal.get('description', ''))
        ]).lower()
        
        # Check for high risk keywords
        high_risk_matches = sum(1 for keyword in self.high_risk_keywords 
                               if keyword in text_content)
        base_score += high_risk_matches * 0.3
        
        # Check for medium risk keywords
        medium_risk_matches = sum(1 for keyword in self.medium_risk_keywords 
                                 if keyword in text_content)
        base_score += medium_risk_matches * 0.15
        
        # Apply severity multipliers
        for severity, multiplier in self.severity_multipliers.items():
            if severity in text_content:
                base_score *= multiplier
                break
        
        # Check specific signal attributes
        if signal.get('urgency') == 'emergency':
            base_score += 0.4
        
        if signal.get('effective_immediately') is True:
            base_score += 0.3
        
        if signal.get('change_type') == 'restriction':
            base_score += 0.2
        
        # Normalize to 0-1 range
        return min(1.0, base_score)


class EventProcessor:
    """Process raw regulatory data into structured events"""
    
    def __init__(self):
        self.risk_scorer = RiskScorer()
        self.category_keywords = {
            'chemical_safety': ['chemical', 'substance', 'safety', 'testing'],
            'chemical_restriction': ['restriction', 'ban', 'prohibited', 'chemical'],
            'environmental_protection': ['environmental', 'air quality', 'emissions', 'water'],
            'safety_guidance': ['guidance', 'safety', 'best practices'],
            'documentation': ['documentation', 'template', 'reporting'],
            'chemical_registration': ['registration', 'reach', 'authorization']
        }
    
    def create_structured_event(self, raw_data: Dict[str, Any]) -> RegulatoryEvent:
        """Convert raw data into structured regulatory event"""
        event_id = raw_data.get('id', raw_data.get('guid', f"EVENT-{datetime.now().timestamp()}"))
        title = raw_data.get('title', '')
        content = raw_data.get('content', raw_data.get('description', ''))
        
        # Calculate risk score
        risk_score = self.risk_scorer.calculate_risk_score(raw_data)
        
        # Categorize event
        category = self.categorize_event(raw_data)
        
        # Extract source URL
        source_url = raw_data.get('link', raw_data.get('url', ''))
        
        return RegulatoryEvent(
            event_id=event_id,
            title=title,
            content=content,
            risk_score=risk_score,
            category=category,
            source_url=source_url,
            created_at=self._parse_date(raw_data.get('published_date', raw_data.get('published', raw_data.get('date'))))
        )
    
    def categorize_event(self, event_data: Dict[str, Any]) -> str:
        """Automatically categorize regulatory events"""
        text_content = " ".join([
            str(event_data.get('title', '')),
            str(event_data.get('content', '')),
            str(event_data.get('description', ''))
        ]).lower()
        
        # Check keywords for each category
        category_scores = {}
        for category, keywords in self.category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text_content)
            if score > 0:
                category_scores[category] = score
        
        # Return category with highest score
        if category_scores:
            return max(category_scores, key=category_scores.get)
        
        return "general"
    
    def _parse_date(self, date_str: Any) -> datetime:
        """Parse date string into datetime object"""
        if isinstance(date_str, datetime):
            return date_str
        
        if not date_str:
            return datetime.now()
        
        # Try common date formats
        date_formats = [
            '%Y-%m-%dT%H:%M:%SZ',
            '%a, %d %b %Y %H:%M:%S GMT',
            '%Y-%m-%d'
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(str(date_str), fmt)
            except ValueError:
                continue
        
        return datetime.now()


class Dashboard:
    """Dashboard for displaying regulatory events with filtering and visualization"""
    
    def __init__(self):
        self.events: List[RegulatoryEvent] = []
    
    def load_events(self, events: List[RegulatoryEvent]) -> None:
        """Load events into the dashboard"""
        self.events = events
    
    def get_event_feed(self) -> List[RegulatoryEvent]:
        """Get all events for display"""
        return sorted(self.events, key=lambda e: e.created_at, reverse=True)
    
    def filter_by_risk_level(self, risk_level: str) -> List[RegulatoryEvent]:
        """Filter events by risk level"""
        risk_thresholds = {
            'high': 0.7,
            'medium': 0.3,
            'low': 0.0
        }
        
        threshold = risk_thresholds.get(risk_level.lower(), 0.0)
        
        if risk_level.lower() == 'high':
            return [event for event in self.events if event.risk_score >= threshold]
        elif risk_level.lower() == 'medium':
            return [event for event in self.events if 0.3 <= event.risk_score < 0.7]
        else:
            return [event for event in self.events if event.risk_score < 0.3]
    
    def filter_by_category(self, category: str, risk_threshold: float = 0.0) -> List[RegulatoryEvent]:
        """Filter events by category with optional risk threshold"""
        filtered = [event for event in self.events 
                   if event.category == category and event.risk_score >= risk_threshold]
        return filtered
    
    def get_risk_visualization_data(self) -> Dict[str, Any]:
        """Generate data for risk visualization"""
        risk_distribution = {'high': 0, 'medium': 0, 'low': 0}
        category_breakdown = defaultdict(int)
        
        for event in self.events:
            # Risk distribution
            if event.risk_score >= 0.7:
                risk_distribution['high'] += 1
            elif event.risk_score >= 0.3:
                risk_distribution['medium'] += 1
            else:
                risk_distribution['low'] += 1
            
            # Category breakdown
            category_breakdown[event.category] += 1
        
        return {
            'risk_distribution': risk_distribution,
            'category_breakdown': dict(category_breakdown)
        }
    
    def get_prioritized_events(self) -> List[RegulatoryEvent]:
        """Get events prioritized by risk score and recency"""
        # Sort by risk score first (descending), then by timestamp (descending for most recent)
        return sorted(self.events, 
                     key=lambda e: (e.risk_score, e.created_at.timestamp()), 
                     reverse=True)
    
    def generate_risk_summary(self) -> Dict[str, Any]:
        """Generate risk summary for decision making"""
        total_events = len(self.events)
        high_risk_events = [e for e in self.events if e.risk_score >= 0.7]
        high_risk_count = len(high_risk_events)
        
        # Find critical categories (categories with high-risk events)
        critical_categories = sorted(list(set(event.category for event in high_risk_events)))
        
        return {
            'total_events': total_events,
            'high_risk_count': high_risk_count,
            'critical_categories': critical_categories
        }


class UKREACHFramework:
    """UK REACH regulatory framework module"""
    
    def __init__(self):
        self.framework_name = "UK_REACH"
        self.jurisdiction = "United Kingdom"
        self.supported_categories = [
            "chemical_registration",
            "substance_restriction", 
            "authorization",
            "evaluation"
        ]
    
    def process_regulatory_data(self, data: Dict[str, Any]) -> RegulatoryEvent:
        """Process regulatory data specific to UK REACH"""
        event = RegulatoryEvent(
            event_id=data.get('id', f"UK-REACH-{datetime.now().timestamp()}"),
            title=data.get('title', ''),
            content=data.get('content', ''),
            framework=self.framework_name,
            substance_id=data.get('substance_id', ''),
            regulation_type=data.get('regulation_type', data.get('type', '')),
            created_at=datetime.now()
        )
        
        # Calculate risk score using framework-specific logic
        risk_scorer = RiskScorer()
        event.risk_score = risk_scorer.calculate_risk_score(data)
        
        return event


class ModularRegulatoryFramework:
    """Modular framework for managing multiple regulatory systems"""
    
    def __init__(self):
        self.frameworks = {
            'UK_REACH': UKREACHFramework()
        }
        self.framework_configs = {}
    
    def get_active_frameworks(self) -> List[str]:
        """Get list of active framework names"""
        # Return both instantiated frameworks and configured ones
        all_frameworks = set(self.frameworks.keys())
        all_frameworks.update(self.framework_configs.keys())
        return list(all_frameworks)
    
    def add_framework(self, name: str, config: Dict[str, Any]) -> None:
        """Add new regulatory framework module"""
        self.framework_configs[name] = config
        # In a real implementation, this would instantiate the framework class
        # For now, we just track it in configs which get_active_frameworks() will include
        
    def route_to_framework(self, data: Dict[str, Any]) -> str:
        """Route regulatory data to appropriate framework"""
        jurisdiction = data.get('jurisdiction', '').upper()
        source = data.get('source', '').lower()
        
        # Simple routing logic
        if jurisdiction == 'UK' or 'gov.uk' in source:
            return 'UK_REACH'
        elif jurisdiction == 'EU' or 'echa.europa.eu' in source:
            return 'EU_REACH'
        
        # Default to UK REACH
        return 'UK_REACH'


class RegulatoryDataIngester:
    """Main ingester for coordinating multiple data sources"""
    
    def __init__(self):
        self.sources: List[DataSource] = []
    
    def add_source(self, source: DataSource) -> None:
        """Add a data source to the ingester"""
        self.sources.append(source)
    
    def ingest_all_sources(self) -> List[Dict[str, Any]]:
        """Ingest data from all configured sources"""
        all_data = []
        for source in self.sources:
            try:
                source_data = source.ingest()
                all_data.extend(source_data)
            except Exception as e:
                # Log error and continue with other sources
                print(f"Error ingesting from {type(source).__name__}: {e}")
                continue
        
        return all_data
