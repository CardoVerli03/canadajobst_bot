import os
from dotenv import load_dotenv

# Load local .env for testing, but on Render it will use Environment Variables
load_dotenv()

# Telegram Credentials
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Turso Database Credentials
TURSO_URL = os.getenv("TURSO_URL")
TURSO_TOKEN = os.getenv("TURSO_TOKEN")

# --- CLOUD/WEBHOOK SETTINGS ---
# Hii URL utaipata Render ukishatengeneza Web Service (e.g., https://mybot.onrender.com)
WEBHOOK_URL = os.getenv("WEBHOOK_URL") 
PORT = int(os.getenv("PORT", 8080)) # Render uses 8080 or 10000 by default

# --- JOB SOURCES ---
# RSS feed URL ya Canada Job Bank (General search)
RSS_URL = "https://www.jobbank.gc.ca/jobsearch/feed/rss?sort=M&fadvnum=1"
# CSV URL ya Open Data Canada (Inatakiwa ku-check daily)
CSV_URL = "https://www.jobbank.gc.ca/jobsearch/downloadjobs"

# Ujumbe wa ulinzi (English only as requested)
SCAM_WARNING = "\n\n⚠️ *Legit employers NEVER ask for money. If asked to pay for a visa or job, it's a SCAM!*"
