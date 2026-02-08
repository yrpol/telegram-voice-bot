import os
import telebot
import openai
from notion_client import Client
import requests
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Initialize bot and API clients with environment variables
bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
openai.api_key = os.getenv('OPENAI_KEY')
notion = Client(auth=os.getenv('NOTION_TOKEN'))
DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Handle /start and /help commands
    Send welcome message with instructions
    """
    welcome_text = (
        "👋 Привіт! Я бот для голосових нотаток.\n\n"
        "📝 Надішли мені голосове повідомлення, і я:\n"
        "1️⃣ Перетворю його в текст через Whisper AI\n"
        "2️⃣ Збережу в твою Notion базу даних\n\n"
        "Просто надішли голосове - і все! 🎤"
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    """
    Main handler for voice messages
    Process: Download -> Transcribe -> Save to Notion
    """
    try:
        # Send initial confirmation to user
        status_msg = bot.reply_to(message, "⏳ Обробляю голосове повідомлення...")
        
        # Step 1: Download audio file from Telegram
        file_info = bot.get_file(message.voice.file_id)
        file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'
        file_response = requests.get(file_url)
        
        # Save audio temporarily
        audio_filename = 'voice.ogg'
        with open(audio_filename, 'wb') as f:
            f.write(file_response.content)
        
        # Update status
        bot.edit_message_text(
            "🎤 Транскрибую аудіо...", 
            message.chat.id, 
            status_msg.message_id
        )
        
        # Step 2: Transcribe audio using OpenAI Whisper
        with open(audio_filename, 'rb') as audio_file:
            transcript = openai.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="uk"  # Ukrainian language
            )
        
        transcribed_text = transcript.text
        
        # Update status
        bot.edit_message_text(
            "💾 Зберігаю в Notion...", 
            message.chat.id, 
            status_msg.message_id
        )
        
        # Step 3: Save to Notion database
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                # Title field - first 100 characters of transcription
                "Назва": {
                    "title": [
                        {
                            "text": {
                                "content": transcribed_text[:100]
                            }
                        }
                    ]
                },
                # Full text field
                "Текст": {
                    "rich_text": [
                        {
                            "text": {
                                "content": transcribed_text
                            }
                        }
                    ]
                }
            }
        )
        
        # Clean up temporary audio file
        if os.path.exists(audio_filename):
            os.remove(audio_filename)
        
        # Send success message with preview
        preview_length = 300
        preview_text = transcribed_text[:preview_length]
        if len(transcribed_text) > preview_length:
            preview_text += "..."
        
        success_message = f"✅ Успішно збережено в Notion!\n\n📝 Текст:\n{preview_text}"
        bot.edit_message_text(
            success_message,
            message.chat.id,
            status_msg.message_id
        )
        
    except Exception as e:
        # Handle any errors and notify user
        error_message = f"❌ Помилка: {str(e)}\n\nСпробуй ще раз або напиши /help"
        bot.reply_to(message, error_message)
        print(f"Error processing voice message: {e}")
        
        # Clean up temporary file in case of error
        if os.path.exists('voice.ogg'):
            os.remove('voice.ogg')

@bot.message_handler(content_types=['text'])
def handle_text(message):
    """
    Handle regular text messages
    Remind user to send voice messages
    """
    bot.reply_to(
        message, 
        "🎤 Надішли мені голосове повідомлення, щоб я міг його обробити!\n\n"
        "Або напиши /help для інструкцій."
    )

# Start the bot
if __name__ == '__main__':
    print("🤖 Bot is starting...")
    print("✅ Ready to receive voice messages!")
    
    # Start polling for messages (blocking call)
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user")
    except Exception as e:
        print(f"❌ Bot crashed: {e}")