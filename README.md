# Content Moderation API

A FastAPI-based content moderation service that uses AI to classify text and images for toxic content, spam, harassment, and safe content. The service provides REST endpoints for content analysis and stores results in a PostgreSQL database.

## Features

- **Text Content Moderation**: Analyze text content for inappropriate material
- **Image Content Moderation**: Analyze uploaded images for inappropriate content
- **AI-Powered Classification**: Uses Google's Gemini AI model for content analysis
- **Database Storage**: Stores moderation requests and results in PostgreSQL
- **User Analytics**: Get moderation statistics by user email
- **Docker Support**: Fully containerized application

## Tech Stack

- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI Model**: Google Gemini 1.5 Flash
- **Containerization**: Docker
- **File Handling**: Content hashing with SHA256

## Project Structure

```
backend/
├── config/
│   └── db.py                    # Database configuration and connection
├── models/
│   └── moderation.py           # SQLAlchemy models for database tables
├── routes/
│   └── classificationRoutes.py # API endpoints for moderation
├── schema/
│   └── moderationSchema.py     # Pydantic models for request/response
├── utils/
│   ├── hash_content.py         # Content hashing utilities
│   └── text_image_classification.py # AI model integration
├── server.py                   # FastAPI application entry point
├── Dockerfile                  # Docker container configuration
└── requirements.txt           # Python dependencies
```

## API Endpoints

### 1. Health Check
```
GET /
```
Returns service status.

### 2. Text Moderation
```
POST /api/text_call
```
**Request Body:**
```json
{
  "text": "Content to moderate",
  "email": "user@example.com"
}
```

**Response:**
```json
{
  "status": "success",
  "result": {
    "classification": "safe|toxic|spam|harassment",
    "confidence": 0.95,
    "reasoning": "Explanation of classification",
    "llm_response": "Full AI model response"
  }
}
```

### 3. Image Moderation
```
POST /api/image_call
```
**Form Data:**
- `email`: User email (string)
- `file`: Image file (multipart/form-data)

**Response:**
```json
{
  "status": "success",
  "result": {
    "classification": "safe|toxic|spam|harassment",
    "confidence": 0.95,
    "reasoning": "Explanation of classification",
    "llm_response": "Full AI model response"
  }
}
```

### 4. User Summary
```
GET /api/summary?user=user@example.com
```
**Response:**
```json
{
  "total_request": 15,
  "by_classification": {
    "safe": 12,
    "toxic": 2,
    "spam": 1,
    "harassment": 0
  }
}
```

## Database Schema

### ModerationRequest Table
- `id`: Primary key
- `content_type`: "text" or "image"
- `content_hash`: SHA256 hash of content
- `email`: User email
- `status`: "pending", "processing", or "completed"
- `created_time`: Timestamp

### ModerationResult Table
- `id`: Primary key
- `request_id`: Foreign key to ModerationRequest
- `classification`: AI classification result
- `confidence`: Confidence score
- `reasoning`: AI reasoning
- `llm_response`: Full AI response

## Setup and Installation

### Prerequisites
- Docker and Docker Compose
- Python 3.12+ (for local development)
- PostgreSQL database
- Google AI API key for Gemini

### Environment Variables
Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/moderation_db
GOOGLE_AI_API_KEY=your_gemini_api_key_here
```

### Docker Setup (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/UB2002/Content_Moderation_LLM
cd backend
```

2. **Build and run with Docker**
```bash
docker-compose up --build
```


### Local Development Setup

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables in env**
```bash
    DATABASE_URL="postgresql://username:password@localhost:5432/moderation_db"
    GOOGLE_AI_API_KEY="your_api_key"
```

3. **Run the application**
```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

## Usage Examples

import the api_call.json file in postman and use it for calling the api(testing the api)

## Content Classification

The AI model classifies content into four categories:

- **safe**: Content is appropriate and safe
- **toxic**: Content contains toxic or harmful material
- **spam**: Content appears to be spam
- **harassment**: Content contains harassment or bullying

Each classification includes:
- Confidence score (0.0 to 1.0)
- Reasoning explanation
- Full AI model response

