import logging
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Replace with your actual credentials
TELEGRAM_TOKEN = "8825784666:AAHX82H0P8JnsrvVj3KGi0s1kkU3re0W_ek"
GEMINI_API_KEY = "AQ.Ab8RN6Izmg2YeYGAqblPbfCd2u5pGHz-2VRuEiR1KVWT_pVAZg"

# Initialize Gemini Client
client = genai.Client(api_key=GEMINI_API_KEY)

# Configure system prompt for English AI response
SYSTEM_PROMPT = "You are a helpful AI assistant. Always respond in English."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        # Generate content using Gemini 2.5 Flash
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\nUser: {user_text}",
        )

        # Reply to user on Telegram
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Sorry, an error occurred while processing your request.")
        print(f"Error: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Telegram AI Agent is running...")
    app.run_polling()
  
