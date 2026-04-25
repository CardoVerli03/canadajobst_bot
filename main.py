import logging
import os
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import config
import database
import fetcher
import formatter
import bot

# 1. Setup Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 2. Initialize Flask for Render (The Keep-Alive & Webhook Receiver)
server = Flask(__name__)

# 3. Build Telegram Application
app = ApplicationBuilder().token(config.BOT_TOKEN).build()

# 4. The Auto-Poster Logic (The "Jangili" Engine)
async def auto_job_poster(context: ContextTypes.DEFAULT_TYPE):
    """Automatic job fetching and posting to channel"""
    daily_count = database.check_daily_limit()
    if daily_count >= 50:
        logger.info("🚫 Daily limit reached (50). Skipping...")
        return

    # Fetch from RSS and CSV
    jobs = fetcher.fetch_rss_jobs() 
    # Optional: jobs += fetcher.fetch_csv_jobs()
    
    posted_now = 0
    for job in jobs:
        if daily_count + posted_now >= 50:
            break
            
        message, reply_markup = formatter.format_job_message(job)
        
        try:
            # Post directly to the CHANNEL
            await context.bot.send_message(
                chat_id=config.CHANNEL_ID,
                text=message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            # Record in Turso DB
            database.add_job_to_db(job['job_id'], job['title'])
            database.increment_daily_count()
            posted_now += 1
            logger.info(f"✅ Posted: {job['title']}")
        except Exception as e:
            logger.error(f"❌ Error posting job: {e}")

# 5. Webhook Routes
@server.route(f"/{config.BOT_TOKEN}", methods=['POST'])
async def webhook():
    """Receive updates from Telegram"""
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), app.bot)
        await app.update_queue.put(update)
        return "OK", 200

@server.route("/")
def index():
    """Home route for Cron-job pinging"""
    return "Bot is running on Webhook mode!", 200

# 6. Main Runner
if __name__ == '__main__':
    # Initialize DB
    database.init_db()

    # Handlers
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CallbackQueryHandler(bot.button_handler))

    # Scheduler (Runs every 6 hours = 21600 seconds)
    job_queue = app.job_queue
    job_queue.run_repeating(auto_job_poster, interval=21600, first=10)

    # Set Webhook with Telegram
    # Important: WEBHOOK_URL must be like https://your-app.onrender.com
    webhook_path = f"{config.WEBHOOK_URL}/{config.BOT_TOKEN}"
    
    logger.info(f"🚀 Setting Webhook to: {webhook_path}")
    
    # Run the Flask server and Bot
    # Note: On Render, we use the PORT variable assigned by the environment
    app.run_webhook(
        listen="0.0.0.0",
        port=config.PORT,
        url_path=config.BOT_TOKEN,
        webhook_url=webhook_path
    )
