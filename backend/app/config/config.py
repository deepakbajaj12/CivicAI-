import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/civicai')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    COHERE_API_KEY = os.getenv('COHERE_API_KEY')
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai')
    PORT = int(os.getenv('PORT', 5000))
    
    # Complaint categories
    CATEGORIES = ['Road', 'Water', 'Electricity', 'Sanitation', 'Safety', 'Other']
    
    # Urgency levels
    URGENCY_LEVELS = ['Low', 'Medium', 'High', 'Critical']
