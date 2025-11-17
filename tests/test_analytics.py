"""
Unit tests for the conversational analytics platform
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import unittest
from src.nlp_engine import NLPEngine
from src.bigquery_analytics import BigQueryAnalytics


class TestNLPEngine(unittest.TestCase):
    """Test NLP Engine"""
    
    def setUp(self):
        self.nlp = NLPEngine()
    
    def test_intent_extraction(self):
        """Test intent extraction from queries"""
        test_cases = [
            ("Find education schemes", "search_scheme"),
            ("List all schemes", "list_schemes"),
            ("Show me statistics", "statistics"),
        ]
        
        for query, expected_intent in test_cases:
            intent = self.nlp.extract_intent(query)
            self.assertIn(expected_intent, intent)
    
    def test_entity_extraction(self):
        """Test entity extraction"""
        query = "Find education schemes in the health category"
        entities = self.nlp.extract_entities(query)
        
        self.assertIsInstance(entities, dict)
        self.assertIn("categories", entities)
    
    def test_query_parsing(self):
        """Test query parsing"""
        query = "Tell me about PM-JAY scheme"
        parsed = self.nlp.parse_query(query)
        
        self.assertIn("original_query", parsed)
        self.assertIn("intent", parsed)
        self.assertIn("entities", parsed)
    
    def test_results_formatting(self):
        """Test results formatting"""
        test_results = [
            {"scheme_name": "Test Scheme", "description": "A test scheme"}
        ]
        
        formatted = self.nlp.format_results(test_results, "search_scheme")
        self.assertIn("Test Scheme", formatted)
    
    def test_empty_results(self):
        """Test handling of empty results"""
        formatted = self.nlp.format_results([], "search_scheme")
        self.assertIsInstance(formatted, str)
        self.assertTrue(len(formatted) > 0)


class TestBigQueryAnalytics(unittest.TestCase):
    """Test BigQuery Analytics (mock tests)"""
    
    def test_initialization(self):
        """Test BigQueryAnalytics initialization"""
        try:
            analytics = BigQueryAnalytics(project_id="test-project")
            self.assertIsNotNone(analytics)
        except Exception as e:
            # Expected if credentials not available
            self.assertIn("credentials", str(e).lower())


if __name__ == "__main__":
    unittest.main()
