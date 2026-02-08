# Telegram Voice Bot 🎤

A Telegram bot for automatic voice message transcription using Whisper AI and saving them to Notion.

## Features

- 🎙️ Receive voice messages in Telegram
- 🎵 Support for audio files (Voice Memos from iPhone, .m4a, .mp3, .wav)
- 🤖 Automatic transcription via OpenAI Whisper API
- 📝 Save transcribed text to Notion database
- 🕐 Automatic timestamp with timezone support (configurable)
- ⏱️ Duration tracking for audio files
- 🔒 User whitelist for private access

## Technologies

- Python 3.8+
- pyTelegramBotAPI - Telegram Bot API
- OpenAI Whisper API - audio transcription
- Notion API - data storage
- Railway.app - hosting (optional)

## Prerequisites

Before installation, obtain the following API keys:

1. **Telegram Bot Token** - via [@BotFather](https://t.me/BotFather)
2. **OpenAI API Key** - at [platform.openai.com](https://platform.openai.com)
3. **Notion Integration Token** - at [notion.so/my-integrations](https://www.notion.so/my-integrations)

## Quick Start (Recommended)

For the fastest setup, use the provided scripts:

```bash
# Clone the repository
git clone https://github.com/your-username/telegram-voice-bot.git
cd telegram-voice-bot

# Run setup wizard (one-time setup)
chmod +x setup.sh
./setup.sh

# Start the bot
./start.sh
```

The setup wizard will:
- Create virtual environment
- Install all dependencies
- Create .env file from template
- Guide you through API key configuration

## Manual Installation (Alternative)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/telegram-voice-bot.git
cd telegram-voice-bot
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```bash
TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_KEY=your_openai_api_key
NOTION_TOKEN=your_notion_integration_token
NOTION_DATABASE_ID=your_notion_database_id
ALLOWED_USERS=your_telegram_user_id
```

**How to obtain each key:**

#### Telegram Bot Token
1. Open [@BotFather](https://t.me/BotFather) in Telegram
2. Send `/newbot`
3. Enter name and username for your bot
4. Copy the token (looks like `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### OpenAI API Key
1. Sign up at [platform.openai.com](https://platform.openai.com)
2. Go to API Keys → Create new secret key
3. Copy the key (starts with `sk-`)
4. Add at least $5 to your account balance

#### Notion Integration Token
1. Go to [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click **"+ New integration"**
3. Fill in:
   - Name: "Telegram Voice Bot"
   - Associated workspace: your workspace
   - Type: Internal integration
4. Submit → copy "Internal Integration Secret" (starts with `secret_`)

#### Notion Database ID
1. Create a new page in Notion
2. Add Database: `/database` → Table - Inline
3. Name the database "Voice Memos"
4. Create columns:
   - **Title** (already exists) - Title property
   - **Text** - Rich text property
   - **Date** - Date property
5. Click **"•••"** → **"Connections"** → add your integration "Telegram Voice Bot"
6. Copy Database ID from URL:
   ```
   https://www.notion.so/Voice-Memos-300fb531a10380bbacb1cb857d1cd1bb
                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                                       This is your DATABASE_ID (32 characters)
   ```

#### Telegram User ID
1. Find [@userinfobot](https://t.me/userinfobot) in Telegram
2. Click Start
3. Copy your User ID (a number, e.g., `123456789`)
4. To add multiple users: `123456789,987654321,555666777`

### 5. Run the bot

```bash
python bot.py
```

Should display:
```
🤖 Bot starting...
✅ Authorized users: [123456789]
🌍 Timezone: Europe/Riga
✅ Ready to receive voice messages!
```

### 6. Test

1. Find your bot in Telegram
2. Send `/start`
3. Send a voice message
4. Check Notion - a new entry should appear!

## Deploy to Railway.app (24/7 hosting)

### 1. Sign up for Railway

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

### 2. Install Railway CLI

```bash
# Mac/Linux
brew install railway

# Or via npm
npm install -g @railway/cli
```

### 3. Login

```bash
railway login
```

### 4. Initialize project

```bash
railway init
```

### 5. Add environment variables

```bash
railway variables set TELEGRAM_TOKEN=your_token
railway variables set OPENAI_KEY=your_key
railway variables set NOTION_TOKEN=your_notion_token
railway variables set NOTION_DATABASE_ID=your_database_id
railway variables set ALLOWED_USERS=your_user_id
```

**Or via web interface:**
1. Open your project on railway.app
2. Settings → Variables
3. Add each variable manually

### 6. Deploy

```bash
railway up
```

### 7. Check logs

```bash
railway logs
```

## Project Structure

```
telegram-voice-bot/
├── bot.py              # Main bot code
├── requirements.txt    # Python dependencies
├── Procfile           # Railway configuration
├── setup.sh           # Setup wizard script
├── start.sh           # Bot start script
├── stop.sh            # Bot stop script
├── .env               # Local variables (DO NOT commit!)
├── .env.example       # Environment template
├── .gitignore         # Ignore .env and venv
└── README.md          # This documentation
```

### Helper Scripts

- **`setup.sh`** - One-time setup wizard that creates venv, installs dependencies, and configures .env
- **`start.sh`** - Activates venv and starts the bot (use this for daily use)
- **`stop.sh`** - Stops running bot process cleanly


## Usage

### Starting the Bot

**Option 1: Using script (recommended)**
```bash
./start.sh
```

**Option 2: Manual start**
```bash
source venv/bin/activate
python bot.py
```

### Stopping the Bot

**Option 1: Using script**
```bash
./stop.sh
```

**Option 2: Manual stop**
- Press `Ctrl+C` in terminal where bot is running

### Bot Commands

- `/start` or `/help` - Show instructions
- Send voice message - Automatic transcription
- Send audio file - Automatic transcription (Voice Memos, .m4a, .mp3, .wav)

### Example Workflow

**With Telegram voice message:**
1. Send voice: "Buy milk, eggs and bread"
2. Bot responds:
   ```
   ✅ Successfully saved!
   📅 Date: 08.02.2026 13:45
   ⏱️ Duration: 0:12
   
   📝 Text:
   Buy milk, eggs and bread
   ```

**With iPhone Voice Memo:**
1. Record a Voice Memo on your iPhone
2. Share it to Telegram (share to bot's chat)
3. Bot automatically transcribes and saves to Notion

3. Entry appears in Notion with full text

## Configuration

### Change Timezone

In `bot.py` change:
```python
TIMEZONE = pytz.timezone('Europe/Riga')  # Your timezone
```

Timezone list: [Wikipedia](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

### Add More Users

In `.env` add comma-separated:
```
ALLOWED_USERS=123456789,987654321,555666777
```

### Change Notion Field Names

If your fields are named differently, change in `bot.py` (line ~110):
```python
properties={
    "Title": {...},      # Your Title field name
    "Text": {...},       # Your Text field name
    "Date": {...}        # Your Date field name
}
```

## Pricing

### OpenAI Whisper API
- $0.006 per minute of audio
- Example: 50 voice messages × 1 minute = $0.30/month

### Railway.app
- $5 free credit monthly (500 hours)
- More than enough for this bot

### Notion
- Free for personal use

**Real cost:** ~$2-5/month (mostly OpenAI)

## Troubleshooting

### Error: "Could not find database"
- Check that Integration is added to database: **"•••"** → **"Connections"**
- Verify Database ID is correct (32 characters, no dashes)

### Error: "Unauthorized"
- Check NOTION_TOKEN
- Verify token starts with `secret_`

### Error: "You don't have access"
- Add your Telegram User ID to ALLOWED_USERS
- Get ID via [@userinfobot](https://t.me/userinfobot)

### Bot doesn't respond
- Check if `python bot.py` is running
- Check Railway logs: `railway logs`
- Verify TELEGRAM_TOKEN

### Whisper doesn't recognize language
- Check that code has `language="uk"` (or your language code)
- Try speaking more clearly
- Check microphone quality

## Security

⚠️ **Important:**

- Never commit `.env` file to git
- Don't share API keys in chats/screenshots
- Use whitelist to restrict access
- Regularly rotate API keys

## Development

### Local Testing

```bash
# Activate venv
source venv/bin/activate

# Run bot
python bot.py

# In another terminal - test via Telegram
```

### Adding New Features

Examples of what you can add:
- Categories for notes
- Tags based on keywords
- AI formatting via Claude
- Search through old notes
- Export to PDF/DOCX

## License

MIT License - free to use for personal and commercial projects.

## Author

Yuriy Polishchuk

## Acknowledgments

This project was developed with the assistance of [Claude AI](https://claude.ai) by Anthropic. Claude helped with:
- Code architecture and implementation
- API integration (Telegram, OpenAI Whisper, Notion)
- Error handling and debugging
- Documentation and README creation
- Deployment configuration

## Feedback

Found a bug or have ideas for improvement? Create an Issue on GitHub!

---

**Useful Links:**
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [OpenAI Whisper](https://platform.openai.com/docs/guides/speech-to-text)
- [Notion API](https://developers.notion.com/)
- [Railway Documentation](https://docs.railway.app/)
