import requests
import config
import database
import processor
import logging

logger = logging.getLogger(__name__)

def fetch_rss_jobs():
    """Fetch jobs from Adzuna API (The Final Boss Strategy)"""
    logger.info(f"📡 Scanning Adzuna API for {config.KEYWORDS} in {config.COUNTRY_CODE}...")
    
    # Adzuna API URL Construction
    # 'results_per_page=50' inatuhakikishia tunapata mzigo wa kutosha kila scan
    url = f"https://api.adzuna.com/v1/api/jobs/{config.COUNTRY_CODE}/search/1"
    params = {
        'app_id': config.AD_APP_ID if hasattr(config, 'AD_APP_ID') else config.ADZUNA_APP_ID,
        'app_key': config.AD_APP_KEY if hasattr(config, 'AD_APP_KEY') else config.ADZUNA_APP_KEY,
        'results_per_page': 50,
        'what': config.KEYWORDS,
        'content-type': 'application/json'
    }

    try:
        response = requests.get(url, params=params, timeout=20)
        
        if response.status_code != 200:
            logger.error(f"❌ Adzuna API Error: {response.status_code} - {response.text}")
            return []
            
        data = response.json()
        results = data.get('results', [])
        new_jobs = []

        for job in results:
            # Adzuna ID ni ya kipekee (Unique)
            job_id = str(job.get('id'))
            
            if database.is_already_posted(job_id):
                continue
                
            title = job.get('title', '')
            link = job.get('redirect_url', '')
            # Adzuna inatoa 'description' nzuri kwa ajili ya processor yetu
            description = job.get('description', '')
            
            # Hatua ya Scoring - Hapa tunahakikisha ni sponsorship kweli
            score, category, reasons = processor.calculate_job_score(title, description)
            
            # Tunapata kazi ambazo zina sifa kweli
            if score >= 2:
                new_jobs.append({
                    "job_id": job_id,
                    "title": title,
                    "link": link,
                    "category": category,
                    "reasons": reasons,
                    "score": score
                })
        
        logger.info(f"✅ Adzuna scan complete. Found {len(new_jobs)} worthy jobs.")
        return new_jobs

    except Exception as e:
        logger.error(f"❌ Adzuna Critical Failure: {e}")
    
    return []

def fetch_csv_jobs():
    """Disabled to save resources"""
    return []
