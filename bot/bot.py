import logging

from django.conf import settings
from openai import AsyncOpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from asgiref.sync import sync_to_async

from .models import TelegramUser, Translation

logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

SYSTEM_PROMPT = """You are a translation and rephrasing assistant.
The user will send you text in any language — it could be Hindi, Hinglish, Spanish, Spanglish, or any mixed-language text written casually in their own words.

Your job:
1. Understand the meaning regardless of language or mixed-language style.
2. Translate it into clean, natural English.
3. Lightly rephrase it so it reads smoothly — don't change the meaning, just make it sound natural.

Reply ONLY with the translated and rephrased English text. No explanations, no quotes, no labels."""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! Send me text in any language (Hinglish, Spanish, mixed — anything!) "
        "and I'll translate and rephrase it into clean English."
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Just send me any text — even mixed languages like Hinglish — "
        "and I'll give you a clean English version."
    )


async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text},
            ],
            temperature=0.3,
        )
        result = response.choices[0].message.content

        tg_user, _ = await sync_to_async(TelegramUser.objects.update_or_create)(
            telegram_id=user.id,
            defaults={
                "username": user.username or "",
                "first_name": user.first_name or "",
                "last_name": user.last_name or "",
                "language_code": user.language_code or "",
                "is_bot": user.is_bot,
            },
        )

        await sync_to_async(Translation.objects.create)(
            user=tg_user,
            original_text=text,
            translated_text=result,
        )

        await update.message.reply_text(result)
    except Exception as e:
        logger.error(f"Translation error: {e}")
        await update.message.reply_text(
            "Sorry, I couldn't translate that. Please try again."
        )


def run_bot():
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))
    logger.info("Bot is running...")
    app.run_polling()
