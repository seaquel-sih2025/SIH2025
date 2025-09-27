# Backend-AI Extension Integration

This document describes the integration between the backend worker and the AI extension for processing hazard reports.

## Overview

The integration allows the backend worker to automatically call AI extension functions directly for additional processing. When a new report is created in the backend, the worker extracts the hazard type and location information and calls the AI extension functions directly, which then processes relevant tweets and stores them in the same database.

## Architecture

```
Backend Worker → AI Extension Functions → AI Pipeline → Database
     ↓                    ↓                    ↓           ↓
  Report ID        Direct Function Call    Tweet Analysis   Reports Table
  Hazard Type         (No API)            NER/Sentiment    (Unified)
  Location                              Classification
  Coordinates
```

## Components

### 1. Backend Worker (`backend/worker.py`)

**Modified Functions:**
- `call_ai_extension()`: Calls AI extension functions directly
- `process_report_message()`: Now includes direct AI extension call

**Configuration:**
- `AI_EXTENSION_ENABLED`: Enable/disable AI extension (default: true)
- `AI_EXTENSION_PATH`: Path to AI extension directory (auto-configured)

**Direct Function Call:**
```python
call_ai_extension(
    report_id=report_id,
    hazard_type="flood",
    location="Kolkata",
    latitude=22.5726,
    longitude=88.3639
)
```

### 2. AI Extension Functions (`ai-extention/main.py`)

**Functions:**
- `run_pipeline_with_params()`: Main function called by backend
- `run_pipeline()`: Core processing pipeline

**Features:**
- Direct function calls (no API overhead)
- Synchronous processing
- Error handling and logging
- Database integration

### 3. AI Pipeline (`ai-extention/main.py`)

**Updated Functions:**
- `run_pipeline()`: Now accepts external parameters
- `run_pipeline_with_params()`: Wrapper for API calls

**Parameters:**
- `hazard_type`: Type of hazard to search for
- `location`: Geographic location for search
- `latitude/longitude`: Coordinates for geographic filtering
- `limit`: Number of tweets to process

## Setup Instructions

### 1. Install Dependencies

```bash
cd ai-extention
pip install -r requirements.txt
```

### 2. Configure Environment Variables

**Backend (.env):**
```env
AI_EXTENSION_ENABLED=true
```

**AI Extension (.env):**
```env
# Database connection (same as backend)
PGHOST=localhost
PGPORT=5432
PGDATABASE=your_database
PGUSER=your_user
PGPASSWORD=your_password

# Twitter API (if using)
TWITTER_BEARER_TOKEN=your_token
```

### 3. Start Services

**Start Backend Worker:**
```bash
cd backend
python worker.py
```

**Test AI Extension Directly:**
```bash
cd ai-extention
python test_direct_integration.py
```

## Usage Examples

### 1. Manual Testing

**Test Direct Function Integration:**
```bash
cd ai-extention
python test_direct_integration.py
```

**Run AI Pipeline Manually:**
```bash
cd ai-extention
python main.py
```

**Run with Custom Parameters:**
```bash
cd ai-extention
python -c "
from main import run_pipeline_with_params
result = run_pipeline_with_params(
    hazard_type='flood',
    location='Kolkata',
    latitude=22.5726,
    longitude=88.3639,
    limit=10
)
print(f'Processed {len(result)} tweets')
"
```

### 2. Backend Integration Testing

**Test Backend Worker:**
```bash
cd backend
python worker.py
```

**Simulate Report Processing:**
The backend worker will automatically call the AI extension when processing reports.

### 3. View Results

**View AI-Generated Reports:**
```bash
cd ai-extention
python view_db.py --type ai --limit 10
```

**View All Reports:**
```bash
cd ai-extention
python view_db.py --type all --limit 20
```

**View Statistics:**
```bash
cd ai-extention
python view_db.py --type stats
```

## Data Flow

1. **Report Creation**: User creates a report in the backend
2. **Worker Processing**: Backend worker processes the report
3. **AI Extension Call**: Worker sends data to AI extension API
4. **Tweet Processing**: AI extension searches for relevant tweets
5. **Analysis**: Tweets are analyzed for hazards and sentiment
6. **Database Storage**: Results are stored in the reports table
7. **Response**: AI extension responds with processing status

## Error Handling

- **Network Errors**: Retry logic with exponential backoff
- **API Errors**: Proper HTTP status codes and error messages
- **Processing Errors**: Graceful degradation and logging
- **Database Errors**: Transaction rollback and error reporting

## Monitoring

**Logs to Watch:**
- Backend worker: Report processing and AI extension calls
- AI Extension API: Incoming requests and processing status
- AI Pipeline: Tweet fetching and analysis results

**Key Metrics:**
- Number of reports processed
- Success/failure rates
- Processing times
- Database record counts

## Troubleshooting

### Common Issues

1. **AI Extension Not Responding**
   - Check if API server is running on port 8001
   - Verify network connectivity
   - Check logs for errors

2. **Database Connection Issues**
   - Verify database credentials
   - Check if reports table exists
   - Ensure proper permissions

3. **Twitter API Issues**
   - Verify API credentials
   - Check rate limits
   - Monitor API status

### Debug Commands

```bash
# Check AI Extension status
curl http://localhost:8001/status

# Test database connection
cd ai-extention
python -c "from pg_db import init_db; init_db(); print('DB OK')"

# Run integration test
cd ai-extention
python test_integration.py
```

## Configuration Options

### Backend Worker
- `AI_EXTENSION_URL`: AI extension API URL
- `AI_EXTENSION_ENABLED`: Enable/disable integration
- `RABBITMQ_URL`: Message queue URL

### AI Extension
- `DEFAULT_HAZARD_TYPE`: Default hazard type for searches
- `DEFAULT_LOCATION`: Default location for searches
- Database connection settings
- Twitter API credentials

## Performance Considerations

- **Async Processing**: AI extension processes requests asynchronously
- **Rate Limiting**: Twitter API rate limits are respected
- **Database Optimization**: Proper indexing on report fields
- **Memory Management**: Efficient processing of large datasets

## Security

- **API Authentication**: Consider adding API keys for production
- **Input Validation**: All inputs are validated and sanitized
- **Database Security**: Use proper connection credentials
- **Network Security**: Consider HTTPS for production deployment
