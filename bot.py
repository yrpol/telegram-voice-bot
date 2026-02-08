import os
import telebot
from openai import OpenAI
from notion_client import Client
import requests
from dotenv import load_dotenv
from datetime import datetime
import pytz

load_dotenv()

# Initialize APIs
bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
openai_client = OpenAI(api_key=os.getenv('OPENAI_KEY'))
notion = Client(auth=os.getenv('NOTION_TOKEN'))
DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

# Timezone configuration
TIMEZONE = pytz.timezone('Europe/Riga')

# Whitelist
ALLOWED_USERS = [int(id) for id in os.getenv('ALLOWED_USERS').split(',')]

def is_authorized(user_id):
    """Check if user is authorized to use the bot"""
    return user_id in ALLOWED_USERS

def authorized_only(func):
    """Decorator to restrict access to authorized users only"""
    def wrapper(message):
        if not is_authorized(message.from_user.id):
            bot.reply_to(
                message, 
                "⛔️ У вас немає доступу до цього бота.\n"
                f"Ваш ID: {message.from_user.id}"
            )
            print(f"❌ Unauthorized access attempt from {message.from_user.id} "
                  f"(@{message.from_user.username})")
            return
        return func(message)
    return wrapper

@bot.message_handler(commands=['start', 'help'])
@authorized_only
def send_welcome(message):
    """Handle /start and /help commands"""
    welcome_text = (
        "👋 Привіт! Я бот для голосових нотаток.\n\n"
        "📝 Надішли мені голосове повідомлення або аудіофайл, і я:\n"
        "1️⃣ Перетворю його в текст через Whisper AI\n"
        "2️⃣ Збережу в твою Notion базу даних\n\n"
        "🎤 Підтримується:\n"
        "• Голосові повідомлення Telegram\n"
        "• Voice Memos з iPhone (.m4a)\n"
        "• Будь-які аудіофайли (.mp3, .wav, тощо)\n\n"
        "Просто надішли аудіо - і все! 🚀"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(content_types=['voice', 'audio'])
@authorized_only
def handle_voice(message):
    """Main handler for voice messages and audio files"""
    try:
        # Send initial confirmation
        status_msg = bot.reply_to(message, "⏳ Обробляю голосове повідомлення...")
        
        # Step 1: Download audio file from Telegram
        # Handle both voice messages and audio files (Voice Memos from iPhone)
        if message.content_type == 'voice':
            file_info = bot.get_file(message.voice.file_id)
            audio_filename = 'voice.ogg'
            duration = message.voice.duration
        else:  # audio
            file_info = bot.get_file(message.audio.file_id)
            # Use original filename or default to audio.m4a
            audio_filename = message.audio.file_name or 'audio.m4a'
            duration = message.audio.duration
        
        file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'
        file_response = requests.get(file_url)
        
        # Save audio temporarily
        with open(audio_filename, 'wb') as f:
            f.write(file_response.content)
        
        # Update status
        bot.edit_message_text(
            "🎤 Транскрибую аудіо...", 
            message.chat.id, 
            status_msg.message_id
        )
        
        # Step 2: Transcribe using Whisper
        with open(audio_filename, 'rb') as audio_file:
            transcript = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="uk"
            )
        
        transcribed_text = transcript.text
        
        # Update status
        bot.edit_message_text(
            "💾 Зберігаю в Notion...", 
            message.chat.id, 
            status_msg.message_id
        )
        
        # Step 3: Convert timestamp to Riga timezone
        # Using timezone-aware datetime instead of deprecated utcfromtimestamp
        utc_time = datetime.fromtimestamp(message.date, tz=pytz.UTC)
        local_time = utc_time.astimezone(TIMEZONE)
        message_date = local_time.isoformat()
        
        # Save to Notion with updated field names
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": transcribed_text[:100]
                            }
                        }
                    ]
                },
                "Text": {
                    "rich_text": [
                        {
                            "text": {
                                "content": transcribed_text
                            }
                        }
                    ]
                },
                "Date": {
                    "date": {
                        "start": message_date
                    }
                }
            }
        )
        
        # Clean up
        if os.path.exists(audio_filename):
            os.remove(audio_filename)
        
        # Success message with local time
        formatted_date = local_time.strftime("%d.%m.%Y %H:%M")
        
        # Format duration in minutes:seconds
        duration_str = f"{duration // 60}:{duration % 60:02d}"
        
        preview_length = 300
        preview_text = transcribed_text[:preview_length]
        if len(transcribed_text) > preview_length:
            preview_text += "..."
        
        success_message = (
            f"✅ Успішно збережено!\n"
            f"📅 Дата: {formatted_date}\n"
            f"⏱️ Тривалість: {duration_str}\n\n"
            f"📝 Текст:\n{preview_text}"
        )
        bot.edit_message_text(
            success_message,
            message.chat.id,
            status_msg.message_id
        )
        
    except Exception as e:
        error_message = f"❌ Помилка: {str(e)}"
        bot.reply_to(message, error_message)
        print(f"Error: {e}")
        
        # Clean up any temporary files
        for ext in ['.ogg', '.m4a', '.mp3', '.wav']:
            temp_file = f"voice{ext}"
            if os.path.exists(temp_file):
                os.remove(temp_file)
            temp_file = f"audio{ext}"
            if os.path.exists(temp_file):
                os.remove(temp_file)

@bot.message_handler(content_types=['text'])
@authorized_only
def handle_text(message):
    """Handle text messages"""
    bot.reply_to(
        message, 
        "🎤 Надішли мені голосове повідомлення або аудіофайл!\n\n"
        "Підтримуються: Voice Memos, .m4a, .mp3, .wav\n\n"
        "Або /help для інструкцій."
    )

# Start bot
if __name__ == '__main__':
    print("🤖 Bot starting...")
    print(f"✅ Authorized users: {ALLOWED_USERS}")
    print(f"🌍 Timezone: {TIMEZONE}")
    
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except KeyboardInterrupt:
        print("\n👋 Bot stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
