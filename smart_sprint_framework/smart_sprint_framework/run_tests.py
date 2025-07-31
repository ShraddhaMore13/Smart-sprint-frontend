import unittest
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import test modules
from tests.test_smart_sprint_system import TestSmartSprintSystem
from tests.test_nlp_pipeline import TestNLPPipeline
from tests.test_developer_recommendation import TestDeveloperRecommendationEngine

def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestSmartSprintSystem))
    suite.addTests(loader.loadTestsFromTestCase(TestNLPPipeline))
    suite.addTests(loader.loadTestsFromTestCase(TestDeveloperRecommendationEngine))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return success status
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)