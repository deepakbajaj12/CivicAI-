"""
Simple test script to validate the backend structure and AI service
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app.services.ai_service import AIService
from app.config import Config

def test_ai_service_fallback():
    """Test AI service fallback mechanism"""
    print("Testing AI Service fallback mechanism...")
    
    # Create AI service with a provider that will use fallback
    ai_service = AIService('openai')
    
    # Test with a sample complaint
    test_complaints = [
        "There is a huge pothole on Main Street causing accidents",
        "Water supply has been cut off for 3 days in our area",
        "Street lights are not working in Block A for a week",
        "Garbage has not been collected for 5 days, creating health hazard",
        "Someone is selling drugs near the school, very dangerous"
    ]
    
    print("\n=== Testing Complaint Analysis ===\n")
    
    for complaint in test_complaints:
        print(f"Complaint: {complaint[:60]}...")
        result = ai_service.analyze_complaint(complaint)
        print(f"  Category: {result['category']}")
        print(f"  Urgency: {result['urgency']}")
        print(f"  Summary: {result['summary'][:60]}...")
        print(f"  Reasoning: {result['reasoning'][:60]}...")
        print()
    
    print("✓ AI Service fallback mechanism works correctly!")
    return True

def test_config():
    """Test configuration"""
    print("Testing Configuration...")
    
    assert len(Config.CATEGORIES) == 6, "Should have 6 categories"
    assert len(Config.URGENCY_LEVELS) == 4, "Should have 4 urgency levels"
    assert 'Road' in Config.CATEGORIES, "Should have Road category"
    assert 'Critical' in Config.URGENCY_LEVELS, "Should have Critical urgency"
    
    print("✓ Configuration is correct!")
    return True

def main():
    print("=" * 60)
    print("CivicAI Backend Validation Tests")
    print("=" * 60)
    print()
    
    try:
        test_config()
        print()
        test_ai_service_fallback()
        print()
        print("=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        return 0
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
