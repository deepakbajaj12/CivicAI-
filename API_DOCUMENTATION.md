# CivicAI API Documentation

## Base URL
```
http://localhost:5000/api
```

## Endpoints

### Health Check
**GET** `/health`

Check if the API is running.

**Response:**
```json
{
  "success": true,
  "message": "CivicAI API is running",
  "ai_provider": "openai"
}
```

---

### Submit Complaint
**POST** `/complaints`

Submit a new civic complaint for AI analysis.

**Request Body:**
```json
{
  "citizen_name": "John Doe",
  "citizen_email": "john@example.com",
  "location": "Main Street, Block A",
  "description": "There is a large pothole causing accidents"
}
```

**Response:**
```json
{
  "success": true,
  "complaint": {
    "_id": "6968ac1bc41631a3f84ec50b",
    "citizen_name": "John Doe",
    "citizen_email": "john@example.com",
    "location": "Main Street, Block A",
    "description": "There is a large pothole causing accidents",
    "category": "Road",
    "urgency": "Critical",
    "summary": "Large pothole on Main Street causing accidents",
    "reasoning": "Classified as Road category due to pothole mention. Critical urgency due to accident risk.",
    "status": "pending",
    "created_at": "Thu, 15 Jan 2026 08:58:03 GMT",
    "updated_at": "Thu, 15 Jan 2026 08:58:03 GMT"
  },
  "message": "Complaint submitted successfully"
}
```

---

### Get All Complaints
**GET** `/complaints`

Retrieve all complaints with pagination and filtering.

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Results per page (default: 10, max: 100)
- `category` (optional): Filter by category (Road, Water, Electricity, Sanitation, Safety, Other)
- `urgency` (optional): Filter by urgency (Low, Medium, High, Critical)
- `status` (optional): Filter by status (pending, in_progress, resolved, rejected)

**Example:**
```
GET /complaints?page=1&limit=10&category=Road&urgency=Critical
```

**Response:**
```json
{
  "success": true,
  "complaints": [
    {
      "_id": "6968ac1bc41631a3f84ec50b",
      "citizen_name": "John Doe",
      "category": "Road",
      "urgency": "Critical",
      ...
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 5,
    "pages": 1
  }
}
```

---

### Get Single Complaint
**GET** `/complaints/:id`

Get details of a specific complaint.

**Response:**
```json
{
  "success": true,
  "complaint": {
    "_id": "6968ac1bc41631a3f84ec50b",
    ...
  }
}
```

---

### Update Complaint
**PUT** `/complaints/:id`

Update a complaint (admin only). Currently supports status updates.

**Request Body:**
```json
{
  "status": "in_progress"
}
```

**Valid Status Values:**
- `pending`
- `in_progress`
- `resolved`
- `rejected`

**Response:**
```json
{
  "success": true,
  "complaint": {
    "_id": "6968ac1bc41631a3f84ec50b",
    "status": "in_progress",
    ...
  },
  "message": "Complaint updated successfully"
}
```

---

### Delete Complaint
**DELETE** `/complaints/:id`

Delete a complaint (admin only).

**Response:**
```json
{
  "success": true,
  "message": "Complaint deleted successfully"
}
```

---

### Get Statistics
**GET** `/statistics`

Get complaint statistics for the admin dashboard.

**Response:**
```json
{
  "success": true,
  "statistics": {
    "total": 25,
    "by_category": {
      "Road": 10,
      "Water": 5,
      "Electricity": 3,
      "Sanitation": 4,
      "Safety": 2,
      "Other": 1
    },
    "by_urgency": {
      "Low": 8,
      "Medium": 7,
      "High": 5,
      "Critical": 5
    }
  }
}
```

---

## Error Responses

All endpoints return consistent error responses:

**400 Bad Request:**
```json
{
  "error": "Description is required"
}
```

**404 Not Found:**
```json
{
  "error": "Complaint not found"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Failed to process complaint"
}
```

---

## Categories

The system classifies complaints into these categories:

- **Road**: Potholes, traffic, street lights, road damage, construction issues
- **Water**: Water supply, leakage, quality, drainage, sewage
- **Electricity**: Power outage, billing, streetlights, transformers
- **Sanitation**: Garbage collection, cleanliness, waste management
- **Safety**: Crime, accidents, public safety concerns, violence
- **Other**: Complaints that don't fit the above categories

---

## Urgency Levels

The system assigns urgency levels based on content analysis:

- **Low**: Minor issues, no immediate impact
- **Medium**: Moderate issues, some inconvenience
- **High**: Significant issues, affecting daily life
- **Critical**: Emergency situations, immediate danger, widespread impact

---

## AI Analysis

When a complaint is submitted, the system:

1. Analyzes the description using AI (OpenAI/Gemini/Cohere)
2. Classifies it into one of 6 categories
3. Determines urgency level (Low to Critical)
4. Generates a concise summary
5. Provides reasoning for the classification

If AI service is unavailable, the system uses a keyword-based fallback algorithm to ensure uninterrupted service.

---

## Rate Limiting

Currently, there are no rate limits. For production deployment, consider implementing rate limiting based on your requirements.

---

## Authentication

The current version does not implement authentication. For production use, implement:
- JWT-based authentication
- Role-based access control (citizen vs admin)
- API keys for external integrations
