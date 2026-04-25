import libsql_client
import config
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Kuanzisha client (Sync client is better for simple webhooks)
def get_client():
    return libsql_client.create_client_sync(
        url=config.TURSO_URL,
        auth_token=config.TURSO_TOKEN
    )

def init_db():
    """Initialize tables in Turso Cloud"""
    db = get_client()
    try:
        # Table for duplicate prevention
        db.execute("""
            CREATE TABLE IF NOT EXISTS posted_jobs (
                job_id TEXT PRIMARY KEY,
                title TEXT,
                posted_date TEXT
            )
        """)
        # Table for anti-spam (50 jobs/day limit)
        db.execute("""
            CREATE TABLE IF NOT EXISTS daily_stats (
                date TEXT PRIMARY KEY,
                count INTEGER DEFAULT 0
            )
        """)
        logger.info("✅ Turso Database synced and ready!")
    except Exception as e:
        logger.error(f"❌ Database Init Error: {e}")

def is_already_posted(job_id):
    """Check if job exists to avoid spamming the channel"""
    db = get_client()
    result = db.execute("SELECT 1 FROM posted_jobs WHERE job_id = ?", [job_id])
    return len(result.rows) > 0

def add_job_to_db(job_id, title):
    """Save job after successful post"""
    db = get_client()
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        db.execute("INSERT OR IGNORE INTO posted_jobs (job_id, title, posted_date) VALUES (?, ?, ?)", 
                   [job_id, title, date_now])
    except Exception as e:
        logger.error(f"❌ Error saving to DB: {e}")

def check_daily_limit():
    """Enforce the 50 jobs per day rule"""
    db = get_client()
    today = datetime.now().strftime("%Y-%m-%d")
    result = db.execute("SELECT count FROM daily_stats WHERE date = ?", [today])
    
    if len(result.rows) == 0:
        # It's a new day, start at 0
        db.execute("INSERT INTO daily_stats (date, count) VALUES (?, 0)", [today])
        return 0
    return result.rows[0][0]

def increment_daily_count():
    """Add +1 to today's count"""
    db = get_client()
    today = datetime.now().strftime("%Y-%m-%d")
    db.execute("UPDATE daily_stats SET count = count + 1 WHERE date = ?", [today])

def get_total_stats():
    """Fetch numbers for the /stats admin command"""
    db = get_client()
    total = db.execute("SELECT COUNT(*) FROM posted_jobs")
    today = datetime.now().strftime("%Y-%m-%d")
    daily = db.execute("SELECT count FROM daily_stats WHERE date = ?", [today])
    
    count_today = daily.rows[0][0] if len(daily.rows) > 0 else 0
    return {"total": total.rows[0][0], "today": count_today}
