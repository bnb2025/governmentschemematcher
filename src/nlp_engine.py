"""
NLP Engine Module - Natural Language Processing and query parsing
"""

from typing import Dict, Optional, List
import re


class NLPEngine:
    """Handles natural language processing and query interpretation"""
    
    def __init__(self):
        """Initialize NLP Engine"""
        self.intent_keywords = {
            "search_scheme": ["find", "search", "look for", "show", "get", "what scheme"],
            "list_schemes": ["list", "all schemes", "available schemes", "show all"],
            "scheme_details": ["details", "information", "about", "tell me"],
            "statistics": ["stats", "statistics", "how many", "count"],
            "eligibility": ["eligible", "qualify", "requirements", "criteria"],
            "apply": ["apply", "registration", "enroll"],
        }
    
    def extract_intent(self, text: str) -> str:
        """
        Extract intent from user's natural language query
        
        Args:
            text: User's spoken or typed query
            
        Returns:
            Intent type (e.g., 'search_scheme')
        """
        text_lower = text.lower()
        
        for intent, keywords in self.intent_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent
        
        return "search_scheme"  # Default intent
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract entities from user's query
        
        Args:
            text: User's query
            
        Returns:
            Dictionary of extracted entities
        """
        entities = {
            "scheme_names": [],
            "categories": [],
            "keywords": [],
        }
        
        # Common government scheme categories
        categories = ["education", "health", "agriculture", "employment", "housing"]
        text_lower = text.lower()
        
        for category in categories:
            if category in text_lower:
                entities["categories"].append(category)
        
        # Extract potential scheme names (capitalized words)
        words = text.split()
        for word in words:
            if word[0].isupper() and len(word) > 3:
                entities["scheme_names"].append(word)
        
        # Extract keywords (words in quotes)
        quoted = re.findall(r'"([^"]*)"', text)
        entities["keywords"].extend(quoted)
        
        return entities
    
    def parse_query(self, text: str) -> Dict:
        """
        Parse user query into structured format
        
        Args:
            text: User's natural language query
            
        Returns:
            Parsed query structure
        """
        return {
            "original_query": text,
            "intent": self.extract_intent(text),
            "entities": self.extract_entities(text),
            "normalized": text.lower().strip(),
        }
    
    def format_results(self, results: List[Dict], intent: str) -> str:
        """
        Format query results into natural language response
        
        Args:
            results: Query results from BigQuery
            intent: Original intent
            
        Returns:
            Formatted response string
        """
        if not results:
            return "I couldn't find any matching schemes. Please try a different search."
        
        if intent == "statistics":
            result = results[0]
            return f"There are {result.get('total_schemes', 0)} government schemes available in {result.get('total_categories', 0)} categories."
        
        # Format scheme information
        response_parts = []
        response_parts.append(f"I found {len(results)} matching schemes:")
        
        for i, scheme in enumerate(results, 1):
            scheme_info = f"\n{i}. "
            
            if "scheme_name" in scheme:
                scheme_info += f"{scheme['scheme_name']}"
            
            if "description" in scheme:
                scheme_info += f" - {scheme['description']}"
            
            response_parts.append(scheme_info)
        
        return "".join(response_parts)
    
    def generate_followup_questions(self, last_result: Dict) -> List[str]:
        """
        Generate suggested follow-up questions based on results
        
        Args:
            last_result: Last query result
            
        Returns:
            List of suggested questions
        """
        questions = [
            "Would you like more details about this scheme?",
            "Are you eligible to apply?",
            "Do you need help with the application?",
        ]
        
        return questions
