from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List, Dict, Any
import psycopg2
from psycopg2.extras import RealDictCursor
import os

from app.db.session import get_db

router = APIRouter()

def get_ai_db_connection():
    """Get connection to the AI database (where alerts and scraped_data tables are stored)"""
    # Use the same database as the AI scrapers
    return psycopg2.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432'),
        database=os.getenv('DB_NAME', 'pravaah_db'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'atharv')
    )

@router.get("/alerts", response_model=List[Dict[str, Any]], summary="Get recent alerts from AI scrapers")
async def get_alerts(limit: int = 20):
    """
    Fetch recent alerts from the alerts table (populated by YouTube scraper)
    """
    try:
        conn = get_ai_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
        SELECT 
            event_type as title,
            sentiment,
            urgency,
            location,
            video_url as link,
            video_created_at as created_at,
            'youtube' as source
        FROM alerts 
        ORDER BY video_created_at DESC 
        LIMIT %s
        """
        
        cur.execute(query, (limit,))
        alerts = cur.fetchall()
        
        # Convert to list of dicts
        result = []
        for alert in alerts:
            alert_dict = dict(alert)
            # Ensure all required fields are present
            alert_dict['title'] = alert_dict.get('title') or 'Ocean Alert'
            alert_dict['sentiment'] = alert_dict.get('sentiment') or 'neutral'
            alert_dict['urgency'] = alert_dict.get('urgency') or 'medium'
            alert_dict['location'] = alert_dict.get('location') or 'Unknown'
            alert_dict['link'] = alert_dict.get('link') or '#'
            alert_dict['created_at'] = alert_dict.get('created_at')
            alert_dict['source'] = alert_dict.get('source') or 'youtube'
            result.append(alert_dict)
        
        cur.close()
        conn.close()
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch alerts: {str(e)}")

@router.get("/scraped-data", response_model=List[Dict[str, Any]], summary="Get recent scraped data from AI scrapers")
async def get_scraped_data(limit: int = 20):
    """
    Fetch recent scraped data from the scraped_data table (populated by Twitter scraper)
    """
    try:
        conn = get_ai_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
        SELECT 
            event_type as title,
            sentiment,
            urgency,
            location,
            source_url as link,
            source_created_at as created_at,
            'twitter' as source
        FROM scraped_data 
        ORDER BY source_created_at DESC 
        LIMIT %s
        """
        
        cur.execute(query, (limit,))
        scraped_data = cur.fetchall()
        
        # Convert to list of dicts
        result = []
        for data in scraped_data:
            data_dict = dict(data)
            # Ensure all required fields are present
            data_dict['title'] = data_dict.get('title') or 'Social Media Alert'
            data_dict['sentiment'] = data_dict.get('sentiment') or 'neutral'
            data_dict['urgency'] = data_dict.get('urgency') or 'medium'
            data_dict['location'] = data_dict.get('location') or 'Unknown'
            data_dict['link'] = data_dict.get('link') or '#'
            data_dict['created_at'] = data_dict.get('created_at')
            data_dict['source'] = data_dict.get('source') or 'twitter'
            result.append(data_dict)
        
        cur.close()
        conn.close()
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch scraped data: {str(e)}")

@router.get("/combined-feed", response_model=List[Dict[str, Any]], summary="Get combined feed from all AI sources")
async def get_combined_feed(limit: int = 30):
    """
    Fetch combined feed from both alerts and scraped_data tables
    """
    try:
        conn = get_ai_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        query = """
        (
            SELECT 
                event_type as title,
                sentiment,
                urgency,
                location,
                video_url as link,
                video_created_at as created_at,
                'youtube' as source
            FROM alerts 
            WHERE video_created_at IS NOT NULL
        )
        UNION ALL
        (
            SELECT 
                event_type as title,
                sentiment,
                urgency,
                location,
                source_url as link,
                source_created_at as created_at,
                'twitter' as source
            FROM scraped_data 
            WHERE source_created_at IS NOT NULL
        )
        ORDER BY created_at DESC 
        LIMIT %s
        """
        
        cur.execute(query, (limit,))
        feed_items = cur.fetchall()
        
        # Convert to list of dicts
        result = []
        for item in feed_items:
            item_dict = dict(item)
            # Ensure all required fields are present
            item_dict['title'] = item_dict.get('title') or 'Ocean Alert'
            item_dict['sentiment'] = item_dict.get('sentiment') or 'neutral'
            item_dict['urgency'] = item_dict.get('urgency') or 'medium'
            item_dict['location'] = item_dict.get('location') or 'Unknown'
            item_dict['link'] = item_dict.get('link') or '#'
            item_dict['created_at'] = item_dict.get('created_at')
            item_dict['source'] = item_dict.get('source') or 'unknown'
            result.append(item_dict)
        
        cur.close()
        conn.close()
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch combined feed: {str(e)}")
