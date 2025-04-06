# Emotion Analysis API Documentation

## Base URL
`http://localhost:8000`

## Authentication
All endpoints require JWT authentication via the `/login` endpoint.

## Endpoints

### 1. Emotion Analysis
**Endpoint**: `POST /analyze`  
**Description**: Analyze text for emotional content  
**Request Body**:
```json
{
  "text": "string (1-500 characters)"
}
```
**Response**:
```json
{
  "emotion": "string",
  "emotion_scores": {
    "anger": 0.0,
    "joy": 0.0,
    "sadness": 0.0,
    "fear": 0.0,
    "surprise": 0.0
  },
  "sentiment": {
    "polarity": 0.0,
    "subjectivity": 0.0
  }
}
```

### 2. Voice Analysis
**Endpoint**: `POST /voice-analyze`  
**Description**: Analyze voice for emotional content  
**Request Body**:
```json
{
  "audio_data": "base64 encoded audio",
  "sample_rate": 16000
}
```
**Response**:
```json
{
  "features": {
    "mfcc": [[...]],
    "pitch": 0.0,
    "intensity": 0.0,
    "speech_rate": 0.0
  },
  "predicted_emotion": "string",
  "sample_rate": 16000
}
```

### 3. Emotion Trends
**Endpoint**: `GET /analytics/emotion-trends`  
**Query Params**:
- `start_date`: ISO datetime (optional)
- `end_date`: ISO datetime (optional)  
**Response**:
```json
{
  "emotion_trends": [
    {
      "emotion": "string",
      "count": 0,
      "avg_score": 0.0
    }
  ]
}
```

### 4. Interaction Stats
**Endpoint**: `GET /analytics/interaction-stats`  
**Query Params**:
- `start_date`: ISO datetime (optional)
- `end_date`: ISO datetime (optional)  
**Response**:
```json
{
  "stats": {
    "total_interactions": [{"count": 0}],
    "by_hour": [{"_id": 0, "count": 0}],
    "common_issues": [{"_id": "string", "count": 0}]
  }
}
```

## Rate Limits
- Authentication endpoints: 5-10 requests/minute
- Analysis endpoints: 20-30 requests/minute
- Analytics endpoints: 30 requests/minute
