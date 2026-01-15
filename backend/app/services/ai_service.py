import json
from app.config import Config

class AIService:
    """AI Service for analyzing complaints"""
    
    def __init__(self, provider='openai'):
        self.provider = provider.lower()
        self._init_client()
    
    def _init_client(self):
        """Initialize AI client based on provider"""
        if self.provider == 'openai':
            # Client will be created in the analyze method
            pass
        elif self.provider == 'gemini':
            import google.generativeai as genai
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.client = genai
        elif self.provider == 'cohere':
            import cohere
            self.client = cohere.Client(Config.COHERE_API_KEY)
    
    def analyze_complaint(self, complaint_text):
        """
        Analyze complaint text to classify category, detect urgency, 
        generate summary and reasoning
        """
        prompt = self._build_analysis_prompt(complaint_text)
        
        try:
            if self.provider == 'openai':
                response = self._analyze_with_openai(prompt)
            elif self.provider == 'gemini':
                response = self._analyze_with_gemini(prompt)
            elif self.provider == 'cohere':
                response = self._analyze_with_cohere(prompt)
            else:
                raise ValueError(f"Unsupported AI provider: {self.provider}")
            
            return self._parse_response(response)
        except Exception as e:
            # Fallback to basic analysis if AI fails
            return self._fallback_analysis(complaint_text, str(e))
    
    def _build_analysis_prompt(self, complaint_text):
        """Build the analysis prompt"""
        return f"""You are an AI assistant for a Smart City Complaint Intelligence System. Analyze the following civic complaint and provide a structured response.

Complaint: "{complaint_text}"

Analyze this complaint and provide a JSON response with the following structure:
{{
    "category": "<one of: Road, Water, Electricity, Sanitation, Safety, Other>",
    "urgency": "<one of: Low, Medium, High, Critical>",
    "summary": "<a brief 1-2 sentence summary of the complaint>",
    "reasoning": "<explain why you chose this category and urgency level>"
}}

Category Guidelines:
- Road: potholes, traffic, street lights, road damage, construction issues
- Water: water supply, leakage, quality, drainage, sewage
- Electricity: power outage, billing, streetlights, transformers
- Sanitation: garbage collection, cleanliness, waste management
- Safety: crime, accidents, public safety concerns, violence
- Other: complaints that don't fit the above categories

Urgency Guidelines:
- Low: minor issues, no immediate impact
- Medium: moderate issues, some inconvenience
- High: significant issues, affecting daily life
- Critical: emergency situations, immediate danger, widespread impact

Provide ONLY the JSON response, no additional text."""
    
    def _analyze_with_openai(self, prompt):
        """Analyze using OpenAI API"""
        from openai import OpenAI
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a civic complaint analyzer. Always respond with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content
    
    def _analyze_with_gemini(self, prompt):
        """Analyze using Gemini API"""
        model = self.client.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    
    def _analyze_with_cohere(self, prompt):
        """Analyze using Cohere API"""
        response = self.client.generate(
            prompt=prompt,
            max_tokens=500,
            temperature=0.3
        )
        return response.generations[0].text
    
    def _parse_response(self, response):
        """Parse AI response to extract structured data"""
        try:
            # Try to extract JSON from response
            response = response.strip()
            
            # Remove markdown code blocks if present
            if response.startswith('```json'):
                response = response[7:]
            if response.startswith('```'):
                response = response[3:]
            if response.endswith('```'):
                response = response[:-3]
            
            response = response.strip()
            
            # Parse JSON
            data = json.loads(response)
            
            # Validate and normalize fields
            category = data.get('category', 'Other')
            if category not in Config.CATEGORIES:
                category = 'Other'
            
            urgency = data.get('urgency', 'Medium')
            if urgency not in Config.URGENCY_LEVELS:
                urgency = 'Medium'
            
            return {
                'category': category,
                'urgency': urgency,
                'summary': data.get('summary', 'Civic complaint submitted'),
                'reasoning': data.get('reasoning', 'Analyzed based on content')
            }
        except json.JSONDecodeError:
            # If JSON parsing fails, try to extract information from text
            return self._extract_from_text(response)
    
    def _extract_from_text(self, text):
        """Extract information from non-JSON text response"""
        text_lower = text.lower()
        
        # Try to find category
        category = 'Other'
        for cat in Config.CATEGORIES:
            if cat.lower() in text_lower:
                category = cat
                break
        
        # Try to find urgency
        urgency = 'Medium'
        for urg in Config.URGENCY_LEVELS:
            if urg.lower() in text_lower:
                urgency = urg
                break
        
        return {
            'category': category,
            'urgency': urgency,
            'summary': 'Civic complaint submitted',
            'reasoning': text[:200] if text else 'Unable to parse AI response'
        }
    
    def _fallback_analysis(self, complaint_text, error_msg):
        """Provide fallback analysis if AI service fails"""
        text_lower = complaint_text.lower()
        
        # Simple keyword-based category detection
        category = 'Other'
        if any(word in text_lower for word in ['road', 'pothole', 'traffic', 'street']):
            category = 'Road'
        elif any(word in text_lower for word in ['water', 'leak', 'drain', 'sewage']):
            category = 'Water'
        elif any(word in text_lower for word in ['electric', 'power', 'light', 'outage']):
            category = 'Electricity'
        elif any(word in text_lower for word in ['garbage', 'trash', 'clean', 'waste']):
            category = 'Sanitation'
        elif any(word in text_lower for word in ['danger', 'crime', 'safe', 'accident']):
            category = 'Safety'
        
        # Simple urgency detection
        urgency = 'Low'
        if any(word in text_lower for word in ['urgent', 'emergency', 'critical', 'immediate', 'danger']):
            urgency = 'Critical'
        elif any(word in text_lower for word in ['serious', 'important', 'severe']):
            urgency = 'High'
        elif any(word in text_lower for word in ['need', 'problem', 'issue']):
            urgency = 'Medium'
        
        return {
            'category': category,
            'urgency': urgency,
            'summary': complaint_text[:100] + ('...' if len(complaint_text) > 100 else ''),
            'reasoning': f'Fallback analysis (AI service unavailable: {error_msg})'
        }
