from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def format_job_message(job):
    """Tengeneza ujumbe wa Kiingereza uliotulia"""
    reasons_str = " | ".join(job['reasons'])
    
    message = (
        f"{job['category']} **NEW JOB FOUND** {job['category']}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 **Title:** {job['title']}\n"
        f"🌟 **Highlights:** {reasons_str}\n"
        f"🎖️ **Score:** {job['score']}/7\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"⚠️ *Legit employers NEVER ask for money. If asked to pay, it's a SCAM!*"
    )
    
    # Kitufe cha Apply
    keyboard = [[InlineKeyboardButton("Apply Now ↗️", url=job['link'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    return message, reply_markup
