import logging
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from apscheduler.schedulers.background import BackgroundScheduler
import config
import database
import fetcher
import formatter
import bot

# Log errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def auto_job_poster(context):
    """Kazi inayojiendesha yenyewe kupost jobs"""
    daily_count = database.check_daily_limit()
    if daily_count >= 50:
        print("🚫 Daily limit reached (50). Skipping...")
        return

    # Vuta kazi toka RSS na CSV
    jobs = fetcher.fetch_rss_jobs() # Unaweza kuongeza fetch_csv_jobs() hapa pia
    
    posted_now = 0
    for job in jobs:
        if daily_count + posted_now >= 50:
            break
            
        message, reply_markup = formatter.format_job_message(job)
        
        try:
            # Post moja kwa moja kwenye CHANNEL yako
            await context.bot.send_message(
                chat_id=config.CHANNEL_ID,
                text=message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            # Record kwenye database
            database.add_job_to_db(job['job_id'], job['title'])
            database.increment_daily_count()
            posted_now += 1
        except Exception as e:
            print(f"❌ Error posting job: {e}")

if __name__ == '__main__':
    # 1. Washa Database
    database.init_db()

    # 2. Setup Telegram Application
    app = ApplicationBuilder().token(config.BOT_TOKEN).build()

    # 3. Handle Commands & Buttons
    app.add_handler(CommandHandler("start", bot.start))
    app.add_handler(CallbackQueryHandler(bot.button_handler))

    # 4. Setup Scheduler (RSS kila baada ya masaa 6)
    job_queue = app.job_queue
    job_queue.run_repeating(auto_job_poster, interval=21600, first=10) # 21600 sec = 6 hours

    print("🚀 Bot is running... Ready for ujangili!")
    app.run_polling()
