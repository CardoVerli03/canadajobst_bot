import feedparser
import requests
import config
import database
import processor
import logging

logger = logging.getLogger(__name__)

# Fake headers - Tunajifanya sisi ni Chrome Browser ya kawaida
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'application/rss+xml, application/xml, text/xml, */*',
    'Accept-Language': 'en-US,en;q=0.9',
}

def fetch_rss_jobs():
    """Fetch and filter live updates from Canada Job Bank RSS"""
    logger.info("📡 Scanning Canada Job Bank RSS for new openings...")
    
    try:
        # Tunatumia timeout fupi kuzuia bot isikwame internet ikiwa slow
        response = requests.get(config.RSS_URL, headers=HEADERS, timeout=15)
        
        if response.status_code != 200:
            logger.error(f"❌ Connection Blocked: Status {response.status_code}")
            return []
            
        feed = feedparser.parse(response.content)
        new_jobs = []

        if not feed.entries:
            logger.info("ℹ️ No new entries found in this cycle.")
            return []

        for entry in feed.entries:
            # Safisha Job ID toka kwenye link (mfano: /jobposting/41234567)
            job_id = entry.link.split('/')[-1] if '/' in entry.link else entry.id
            
            # Hatua ya kwanza: Je, ishapostiwa? (Chuja duplicate)
            if database.is_already_posted(job_id):
                continue
                
            title = entry.title
            link = entry.link
            summary = entry.summary if 'summary' in entry else ""
            
            # Hatua ya pili: Scoring Engine (Ni ya sponsorship?)
            score, category, reasons = processor.calculate_job_score(title, summary)
            
            if processor.is_job_worthy(score):
                new_jobs.append({
                    "job_id": job_id,
                    "title": title,
                    "link": link,
                    "category": category,
                    "reasons": reasons,
                    "score": score
                })
        
        logger.info(f"✅ Scan complete. Found {len(new_jobs)} worthy jobs.")
        return new_jobs

    except requests.exceptions.Timeout:
        logger.error("❌ RSS Fetch Timeout - Site is slow or connection lagging.")
    except Exception as e:
        logger.error(f"❌ RSS Error: {e}")
    
    return []

# CSV function imezimwa ili kuzuia RAM overload kule Render
def fetch_csv_jobs():
    """CSV functionality disabled to preserve Cloud resources"""
    return []
