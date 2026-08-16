import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TELEGRAM_TOKEN = "8943921319:AAHDKG7vYbXvlx4ICidWgkT4s_GojBpILSE"
GEMINI_API_KEY = "AQ.Ab8RN6Km28tHRy_Om-AD411H9O6yLsbNUAsW_TvGFwbKOdKfAw"

client = genai.Client(api_key=GEMINI_API_KEY)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()

def run_web_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHTTPRequestHandler)
    server.serve_forever()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=update.message.text,
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        # Menampilkan detail error asli ke Telegram
        await update.message.reply_text(f"Penyebab error: {e}")

if __name__ == '__main__':
    Thread(target=run_web_server, daemon=True).start()
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
    
