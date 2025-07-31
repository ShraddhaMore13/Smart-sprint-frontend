import re
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

class NLPPipeline:
    def __init__(self):
        # Priority keywords (fallback)
        self.priority_keywords = {
            'high': ['high', 'critical', 'urgent', 'asap', 'immediately', 'important'],
            'medium': ['medium', 'normal', 'regular', 'standard'],
            'low': ['low', 'minor', 'optional', 'later', 'nice-to-have']
        }
        
        # Complexity indicators (fallback)
        self.complexity_keywords = {
            'high': ['complex', 'complicated', 'difficult', 'challenging', 'advanced', 
                    'multiple', 'integrate', 'scalable', 'distributed', 'enterprise'],
            'medium': ['moderate', 'several', 'some', 'few', 'update', 'improve'],
            'low': ['simple', 'basic', 'easy', 'straightforward', 'single', 'minor']
        }
        
        # Initialize BERT-based models
        try:
            self.sentiment_analyzer = pipeline("sentiment-analysis")
            self.ner_analyzer = pipeline("ner", grouped_entities=True)
            self.zero_shot_classifier = pipeline("zero-shot-classification")
            self.advanced_nlp = True
            print("Advanced NLP models loaded successfully")
        except Exception as e:
            print(f"Failed to load advanced NLP models: {e}")
            self.advanced_nlp = False
    
    def extract_entities(self, text):
        """Extract entities like priorities, dependencies, deadlines from text"""
        entities = {
            'priorities': [],
            'dependencies': [],
            'deadlines': [],
            'tasks': []
        }
        
        text_lower = text.lower()
        
        # Check for priority keywords (fallback)
        for priority, keywords in self.priority_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    entities['priorities'].append(priority)
                    break
        
        # If no priority found, default to medium
        if not entities['priorities']:
            entities['priorities'].append('medium')
        
        # Use advanced NLP if available
        if self.advanced_nlp:
            try:
                # Extract tasks using zero-shot classification
                task_labels = ["task", "feature", "bug fix", "improvement", "documentation"]
                result = self.zero_shot_classifier(text, task_labels)
                
                if result['labels'][0] == "task" and result['scores'][0] > 0.7:
                    # Extract potential task descriptions
                    sentences = re.split(r'[.!?]+', text)
                    for sentence in sentences:
                        if len(sentence.strip()) > 10:  # Ignore very short sentences
                            entities['tasks'].append(sentence.strip())
                
                # Extract dependencies using pattern matching
                dep_patterns = [
                    r'dependenc(?:y|ies)\s*[:\-]?\s*([^\n\r]+)',
                    r'requires?\s+([^\n\r]+)',
                    r'after\s+([^\n\r]+)',
                    r'blocked\s+by\s+([^\n\r]+)'
                ]
                
                for pattern in dep_patterns:
                    matches = re.findall(pattern, text_lower)
                    entities['dependencies'].extend(matches)
                
                # Extract deadlines
                deadline_patterns = [
                    r'deadline\s*[:\-]?\s*([^\n\r]+)',
                    r'due\s*[:\-]?\s*([^\n\r]+)',
                    r'by\s+([A-Za-z]+\s+\d{1,2},?\s+\d{4})',
                    r'before\s+([^\n\r]+)'
                ]
                
                for pattern in deadline_patterns:
                    matches = re.findall(pattern, text_lower)
                    entities['deadlines'].extend(matches)
                
            except Exception as e:
                print(f"Error in advanced NLP processing: {e}")
        
        return entities
    
    def analyze_complexity(self, text):
        """Analyze complexity of text on a scale of 1-5 using BERT if available"""
        if self.advanced_nlp:
            try:
                # Use zero-shot classification for complexity
                complexity_labels = ["very simple", "simple", "moderate", "complex", "very complex"]
                result = self.zero_shot_classifier(text, complexity_labels)
                
                # Map to 1-5 scale
                complexity_map = {
                    "very simple": 1,
                    "simple": 2,
                    "moderate": 3,
                    "complex": 4,
                    "very complex": 5
                }
                
                top_label = result['labels'][0]
                return complexity_map.get(top_label, 3)
                
            except Exception as e:
                print(f"Error in complexity analysis: {e}")
        
        # Fallback to keyword-based analysis
        text_lower = text.lower()
        
        # Count complexity indicators
        high_count = sum(1 for keyword in self.complexity_keywords['high'] if keyword in text_lower)
        medium_count = sum(1 for keyword in self.complexity_keywords['medium'] if keyword in text_lower)
        low_count = sum(1 for keyword in self.complexity_keywords['low'] if keyword in text_lower)
        
        # Calculate score (weighted)
        score = (high_count * 3) + (medium_count * 2) + (low_count * 1)
        
        # Normalize to 1-5 scale
        complexity = min(5, max(1, int(score / 2) + 1))
        
        # Adjust based on text length (longer descriptions might be more complex)
        if len(text) > 500:
            complexity = min(5, complexity + 1)
        elif len(text) < 100:
            complexity = max(1, complexity - 1)
        
        return complexity
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of text using BERT if available"""
        if self.advanced_nlp:
            try:
                result = self.sentiment_analyzer(text)[0]
                return {
                    'label': result['label'],
                    'score': result['score']
                }
            except Exception as e:
                print(f"Error in sentiment analysis: {e}")
        
        # Fallback to simple keyword-based sentiment
        text_lower = text.lower()
        
        positive_words = ['good', 'great', 'excellent', 'completed', 'success', 'working', 'fixed']
        negative_words = ['issue', 'problem', 'error', 'bug', 'failed', 'broken', 'blocked']
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return {'label': 'POSITIVE', 'score': min(0.9, 0.5 + (positive_count - negative_count) * 0.1)}
        elif negative_count > positive_count:
            return {'label': 'NEGATIVE', 'score': min(0.9, 0.5 + (negative_count - positive_count) * 0.1)}
        else:
            return {'label': 'NEUTRAL', 'score': 0.5}