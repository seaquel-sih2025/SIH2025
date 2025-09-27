# View Database Usage Guide

The `view_db.py` script has been updated to work with the new `reports` table structure. Here are the available commands:

## Basic Usage

### View AI-Generated Reports (Default)
```bash
python view_db.py
```
or
```bash
python view_db.py --type ai --limit 20
```

### View All Reports (AI + User Generated)
```bash
python view_db.py --type all --limit 50
```

### View Database Statistics
```bash
python view_db.py --type stats
```

## Command Line Options

- `--limit N`: Maximum number of rows to display (default: 50)
- `--type {ai,all,stats}`: Type of data to view
  - `ai`: AI-generated reports only (those with tweet_url)
  - `all`: All reports (both AI and user-generated)
  - `stats`: Database statistics

## Examples

### View last 10 AI-generated reports
```bash
python view_db.py --type ai --limit 10
```

### View all reports with a limit of 100
```bash
python view_db.py --type all --limit 100
```

### Get database statistics
```bash
python view_db.py --type stats
```

## Output Format

The script outputs JSON data with the following fields for reports:

**AI-Generated Reports:**
- `id`: UUID of the report
- `tweet_url`: URL of the original tweet
- `user_hazard_type`: Type of hazard detected
- `user_city`: City where the hazard was detected
- `user_description`: Description of the hazard
- `sentiment_label`: Sentiment analysis result
- `sentiment_score`: Confidence score for sentiment
- `tweet_date`: Date of the tweet
- `tweet_time`: Time of the tweet
- `latitude`, `longitude`: Geographic coordinates
- `status`: Report status (under_verification, verified, rejected)
- `final_confidence_score`: Final confidence score
- `created_at`: When the report was created
- `inserted_at`: When the report was inserted by AI

**Statistics Output:**
- `total_reports`: Total number of reports
- `ai_generated_reports`: Number of AI-generated reports
- `user_generated_reports`: Number of user-generated reports
- `under_verification`: Reports under verification
- `verified`: Verified reports
- `rejected`: Rejected reports
