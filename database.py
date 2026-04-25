import libsql_client
import config
from datetime import datetime

# Unganisha na Turso
client = libsql_client.create_client_sync(
    url=config.TURSO_URL,
    auth_token=config.TURSO_TOKEN
)

def init_db():
    """Tengeneza table kama hazipo"""
    # Table ya kazi zilizopostiwa
    client.execute("""
        CREATE TABLE IF NOT EXISTS posted_jobs (
            job_id TEXT PRIMARY KEY,
            title TEXT,
            posted_date TEXT
        )
    """)
    # Table ya stats za siku (Daily Limit)
    client.execute("""
        CREATE TABLE IF NOT EXISTS daily_stats (
            date TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
    """)
    print("✅ Database initialized successfully!")

def is_already_posted(job_id):
    """Check kama kazi ishapostiwa kuzuia duplicates"""
    result = client.execute("SELECT 1 FROM posted_jobs WHERE job_id = ?", [job_id])
    return len(result.rows) > 0

def add_job_to_db(job_id, title):
    """Hifadhi kazi baada ya kupost"""
    date_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    client.execute("INSERT INTO posted_jobs (job_id, title, posted_date) VALUES (?, ?, ?)", 
                   [job_id, title, date_now])

def check_daily_limit():
    """Angalia kama tushafikisha kazi 50 leo"""
    today = datetime.now().strftime("%Y-%m-%d")
    result = client.execute("SELECT count FROM daily_stats WHERE date = ?", [today])
    if len(result.rows) == 0:
        client.execute("INSERT INTO daily_stats (date, count) VALUES (?, 0)", [today])
        return 0
    return result.rows[0][0]

def increment_daily_count():
    """Ongeza hesabu ya kazi ya siku"""
    today = datetime.now().strftime("%Y-%m-%d")
    client.execute("UPDATE daily_stats SET count = count + 1 WHERE date = ?", [today])

def get_total_stats():
    """Kwa ajili ya /stats command ya Admin"""
    total = client.execute("SELECT COUNT(*) FROM posted_jobs")
    today = datetime.now().strftime("%Y-%m-%d")
    daily = client.execute("SELECT count FROM daily_stats WHERE date = ?", [today])
    
    count_today = daily.rows[0][0] if len(daily.rows) > 0 else 0
    return {"total": total.rows[0][0], "today": count_today}
