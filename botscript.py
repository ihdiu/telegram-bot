from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# === CONFIGURATION ===
TOKEN = "7414416452:AAGXzuIMfox-3cWddcpNQTSe8CNgpnrqOJw"
GROUP_ID = -1002302994371  # Replace with your supergroup ID
ANNOUNCEMENT_TOPIC_ID = 2  # Replace with your actual announcement topic ID
DISCUSSION_TOPIC_ID =  0   # Replace with your actual discussion topic ID

# === MAIN HANDLER ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.effective_message
    user = message.from_user

    # Check topic
    if message.message_thread_id != ANNOUNCEMENT_TOPIC_ID:
        return

    # Skip admins
    member = await context.bot.get_chat_member(chat_id=GROUP_ID, user_id=user.id)
    if member.status in ['administrator', 'creator']:
        return

    # Build display name
    name = user.username if user.username else user.first_name

    # Send formatted message to discussion topic
    header = f"From: @{name}\n\n<blockquote>Message: {message.text}</blockquote>\n\nForwarded From: Announcement"
    await context.bot.send_message(
        chat_id=GROUP_ID,
        text=header,
        message_thread_id=DISCUSSION_TOPIC_ID,
        parse_mode='HTML'
    )

    # Forward the message content (copied, so it appears fresh)
    #await context.bot.copy_message(
    #    chat_id=GROUP_ID,
    #    from_chat_id=GROUP_ID,
    #    message_id=message.message_id,
    #    message_thread_id=DISCUSSION_TOPIC_ID
    #)

    # Delete original message in the announcement topic
    await message.delete()

# === SETUP ===
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.Chat(GROUP_ID) & filters.ALL, handle_message))
    print("Bot is running...")
    app.run_polling()
