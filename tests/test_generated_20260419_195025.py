"""
Test suite for LAYER-MVP-0030: Regulatory Intelligence Risk Scanner
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from typing import List, Dict, Any

from layer_mvp_0030 import (
    RegulatoryDataIngester,
    APIDataSource,
    RSSDataSource,
    HTMLScrapingDataSource,
    RiskScorer,
    EventProcessor,
    RegulatoryEvent,
    Dashboard,
    UKREACHFramework,
    ModularRegulatoryFramework
)


class TestRegulatoryDataIngestion:
    """Test data ingestion from multiple sources"""
    
    def test_api_data_source_ingestion(self):
        """Test ingestion of regulatory data from API sources"""
        api_source = APIDataSource(
            endpoint="https://api.regulatory.gov/documents",
            api_key="test-key"
        )
        
        mock_response = {
            "documents": [
                {
                    "id": "REG-2024-001",
                    "title": "Chemical Safety Update",
                    "content": "New chemical restrictions announced",
                    "published_date": "2024-01-15T10:00:00Z",
                    "agency": "EPA"
                }
            ]
        }
        
        with patch.object(api_source, 'fetch_data', return_value=mock_response):
            data = api_source.ingest()
            
        assert len(data) == 1
        assert data[0]["id"] == "REG-2024-001"
        assert data[0]["title"] == "Chemical Safety Update"
        assert data[0]["agency"] == "EPA"
    
    def test_rss_feed_ingestion(self):
        """Test ingestion of regulatory data from RSS feeds"""
        rss_source = RSSDataSource(
            feed_url="https://regulatory.gov/rss/chemical-updates"
        )
        
        mock_feed_data = [
            {
                "title": "REACH Compliance Update",
                "link": "https://regulatory.gov/reach-update-001",
                "description": "Updated REACH requirements for chemical substances",
                "published": "Mon, 15 Jan 2024 10:00:00 GMT",
                "guid": "reach-001"
            }
        ]
        
        with patch.object(rss_source, 'parse_feed', return_value=mock_feed_data):
            data = rss_source.ingest()
            
        assert len(data) == 1
        assert data[0]["title"] == "REACH Compliance Update"
        assert "REACH requirements" in data[0]["description"]
    
    def test_html_scraping_ingestion(self):
        """Test ingestion of regulatory data from HTML scraping"""
        html_source = HTMLScrapingDataSource(
            base_url="https://regulatory-site.gov",
            selectors={
                "title": "h2.regulation-title",
                "content": "div.regulation-content",
                "date": "span.publish-date"
            }
        )
        
        mock_scraped_data = [
            {
                "title": "New Chemical Registration Requirements",
                "content": "Effective immediately, all chemical manufacturers must...",
                "date": "2024-01-15",
                "url": "https://regulatory-site.gov/reg-001",
                "source": "regulatory-site.gov"
            }
        ]
        
        with patch.object(html_source, 'scrape_pages', return_value=mock_scraped_data):
            data = html_source.ingest()
            
        assert len(data) == 1
        assert data[0]["title"] == "New Chemical Registration Requirements"
        assert "chemical manufacturers" in data[0]["content"]


class TestRegulatorySignalProcessing:
    """Test conversion of raw signals into structured events with risk scoring"""
    
    def test_risk_score_calculation(self):
        """Test risk scoring algorithm for regulatory signals"""
        risk_scorer = RiskScorer()
        
        raw_signal = {
            "title": "Immediate Chemical Ban Announcement",
            "content": "The following chemicals are banned effective immediately due to health risks",
            "keywords": ["ban", "immediate", "health risks", "toxic"],
            "agency": "EPA",
            "severity_indicators": ["immediate", "banned", "toxic"]
        }
        
        risk_score = risk_scorer.calculate_risk_score(raw_signal)
        
        assert risk_score >= 0.8  # High risk due to immediate ban and health risks
        assert isinstance(risk_score, float)
        assert 0 <= risk_score <= 1
    
    def test_structured_event_creation(self):
        """Test conversion of raw data into structured regulatory events"""
        event_processor = EventProcessor()
        
        raw_data = {
            "id": "REG-2024-001",
            "title": "REACH Substance Restriction",
            "content": "New restrictions on chemical substance ABC-123",
            "published_date": "2024-01-15T10:00:00Z",
            "source": "echa.europa.eu",
            "category": "chemical_restriction"
        }
        
        event = event_processor.create_structured_event(raw_data)
        
        assert isinstance(event, RegulatoryEvent)
        assert event.event_id == "REG-2024-001"
        assert event.title == "REACH Substance Restriction"
        assert event.category == "chemical_restriction"
        assert isinstance(event.risk_score, float)
        assert isinstance(event.created_at, datetime)
    
    def test_event_categorization(self):
        """Test automatic categorization of regulatory events"""
        event_processor = EventProcessor()
        
        chemical_event_data = {
            "title": "Chemical Safety Update",
            "content": "New chemical testing requirements",
            "keywords": ["chemical", "testing", "safety"]
        }
        
        environmental_event_data = {
            "title": "Environmental Protection Regulation",
            "content": "New air quality standards",
            "keywords": ["environmental", "air quality", "emissions"]
        }
        
        chemical_category = event_processor.categorize_event(chemical_event_data)
        environmental_category = event_processor.categorize_event(environmental_event_data)
        
        assert chemical_category == "chemical_safety"
        assert environmental_category == "environmental_protection"


class TestDashboardVisualization:
    """Test dashboard display with filtering and risk visualization"""
    
    def test_event_feed_display(self):
        """Test display of regulatory event feed on dashboard"""
        dashboard = Dashboard()
        
        mock_events = [
            RegulatoryEvent(
                event_id="REG-001",
                title="Chemical Ban",
                risk_score=0.9,
                category="chemical_restriction",
                created_at=datetime.now()
            ),
            RegulatoryEvent(
                event_id="REG-002", 
                title="Safety Update",
                risk_score=0.3,
                category="safety_guidance",
                created_at=datetime.now()
            )
        ]
        
        dashboard.load_events(mock_events)
        displayed_events = dashboard.get_event_feed()
        
        assert len(displayed_events) == 2
        assert displayed_events[0].event_id == "REG-001"
        assert displayed_events[1].event_id == "REG-002"
    
    def test_risk_based_filtering(self):
        """Test filtering events by risk level"""
        dashboard = Dashboard()
        
        mock_events = [
            RegulatoryEvent(event_id="HIGH-001", risk_score=0.9),
            RegulatoryEvent(event_id="MED-001", risk_score=0.5),
            RegulatoryEvent(event_id="LOW-001", risk_score=0.2)
        ]
        
        dashboard.load_events(mock_events)
        high_risk_events = dashboard.filter_by_risk_level("high")
        
        assert len(high_risk_events) == 1
        assert high_risk_events[0].event_id == "HIGH-001"
        assert high_risk_events[0].risk_score >= 0.7
    
    def test_category_filtering(self):
        """Test filtering events by regulatory category"""
        dashboard = Dashboard()
        
        mock_events = [
            RegulatoryEvent(event_id="CHEM-001", category="chemical_restriction"),
            RegulatoryEvent(event_id="ENV-001", category="environmental_protection"),
            RegulatoryEvent(event_id="CHEM-002", category="chemical_restriction")
        ]
        
        dashboard.load_events(mock_events)
        chemical_events = dashboard.filter_by_category("chemical_restriction")
        
        assert len(chemical_events) == 2
        assert all(event.category == "chemical_restriction" for event in chemical_events)
    
    def test_risk_visualization_data(self):
        """Test generation of risk visualization data"""
        dashboard = Dashboard()
        
        mock_events = [
            RegulatoryEvent(event_id="E1", risk_score=0.9, category="chemical"),
            RegulatoryEvent(event_id="E2", risk_score=0.5, category="environmental"),
            RegulatoryEvent(event_id="E3", risk_score=0.8, category="chemical")
        ]
        
        dashboard.load_events(mock_events)
        viz_data = dashboard.get_risk_visualization_data()
        
        assert "risk_distribution" in viz_data
        assert "category_breakdown" in viz_data
        assert viz_data["risk_distribution"]["high"] == 2
        assert viz_data["category_breakdown"]["chemical"] == 2


class TestModularFramework:
    """Test modular framework with UK REACH support and expansion capability"""
    
    def test_uk_reach_framework_initialization(self):
        """Test UK REACH framework module initialization"""
        uk_reach = UKREACHFramework()
        
        assert uk_reach.framework_name == "UK_REACH"
        assert uk_reach.jurisdiction == "United Kingdom"
        assert "chemical_registration" in uk_reach.supported_categories
        assert "substance_restriction" in uk_reach.supported_categories
    
    def test_uk_reach_specific_processing(self):
        """Test UK REACH specific data processing rules"""
        uk_reach = UKREACHFramework()
        
        reach_data = {
            "title": "REACH Dossier Update",
            "content": "Chemical substance XYZ requires updated safety data",
            "regulation_type": "REACH",
            "substance_id": "EC-123-456-7"
        }
        
        processed_event = uk_reach.process_regulatory_data(reach_data)
        
        assert processed_event.framework == "UK_REACH"
        assert processed_event.substance_id == "EC-123-456-7"
        assert processed_event.regulation_type == "REACH"
    
    def test_modular_framework_expansion(self):
        """Test addition of new regulatory framework modules"""
        modular_framework = ModularRegulatoryFramework()
        
        # Initially only UK REACH
        initial_frameworks = modular_framework.get_active_frameworks()
        assert "UK_REACH" in initial_frameworks
        
        # Add EU REACH framework
        eu_reach_config = {
            "name": "EU_REACH",
            "jurisdiction": "European Union",
            "categories": ["chemical_registration", "authorization", "restriction"]
        }
        
        modular_framework.add_framework("EU_REACH", eu_reach_config)
        updated_frameworks = modular_framework.get_active_frameworks()
        
        assert "EU_REACH" in updated_frameworks
        assert len(updated_frameworks) == 2
    
    def test_framework_routing(self):
        """Test routing of regulatory data to appropriate framework"""
        modular_framework = ModularRegulatoryFramework()
        
        uk_data = {
            "source": "gov.uk",
            "jurisdiction": "UK",
            "regulation": "REACH"
        }
        
        eu_data = {
            "source": "echa.europa.eu", 
            "jurisdiction": "EU",
            "regulation": "REACH"
        }
        
        uk_framework = modular_framework.route_to_framework(uk_data)
        eu_framework = modular_framework.route_to_framework(eu_data)
        
        assert uk_framework == "UK_REACH"
        assert eu_framework == "EU_REACH"


class TestIntegrationDataProcessing:
    """Testing the complete flow from data source ingestion through risk scoring and event creation"""
    
    def test_api_ingestion_to_risk_scoring(self):
        """Test complete pipeline from API ingestion to risk scoring"""
        ingester = RegulatoryDataIngester()
        api_source = APIDataSource(endpoint="https://api.test.gov/regs")
        risk_scorer = RiskScorer()
        
        mock_api_data = [
            {
                "id": "API-001",
                "title": "Critical Chemical Safety Alert",
                "content": "Immediate action required for chemical ABC",
                "severity": "high",
                "effective_date": "2024-01-20T00:00:00Z"
            }
        ]
        
        with patch.object(api_source, 'ingest', return_value=mock_api_data):
            ingester.add_source(api_source)
            raw_data = ingester.ingest_all_sources()
            
            processed_events = []
            for item in raw_data:
                risk_score = risk_scorer.calculate_risk_score(item)
                event = RegulatoryEvent(
                    event_id=item["id"],
                    title=item["title"],
                    risk_score=risk_score
                )
                processed_events.append(event)
        
        assert len(processed_events) == 1
        assert processed_events[0].event_id == "API-001"
        assert processed_events[0].risk_score > 0.7  # High risk due to "Critical" and "Immediate"
    
    def test_rss_feed_processing_pipeline(self):
        """Test complete RSS feed processing through event creation"""
        ingester = RegulatoryDataIngester()
        rss_source = RSSDataSource(feed_url="https://feed.regulatory.gov/updates")
        event_processor = EventProcessor()
        
        mock_rss_data = [
            {
                "title": "REACH Compliance Deadline Extended",
                "description": "Registration deadline for chemical substances extended to March 2024",
                "link": "https://regulatory.gov/reach-extension",
                "published": "2024-01-15T09:00:00Z"
            }
        ]
        
        with patch.object(rss_source, 'ingest', return_value=mock_rss_data):
            ingester.add_source(rss_source)
            raw_data = ingester.ingest_all_sources()
            
            events = []
            for item in raw_data:
                event = event_processor.create_structured_event(item)
                events.append(event)
        
        assert len(events) == 1
        assert events[0].title == "REACH Compliance Deadline Extended"
        assert events[0].source_url == "https://regulatory.gov/reach-extension"
        assert isinstance(events[0].risk_score, float)
    
    def test_html_scraping_to_structured_events(self):
        """Test HTML scraping through structured event creation"""
        ingester = RegulatoryDataIngester()
        html_source = HTMLScrapingDataSource(base_url="https://regulations.gov")
        event_processor = EventProcessor()
        uk_reach = UKREACHFramework()
        
        mock_scraped_data = [
            {
                "title": "UK REACH Substance Authorization",
                "content": "New authorization requirements for substance EC-200-001-8",
                "date": "2024-01-14",
                "regulation_type": "authorization",
                "substance_id": "EC-200-001-8"
            }
        ]
        
        with patch.object(html_source, 'ingest', return_value=mock_scraped_data):
            ingester.add_source(html_source)
            raw_data = ingester.ingest_all_sources()
            
            structured_events = []
            for item in raw_data:
                if "REACH" in item.get("title", ""):
                    event = uk_reach.process_regulatory_data(item)
                else:
                    event = event_processor.create_structured_event(item)
                structured_events.append(event)
        
        assert len(structured_events) == 1
        assert structured_events[0].framework == "UK_REACH"
        assert structured_events[0].substance_id == "EC-200-001-8"
        assert structured_events[0].regulation_type == "authorization"


class TestE2ERegulatoryWorkflow:
    """Testing complete user workflow from regulatory change detection through dashboard visualization and filtering"""
    
    def test_regulatory_change_detection_to_dashboard_display(self):
        """Test complete workflow from change detection to dashboard display"""
        # Setup complete system
        ingester = RegulatoryDataIngester()
        api_source = APIDataSource(endpoint="https://api.regulatory.gov/changes")
        risk_scorer = RiskScorer()
        event_processor = EventProcessor()
        dashboard = Dashboard()
        
        # Mock regulatory change detected
        mock_change_data = [
            {
                "id": "CHANGE-001",
                "title": "Emergency Chemical Restriction",
                "content": "Chemical XYZ-789 restricted due to health concerns",
                "change_type": "restriction",
                "urgency": "emergency",
                "effective_immediately": True,
                "published_date": "2024-01-15T14:30:00Z"
            }
        ]
        
        with patch.object(api_source, 'ingest', return_value=mock_change_data):
            # Ingest regulatory changes
            ingester.add_source(api_source)
            changes = ingester.ingest_all_sources()
            
            # Process into events
            events = []
            for change in changes:
                risk_score = risk_scorer.calculate_risk_score(change)
                event = event_processor.create_structured_event(change)
                event.risk_score = risk_score
                events.append(event)
            
            # Display on dashboard
            dashboard.load_events(events)
            displayed_feed = dashboard.get_event_feed()
        
        # Verify end-to-end flow
        assert len(displayed_feed) == 1
        assert displayed_feed[0].event_id == "CHANGE-001"
        assert displayed_feed[0].title == "Emergency Chemical Restriction"
        assert displayed_feed[0].risk_score >= 0.8  # High risk due to emergency restriction
        assert "Chemical XYZ-789" in displayed_feed[0].content
    
    def test_user_filtering_and_risk_prioritization_workflow(self):
        """Test complete user workflow for filtering and prioritizing regulatory events"""
        dashboard = Dashboard()
        
        # Load multiple events with varying risk levels and categories
        mock_events = [
            RegulatoryEvent(
                event_id="HIGH-CHEM-001",
                title="Immediate Chemical Ban",
                risk_score=0.95,
                category="chemical_restriction",
                created_at=datetime.now() - timedelta(hours=1)
            ),
            RegulatoryEvent(
                event_id="MED-ENV-001", 
                title="Environmental Guideline Update",
                risk_score=0.6,
                category="environmental_guidance",
                created_at=datetime.now() - timedelta(hours=2)
            ),
            RegulatoryEvent(
                event_id="LOW-SAFE-001",
                title="Safety Documentation Template",
                risk_score=0.2,
                category="documentation",
                created_at=datetime.now() - timedelta(hours=3)
            ),
            RegulatoryEvent(
                event_id="HIGH-REACH-001",
                title="Critical REACH Compliance Alert",
                risk_score=0.9,
                category="chemical_registration", 
                created_at=datetime.now() - timedelta(minutes=30)
            )
        ]
        
        dashboard.load_events(mock_events)
        
        # User workflow: Filter by high risk
        high_risk_events = dashboard.filter_by_risk_level("high")
        assert len(high_risk_events) == 2
        assert all(event.risk_score >= 0.7 for event in high_risk_events)
        
        # User workflow: Filter high risk chemical events
        high_risk_chemical = dashboard.filter_by_category("chemical_restriction", 
                                                        risk_threshold=0.7)
        assert len(high_risk_chemical) == 1
        assert high_risk_chemical[0].event_id == "HIGH-CHEM-001"
        
        # User workflow: Get prioritized event list (sorted by risk and recency)
        prioritized_events = dashboard.get_prioritized_events()
        assert prioritized_events[0].event_id == "HIGH-REACH-001"  # Most recent high risk
        assert prioritized_events[1].event_id == "HIGH-CHEM-001"   # Second most recent high risk
        
        # User workflow: Create risk summary for decision making
        risk_summary = dashboard.generate_risk_summary()
        assert risk_summary["total_events"] == 4
        assert risk_summary["high_risk_count"] == 2
        assert risk_summary["critical_categories"] == ["chemical_restriction", "chemical_registration"]
