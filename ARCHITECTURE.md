# CivicAI - Project Architecture

## Overview

CivicAI is a full-stack application for intelligent civic complaint management using AI/ML for automatic categorization and urgency detection.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                     │
│                                                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  Complaint   │  │    Admin     │  │   Services   │  │
│  │     Form     │  │  Dashboard   │  │   (API)      │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP/REST API
┌────────────────────────▼────────────────────────────────┐
│                  Backend (Flask)                         │
│                                                           │
│  ┌──────────────────────────────────────────────────┐   │
│  │              Routes Layer                         │   │
│  │  /complaints, /statistics, /health               │   │
│  └─────────────────┬────────────────────────────────┘   │
│                    │                                      │
│  ┌─────────────────▼──────────┐  ┌─────────────────┐   │
│  │     Services Layer          │  │  Models Layer   │   │
│  │                             │  │                 │   │
│  │  ┌──────────────────────┐  │  │  ┌───────────┐ │   │
│  │  │   AI Service         │  │  │  │ Database  │ │   │
│  │  │  - OpenAI            │  │  │  │  Models   │ │   │
│  │  │  - Gemini            │  │  │  └───────────┘ │   │
│  │  │  - Cohere            │  │  │                 │   │
│  │  │  - Fallback Logic    │  │  │                 │   │
│  │  └──────────────────────┘  │  │                 │   │
│  └─────────────────────────────┘  └─────────────────┘   │
│                    │                        │             │
└────────────────────┼────────────────────────┼────────────┘
                     │                        │
                     ▼                        ▼
            ┌────────────────┐      ┌────────────────┐
            │   AI Providers │      │    MongoDB     │
            │  (External)    │      │   Database     │
            └────────────────┘      └────────────────┘
```

## Component Details

### Frontend (React + Tailwind CSS)

**Technology Stack:**
- React 18.2.0
- Vite 5.0.8 (Build tool)
- Tailwind CSS 3.4.0
- Axios 1.6.2 (HTTP client)

**Key Components:**

1. **ComplaintForm.jsx**
   - User input for complaint submission
   - Form validation
   - Real-time feedback with AI analysis results
   - Category and urgency display

2. **AdminDashboard.jsx**
   - Statistics cards (total, by category, by urgency)
   - Complaint table with pagination
   - Filtering by category, urgency, and status
   - Status update functionality
   - Delete functionality

3. **HomePage.jsx**
   - Main layout with navigation
   - Tab switching between form and dashboard
   - Header and footer components

4. **API Service (api.js)**
   - Centralized API calls
   - Error handling
   - Environment-based configuration

### Backend (Flask)

**Technology Stack:**
- Flask 3.0.0
- Flask-CORS 4.0.0
- PyMongo 4.6.1
- OpenAI 1.6.1
- Google Generative AI 0.3.2
- Cohere 4.37
- Gunicorn 21.2.0 (Production server)

**Module Structure:**

1. **app/routes/complaints.py**
   - REST API endpoints
   - Request validation
   - Response formatting
   - Error handling

2. **app/services/ai_service.py**
   - AI provider abstraction
   - Multi-provider support (OpenAI, Gemini, Cohere)
   - Prompt engineering
   - Response parsing
   - Fallback mechanism

3. **app/models/database.py**
   - MongoDB operations
   - CRUD functions
   - Statistics aggregation
   - Error handling

4. **app/config/config.py**
   - Environment variable management
   - Configuration constants
   - Category and urgency definitions

### Database (MongoDB)

**Collection: complaints**

Document Schema:
```javascript
{
  _id: ObjectId,
  citizen_name: String,
  citizen_email: String,
  location: String,
  description: String,
  category: String,  // Road, Water, Electricity, Sanitation, Safety, Other
  urgency: String,   // Low, Medium, High, Critical
  summary: String,
  reasoning: String,
  status: String,    // pending, in_progress, resolved, rejected
  created_at: DateTime,
  updated_at: DateTime
}
```

**Indexes:**
- `created_at` (descending) - for chronological sorting
- `category` - for filtering
- `urgency` - for filtering
- `status` - for filtering

## Data Flow

### Complaint Submission Flow

```
1. User fills form in React
   ↓
