# Rephrase Bot

A Telegram bot that translates and rephrases text from any language (including mixed languages like Hinglish, Spanglish) into clean, natural English using OpenAI.

## Setup

1. **Create a Telegram bot** via [BotFather](https://t.me/BotFather) and copy the token.

2. **Get an OpenAI API key** from [platform.openai.com/api-keys](https://platform.openai.com/api-keys).

3. **Clone and configure:**
   ```bash
   cd rephrase_bot
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Create a `.env` file:**
   ```
   TELEGRAM_BOT_TOKEN=your-telegram-bot-token
   OPENAI_API_KEY=your-openai-api-key
   ```

5. **Run:**
   ```bash
   python bot.py
   ```

## How It Works

- Send any text to the bot in any language
- The bot uses GPT-4o-mini to understand, translate, and lightly rephrase it into natural English
- Handles mixed-language input (Hinglish, Spanglish, etc.) that traditional translators struggle with
- Uses async OpenAI calls so multiple users are handled concurrently
