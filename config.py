import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = os.getenv("CHANNEL_ID")
TURSO_URL = os.getenv("TURSO_URL")
TURSO_TOKEN = os.getenv("TURSO_TOKEN")

# RSS feed URL ya Canada Job Bank (General search)
RSS_URL = "https://www.jobbank.gc.ca/jobsearch/feed/rss?sort=M&fadvnum=1"
# CSV URL ya Open Data Canada (Inatakiwa ku-check daily)
CSV_URL = "https://www.jobbank.gc.ca/jobsearch/downloadjobs" 
