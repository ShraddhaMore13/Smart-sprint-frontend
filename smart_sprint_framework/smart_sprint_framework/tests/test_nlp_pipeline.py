import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp_pipeline import NLPPipeline

class TestNLPPipeline(unittest.TestCase):
    def setUp(self):
        self.nlp = NLPPipeline()
    
    def test_extract_entities(self):
        """Test entity extraction from text"""
        text = "This is a high priority task that needs to be completed by Friday."
        entities = self.nlp.extract_entities(text)
        
        self.assertIn('priorities', entities)
        self.assertIn('high', entities['priorities'])
    
    def test_analyze_complexity(self):
        """Test complexity analysis"""
        simple_text = "This is a simple task."
        complex_text = "This is a complex task that requires multiple integrations and advanced algorithms."
        
        simple_complexity = self.nlp.analyze_complexity(simple_text)
        complex_complexity = self.nlp.analyze_complexity(complex_text)
        
        self.assertGreaterEqual(complex_complexity, simple_complexity)
        self.assertGreaterEqual(complex_complexity, 1)
        self.assertLessEqual(complex_complexity, 5)
    
    def test_analyze_sentiment(self):
        """Test sentiment analysis"""
        positive_text = "This is great! Everything is working perfectly."
        negative_text = "This is terrible. Nothing is working as expected."
        
        positive_sentiment = self.nlp.analyze_sentiment(positive_text)
        negative_sentiment = self.nlp.analyze_sentiment(negative_text)
        
        self.assertIn('label', positive_sentiment)
        self.assertIn('score', positive_sentiment)
        self.assertIn('label', negative_sentiment)
        self.assertIn('score', negative_sentiment)

if __name__ == '__main__':
    unittest.main()