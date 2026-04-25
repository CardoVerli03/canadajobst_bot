import os
from dotenv import load_dotenv

# Load local .env for testing, but on Render it will use Environment Variables
load_dotenv()

# --- TELEGRAM CREDENTIALS ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Tunahakikisha ADMIN_ID inasomeka kama namba
ADMIN_ID = int(os.getenv("ADMIN_ID")) if os.getenv("ADMIN_ID") else 0
CHANNEL_ID = os.getenv("CHANNEL_ID")

# --- TURSO DATABASE ---
TURSO_URL = os.getenv("TURSO_URL")
TURSO_TOKEN = os.getenv("TURSO_TOKEN")

# --- CLOUD/WEBHOOK SETTINGS ---
# Hii URL inatakiwa iwe ile ya Render (https://canadajobst-bot.onrender.com)
WEBHOOK_URL = os.getenv("WEBHOOK_URL") 
PORT = int(os.getenv("PORT", 10000)) 

# --- JOB SOURCES (RSS ONLY) ---
# Toleo la 2026 la Job Bank RSS - General Search
RSS_URL = "https://www.jobbank.gc.ca/jobsearch/feed/rss?sort=M&fadvnum=1"

# --- SYSTEM SETTINGS ---
# Scam warning inayotumika kwenye formatter.py
SCAM_WARNING = "\n\n⚠️ *Legit employers NEVER ask for money. If asked to pay for a visa or job, it's a SCAM!*"
