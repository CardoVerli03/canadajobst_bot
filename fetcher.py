import feedparser
import requests
import csv
import io
import config
import database
import processor
import logging

logger = logging.getLogger(__name__)

# Fake headers to avoid being blocked by Canada Job Bank
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def fetch_rss_jobs():
    """Fetch live updates from RSS feed with headers and error handling"""
    logger.info("📡 Fetching jobs from RSS...")
    try:
        # Fetching with requests first to use headers, then parsing with feedparser
        response = requests.get(config.RSS_URL, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            logger.error(f"❌ RSS Error: Status {response.status_code}")
            return []
            
        feed = feedparser.parse(response.content)
        new_jobs = []

        for entry in feed.entries:
            # Extract Job ID safely
            job_id = entry.id.split('/')[-1] if 'id' in entry else entry.link.split('/')[-1]
            
            if database.is_already_posted(job_id):
                continue
                
            title = entry.title
            link = entry.link
            description = entry.summary if 'summary' in entry else ""
            
            score, category, reasons = processor.calculate_job_score(title, description)
            
            if processor.is_job_worthy(score):
                new_jobs.append({
                    "job_id": job_id,
                    "title": title,
                    "link": link,
                    "category": category,
                    "reasons": reasons,
                    "score": score
                })
        
        return new_jobs
    except Exception as e:
        logger.error(f"❌ RSS Critical Failure: {e}")
        return []

def fetch_csv_jobs():
    """Download and process the Daily CSV dataset with memory efficiency"""
    logger.info("📥 Downloading Daily CSV Dataset...")
    try:
        response = requests.get(config.CSV_URL, headers=HEADERS, timeout=30)
        if response.status_code != 200:
            logger.error("❌ Failed to download CSV")
            return []

        new_jobs = []
        content = response.content.decode('utf-8')
        csv_reader = csv.DictReader(io.StringIO(content))

        for row in csv_reader:
            job_id = row.get('Job ID', row.get('JobNumber'))
            
            if not job_id or database.is_already_posted(job_id):
                continue
                
            title = row.get('Job Title', '')
            # Combine all text fields for the scoring engine to analyze
            description = f"{row.get('Job Summary', '')} {row.get('Requirements', '')} {row.get('Specific Skills', '')}"
            link = f"https://www.jobbank.gc.ca/jobsearch/jobposting/{job_id}"
            
            score, category, reasons = processor.calculate_job_score(title, description)
            
            if processor.is_job_worthy(score):
                new_jobs.append({
                    "job_id": job_id,
                    "title": title,
                    "link": link,
                    "category": category,
                    "reasons": reasons,
                    "score": score
                })
                # Cap CSV processing to save memory on Render Free Tier
                if len(new_jobs) >= 50: 
                    break
                    
        return new_jobs
    except Exception as e:
        logger.error(f"❌ CSV Processing Failure: {e}")
        return []
