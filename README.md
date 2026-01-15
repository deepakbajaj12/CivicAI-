# CivicAI - Smart City Complaint Intelligence System

A hackathon-ready GenAI-powered application that intelligently analyzes and categorizes civic complaints using AI.

## 🚀 Features

- **Intelligent Analysis**: Automatically classifies complaints into categories (Road, Water, Electricity, Sanitation, Safety, Other)
- **Urgency Detection**: AI-powered urgency level detection (Low, Medium, High, Critical)
- **Smart Summarization**: Generates concise summaries and reasoning for each complaint
- **Admin Dashboard**: Real-time statistics and complaint management
- **Modern UI**: Responsive React frontend with Tailwind CSS
- **REST API**: Clean, modular Flask backend
- **Multi-AI Support**: Works with OpenAI, Google Gemini, or Cohere

## 🛠️ Tech Stack

### Backend
- **Flask** - Python web framework
- **MongoDB** - NoSQL database
- **OpenAI/Gemini/Cohere** - AI/ML services
- **Python 3.8+**

### Frontend
- **React 18** - UI library
- **Tailwind CSS** - Styling
- **Vite** - Build tool
- **Axios** - HTTP client

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- MongoDB (local or cloud)
- API key for OpenAI, Google Gemini, or Cohere

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/deepakbajaj12/CivicAI-.git
cd CivicAI-
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env and add your configuration:
# - MongoDB connection string
# - AI API keys (OpenAI/Gemini/Cohere)
# - Choose AI provider (openai/gemini/cohere)
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

## 🚀 Running the Application

### Start Backend Server

```bash
cd backend
python run.py
```

Backend will run on `http://localhost:5000`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

Frontend will run on `http://localhost:3000`

## 📡 API Endpoints

### Complaints

- `POST /api/complaints` - Submit a new complaint
- `GET /api/complaints` - Get all complaints (with pagination & filters)
- `GET /api/complaints/:id` - Get a specific complaint
- `PUT /api/complaints/:id` - Update complaint status
- `DELETE /api/complaints/:id` - Delete a complaint

### Admin

- `GET /api/statistics` - Get complaint statistics
- `GET /api/health` - Health check

### Query Parameters (GET /api/complaints)

- `page` - Page number (default: 1)
- `limit` - Results per page (default: 10)
- `category` - Filter by category
- `urgency` - Filter by urgency
- `status` - Filter by status

## 📊 Example API Usage

### Submit a Complaint

```bash
curl -X POST http://localhost:5000/api/complaints \
  -H "Content-Type: application/json" \
  -d '{
    "citizen_name": "John Doe",
    "citizen_email": "john@example.com",
    "location": "Main Street, Block A",
    "description": "There is a large pothole on Main Street causing traffic issues"
  }'
```

### Get Statistics

```bash
curl http://localhost:5000/api/statistics
```

## 🎨 UI Features

### Citizen Interface
- Simple complaint submission form
- Real-time AI analysis feedback
- Category and urgency display
- Summary and reasoning explanation

### Admin Dashboard
- Statistics overview (total complaints, by category, by urgency)
- Complaint list with filters
- Status management
- Delete functionality
- Responsive design

## 🔐 Environment Variables

### Backend (.env)

```env
MONGO_URI=mongodb://localhost:27017/civicai
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
COHERE_API_KEY=your_cohere_api_key_here
AI_PROVIDER=openai  # or gemini or cohere
FLASK_ENV=development
PORT=5000
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:5000/api
```

## 🏗️ Project Structure

```
CivicAI-/
├── backend/
│   ├── app/
│   │   ├── config/          # Configuration
│   │   ├── models/          # Database models
│   │   ├── routes/          # API routes
│   │   └── services/        # AI service
│   ├── requirements.txt
│   ├── run.py
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   └── services/        # API service
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🚢 Production Deployment

### Backend

```bash
# Use gunicorn for production
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Frontend

```bash
# Build for production
npm run build

# Serve the dist folder with a web server
```

## 🧪 Testing

### Test Backend API

```bash
cd backend
python -m pytest
```

### Test Frontend

```bash
cd frontend
npm test
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI, Google Gemini, and Cohere for AI services
- Flask and React communities
- MongoDB team

## 📞 Support

For issues and questions, please open an issue on GitHub.

---

Built with ❤️ for smarter cities
