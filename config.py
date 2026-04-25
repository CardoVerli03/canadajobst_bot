import os
from dotenv import load_dotenv

# Load local .env for testing
load_dotenv()

# --- TELEGRAM CREDENTIALS ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID")) if os.getenv("ADMIN_ID") else 0
CHANNEL_ID = os.getenv("CHANNEL_ID")

# --- TURSO DATABASE ---
TURSO_URL = os.getenv("TURSO_URL")
TURSO_TOKEN = os.getenv("TURSO_TOKEN")

# --- CLOUD/WEBHOOK SETTINGS ---
WEBHOOK_URL = os.getenv("WEBHOOK_URL") 
PORT = int(os.getenv("PORT", 10000)) 

# --- JOB SOURCES (GOOGLE GATEWAY) ---
# Hii inatafuta site ya jobbank.gc.ca yenye neno sponsorship au lmia ya siku 1 iliyopita
RSS_URL = "https://news.google.com/rss/search?q=site:jobbank.gc.ca+%22sponsorship%22+OR+%22lmia%22+when:1d&hl=en-CA&gl=CA&ceid=CA:en"

# --- SYSTEM SETTINGS ---
SCAM_WARNING = "\n\n⚠️ *Legit employers NEVER ask for money. If asked to pay for a visa or job, it's a SCAM!*"