2. Frontend validates input
   ↓
3. POST request to /api/complaints
   ↓
4. Backend receives request
   ↓
5. AI Service analyzes complaint text
   ├─→ Try primary AI provider (OpenAI/Gemini/Cohere)
   │   ├─→ Success: Parse JSON response
   │   └─→ Failure: Use fallback keyword analysis
   ↓
6. Create complaint document with analysis
   ↓
7. Save to MongoDB
   ↓
8. Return complete complaint object
   ↓
9. Frontend displays analysis results
```

### Admin Dashboard Flow

```
1. User opens admin dashboard
   ↓
2. Frontend requests data
   ├─→ GET /api/complaints (with filters)
   └─→ GET /api/statistics
   ↓
3. Backend queries MongoDB
   ↓
4. Aggregate and format data
   ↓
5. Return JSON responses
   ↓
6. Frontend renders UI
   ├─→ Statistics cards
   ├─→ Filters
   └─→ Complaint table
```

## AI Analysis Pipeline

### 1. Prompt Construction
```
System: Civic complaint analyzer
User: Analyze complaint + guidelines
```

### 2. AI Processing
- Send to configured provider (OpenAI/Gemini/Cohere)
- Wait for response (max 10 seconds)
- Handle provider-specific response format

### 3. Response Parsing
```
Expected JSON:
{
  "category": "Road",
  "urgency": "High",
  "summary": "Brief summary",
  "reasoning": "Why this classification"
}
```

### 4. Validation
- Verify category is in allowed list
- Verify urgency is in allowed list
- Sanitize text fields
- Handle malformed responses

### 5. Fallback Logic
If AI fails:
- Keyword matching for category
- Keyword matching for urgency
- Generate basic summary (first 100 chars)
- Generic reasoning message

## Security Considerations

1. **Error Handling**
   - Generic error messages for users
   - Detailed logs for debugging
   - No stack traces in production

2. **Input Validation**
   - Required field checks
   - Data type validation
   - Length limits

3. **Environment Configuration**
   - Secrets in .env files
   - Debug mode controlled by environment
   - Production-ready defaults

4. **CORS**
   - Configured for cross-origin requests
   - Should be restricted in production

## Scalability Considerations

1. **Database**
   - MongoDB sharding for horizontal scaling
   - Indexes for query performance
   - Connection pooling

2. **Backend**
   - Gunicorn with multiple workers
   - Stateless design for load balancing
   - Caching for statistics

3. **Frontend**
   - Static file serving via CDN
   - Code splitting
   - Lazy loading

4. **AI Service**
   - Request queuing for rate limiting
   - Caching for duplicate complaints
   - Fallback for high availability

## Deployment Options

### Option 1: Docker Compose (Recommended for Development)
```bash
docker-compose up
```

### Option 2: Kubernetes (Production)
- Separate deployments for frontend, backend, MongoDB
- Horizontal pod autoscaling
- Ingress controller for routing

### Option 3: Traditional (Manual)
- Nginx for frontend static files
- Gunicorn + systemd for backend
- MongoDB as a service

## Monitoring and Logging

Recommended additions for production:

1. **Application Monitoring**
   - Request logging
   - Error tracking (e.g., Sentry)
   - Performance metrics

2. **Database Monitoring**
   - Query performance
   - Connection pool stats
   - Storage metrics

3. **AI Service Monitoring**
   - API call success/failure rates
   - Response times
   - Fallback usage statistics

## Future Enhancements

1. **Authentication & Authorization**
   - User registration/login
   - Role-based access control
   - JWT tokens

2. **Real-time Updates**
   - WebSocket for live dashboard updates
   - Push notifications

3. **Advanced Analytics**
   - Trend analysis
   - Geospatial clustering
   - Predictive maintenance

4. **Integration**
   - SMS/Email notifications
   - Third-party ticketing systems
   - GIS mapping integration

5. **Mobile Apps**
   - React Native apps
   - Location-based complaints
   - Photo attachments
