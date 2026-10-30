import os
import random
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

QUESTIONS = [
    {"q": "What is the capital of Nigeria?", "options": ["Lagos", "Abuja", "Kano"], "a": "Abuja"},
    {"q": "Who is known as Afrobeat legend?", "options": ["Fela", "Wizkid", "Davido"], "a": "Fela"},
    {"q": "2 + 2 x 2 = ?", "options": ["4", "6", "8"], "a": "6"},
    {"q": "What year did Nigeria gain independence?", "options": ["1960", "1963", "1970"], "a": "1960"},
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🇳🇬 Welcome to Naija Sharp Quiz Bot!\n\nType /quiz to get a question!\nType /score to see your score.")

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = random.choice(QUESTIONS)
    context.user_data['current_answer'] = q['a']
    text = f"🧠 {q['q']}\n\n"
    for i, opt in enumerate(q['options'], 1):
        text += f"{i}. {opt}\n"
    text += "\nReply with the answer!"
    await update.message.reply_text(text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_answer = update.message.text.strip()
    correct = context.user_data.get('current_answer')
    if not correct:
        await update.message.reply_text("Type /quiz first!")
        return
    if user_answer.lower() == correct.lower() or user_answer in correct:
        await update.message.reply_text(f"✅ Correct! Na {correct}!")
        context.user_data['score'] = context.user_data.get('score', 0) + 1
    else:
        await update.message.reply_text(f"❌ Wrong! Answer na {correct}. Try /quiz again!")
    context.user_data['current_answer'] = None

async def score(update: Update, context: ContextTypes.DEFAULT_TYPE):
    s = context.user_data.get('score', 0)
    await update.message.reply_text(f"Your score: {s} points 🔥")

TOKEN = os.getenv("BOT_TOKEN")
if not TOKEN:
    raise ValueError("BOT_TOKEN not set!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("quiz", quiz))
app.add_handler(CommandHandler("score", score))
from telegram.ext import MessageHandler, filters
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()
