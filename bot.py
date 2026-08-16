import asyncio
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Dummy Web Server agar Render senang (Port Binding)
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot Telegram is Running!")

def run_web_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHTTPRequestHandler)
    server.serve_forever()

# Credential kamu
TELEGRAM_TOKEN = "8825784666:AAHX82H0P8JnsrvVj3KGi0s1kkU3re0W_ek"
GEMINI_API_KEY = "AQ.Ab8RN6JboF5XV-ihNOugbPZJLKt4d2651XYVBHpJDkFpi05r1g"

client = genai.Client(api_key=GEMINI_API_KEY)
SYSTEM_PROMPT = "You are a helpful AI assistant. Always respond in English."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\nUser: {user_text}",
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        # Langsung tampilkan isi pesan error aslinya ke chat Telegram
        await update.message.reply_text(f"Error detail: {str(e)}")
        print(f"Error: {e}")
        
