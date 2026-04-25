from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import config

def format_job_message(job):
    """Generates a clean, professional English job post for the channel"""
    
    # Safisha title (Lower case then Title case for better reading)
    clean_title = job['title'].strip().title()
    
    # Panga highlights vizuri na alama
    reasons_str = " | ".join(job['reasons'])
    
    # Message Body
    message = (
        f"{job['category']} **NEW OPPORTUNITY FOUND** {job['category']}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 **Position:** {clean_title}\n"
        f"✨ **Highlights:** {reasons_str}\n"
        f"📊 **Match Score:** {job['score']}/7\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📍 Location: Canada (LMIA/Sponsorship)\n"
        f"{config.SCAM_WARNING}"
    )
    
    # Modern Buttons
    keyboard = [
        [InlineKeyboardButton("Apply Now ↗️", url=job['link'])],
        # Unaweza kuongeza button ya pili hapa kama unataka, mfano Contact Admin
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    return message, reply_markup
