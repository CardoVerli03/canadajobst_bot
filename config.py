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

# --- ADZUNA API CREDENTIALS ---
ADZUNA_APP_ID = "77fd8aaa"
ADZUNA_APP_KEY = "e068ae31ce1c2a3e428ca0399875dcdb"

# --- JOB SETTINGS ---
# Tutatafuta kazi nchi ya Canada (ca)
COUNTRY_CODE = "ca"
# Tafuta maneno haya ya ujangili
KEYWORDS = "sponsorship visa lmia"

# --- SYSTEM SETTINGS ---
SCAM_WARNING = "\n\n⚠️ *Legit employers NEVER ask for money. If asked to pay for a visa or job, it's a SCAM!*"
