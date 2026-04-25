from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import database
import config
import keywords

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Main Menu ya Admin pekee"""
    if update.effective_user.id != config.ADMIN_ID:
        return # Unskilled intruder block!

    keyboard = [
        [InlineKeyboardButton("📊 Stats", callback_data='stats'),
         InlineKeyboardButton("🚀 Force Fetch", callback_data='force')],
        [InlineKeyboardButton("📂 Job Categories", callback_data='categories')],
        [InlineKeyboardButton("🔑 View Keywords", callback_data='keywords')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🇨🇦 **Canada Jobs Admin Panel**\nChoose an action below:",
        reply_markup=reply_markup, parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inashughulika na mibonyezo yote ya button"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'stats':
        stats = database.get_total_stats()
        text = f"📈 **Bot Statistics**\n\nJobs Today: {stats['today']}/50\nTotal Posted: {stats['total']}"
        keyboard = [[InlineKeyboardButton("⬅️ Back", callback_data='back_main')]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'categories':
        keyboard = []
        # Tengeneza grid ya categories 2 per row
        cats = list(keywords.CATEGORIES.keys())
        for i in range(0, len(cats), 2):
            row = [InlineKeyboardButton(cats[i], callback_data=f"cat_{cats[i]}")]
            if i+1 < len(cats):
                row.append(InlineKeyboardButton(cats[i+1], callback_data=f"cat_{cats[i+1]}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data='back_main')])
        
        await query.edit_message_text("Select a category to see keywords:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'back_main':
        # Rudisha menu kuu
        keyboard = [
            [InlineKeyboardButton("📊 Stats", callback_data='stats'),
             InlineKeyboardButton("🚀 Force Fetch", callback_data='force')],
            [InlineKeyboardButton("📂 Job Categories", callback_data='categories')],
            [InlineKeyboardButton("🔑 View Keywords", callback_data='keywords')]
        ]
        await query.edit_message_text("🇨🇦 **Canada Jobs Admin Panel**\nChoose an action below:", 
                                      reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

    elif query.data == 'force':
        await query.edit_message_text("🔄 Manual Fetch Started... checking RSS/CSV.")
        # Trigger fetch function hapa (tutaiita kutoka main.py)
