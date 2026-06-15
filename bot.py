import random
from groq import Groq
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram import Bot
import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
# ====================================

bot = Bot(token=TELEGRAM_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

CONTENT_PROMPTS = [
    "Generate a funny, relatable programming meme caption in Hinglish for developers. Just give the text, witty and short, with 1-2 emojis. Topic: bugs, deadlines, or coding life. Only output the caption, nothing else.",

    "Give one useful coding tip in Hinglish for web developers (PHP/Laravel/React). Keep it short (3-4 lines), practical, with code example if needed. Add a catchy title with emoji. Only output the tip, nothing else.",

    "Create a short roadmap post in Hinglish for someone learning Full Stack Web Development (PHP/Laravel/React). Pick ONE stage (e.g., basics, backend, frontend, deployment) and give 4-5 bullet points of what to learn. Add emoji and motivating tone. Only output the post, nothing else.",

    "Generate an inspirational/motivational quote for programmers in Hinglish, short and shareable, 2-3 lines with emoji. Only output the quote, nothing else."
]


async def generate_content():
    prompt = random.choice(CONTENT_PROMPTS)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content


async def post_daily():
    try:
        content = await generate_content()
        await bot.send_message(chat_id=CHANNEL_ID, text=content)
        print("✅ Posted successfully!")
    except Exception as e:
        print(f"❌ Error: {e}")


async def test_run():
    await post_daily()


async def main():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(post_daily, 'cron', hour=9, minute=0)
    scheduler.add_job(post_daily, 'cron', hour=14, minute=0)
    scheduler.add_job(post_daily, 'cron', hour=20, minute=0)
    scheduler.start()
    print("🚀 Bot scheduler started! Waiting for scheduled times...")

    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    # asyncio.run(test_run())
    asyncio.run(main())
