import feedparser
import requests
import csv
import io
import config
import database
import processor

def fetch_rss_jobs():
    """Vuta kazi mpya kutoka RSS feed (Live Updates)"""
    print("📡 Fetching jobs from RSS...")
    feed = feedparser.parse(config.RSS_URL)
    new_jobs = []

    for entry in feed.entries:
        job_id = entry.id.split('/')[-1] # Extract ID kutoka URL
        
        if database.is_already_posted(job_id):
            continue
            
        title = entry.title
        link = entry.link
        # RSS mara nyingi haina description ndefu, tunachukua summary
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

def fetch_csv_jobs():
    """Vuta kazi kutoka kwenye Open Data CSV (Daily Deep Scan)"""
    print("📥 Downloading Daily CSV Dataset...")
    response = requests.get(config.CSV_URL)
    if response.status_code != 200:
        print("❌ Failed to download CSV")
        return []

    new_jobs = []
    # Kusoma CSV data toka kwenye memory bila kusave file kwanza
    content = response.content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(content))

    for row in csv_reader:
        # Canada Job Bank CSV mara nyingi ina 'Job ID' column
        job_id = row.get('Job ID', row.get('JobNumber'))
        
        if not job_id or database.is_already_posted(job_id):
            continue
            
        title = row.get('Job Title', '')
        description = f"{row.get('Job Summary', '')} {row.get('Requirements', '')}"
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
            # Limit CSV processing isije ikala RAM ya simu/VPS
            if len(new_jobs) >= 100: 
                break
                
    return new_jobs
