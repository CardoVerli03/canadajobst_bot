import feedparser
import requests
import config
import database
import processor
import logging
import re

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
}

def fetch_rss_jobs():
    """Fetch jobs via Google News RSS to bypass direct site blocks"""
    logger.info("📡 Scanning via Google News Gateway (Plan B)...")
    
    try:
        response = requests.get(config.RSS_URL, headers=HEADERS, timeout=15)
        
        if response.status_code != 200:
            logger.error(f"❌ Gateway Blocked: Status {response.status_code}")
            return []
            
        feed = feedparser.parse(response.content)
        new_jobs = []

        for entry in feed.entries:
            # Google News ID huwa ni ndefu sana, tunachukua herufi 20 za mwanzo kama ID ya Turso
            raw_id = entry.get('id', entry.link)
            job_id = re.sub(r'\W+', '', raw_id)[:20] 
            
            if database.is_already_posted(job_id):
                continue
                
            title = entry.title
            link = entry.link
            # Google News mara nyingi haina summary ya maana, tunascan title
            summary = entry.get('summary', '')
            
            # Hatua ya Scoring
            score, category, reasons = processor.calculate_job_score(title, summary)
            
            # Kwa sababu Google News URL yetu imesha-filter "Sponsorship", 
            # hata score ya 2 (Category pekee) inatosha kupost.
            if score >= 2:
                new_jobs.append({
                    "job_id": job_id,
                    "title": title,
                    "link": link,
                    "category": category,
                    "reasons": reasons,
                    "score": score
                })
        
        logger.info(f"✅ Gateway Scan complete. Found {len(new_jobs)} jobs.")
        return new_jobs

    except Exception as e:
        logger.error(f"❌ Gateway Error: {e}")
    
    return []

def fetch_csv_jobs():
    """CSV disabled for Cloud stability"""
    return []
