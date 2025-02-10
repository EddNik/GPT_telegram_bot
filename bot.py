
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler, MessageHandler,filters, ConversationHandler

from gpt import ChatGptService
from util import (load_message, send_text, send_image, show_main_menu, send_text_buttons,
                   load_prompt, Dialog)

import credentials

async def default_callback_handler(update: Update,
                                   context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    query = update.callback_query.data
    if query == "bot_random_btn_request":
        await random(update, context)
    elif query == "bot_random_btn_exit":
        await start(update, context)
    # elif query == "bot_gpt_btn_promt":
    #     await gpt(update, context)
    elif query == "bot_gpt_btn_exit":
        await start(update, context)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "default"
    text = load_message('main')
    await send_image(update, context, 'main')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'start': 'Головне меню',
        'random': 'Дізнатися випадковий цікавий факт 🧠',
        'gpt': 'Задати питання чату GPT 🤖',
        'talk': 'Поговорити з відомою особистістю 👤',
        'quiz': 'Взяти участь у квізі ❓'
        # Додати команду в меню можна так:
        # 'command': 'button text'
    })

# async def app_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "random"
    text = load_message('random')
    await send_image(update, context,'random')
    await send_text(update, context, text)
    prompt = load_prompt('random')
    content = await chat_gpt.send_question(prompt, 'Дай цікавий факт' )
    await send_text(update, context, content)
    text = load_message('thanksgiving')
    content = await chat_gpt.send_question(text, 'Thank you')
    await send_text_buttons(update, context, content,
                            {'bot_random_btn_request': 'Give me more facts', 'bot_random_btn_exit': 'Exit'})

async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "gpt"
    # text = load_message('gpt')
    await send_image(update, context, 'gpt')
    text = update.message.text
    await update.message.reply_text(f"You sent: {text}. Wait for answer please.")
    await chat_gpt.add_message(text)
    answer = await chat_gpt.send_message_list()
    await send_text(update, context, answer)
    await update.message.reply_text("Now type something else or exit.")
    await send_text_buttons(update, context, text,
                            {'bot_gpt_btn_exit': 'Exit'})


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "talk"
    text = load_message('talk')
    await send_image(update, context, 'talk')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'talk': 'Поговорити з відомою особистістю ��',
            })
    # content = await chat_gpt.send_question(prompt, 'Дай цікавий факт')



dialog = Dialog()
dialog.mode = "default"

chat_gpt = ChatGptService(credentials.ChatGPT_TOKEN)
bot = ApplicationBuilder().token(credentials.BOT_TOKEN).build()

# Зареєструвати обробник команди можна так:
# app.add_handler(CommandHandler('command', handler_func))
bot.add_handler(CommandHandler('start',start))
bot.add_handler(CommandHandler('random', random))
bot.add_handler(CommandHandler('gpt', gpt))
bot.add_handler(CommandHandler('talk', talk))

bot.add_handler(MessageHandler(filters.TEXT, gpt))
# bot.add_handler(MessageHandler(filters.COMMAND, start))

# Зареєструвати обробник колбеку можна так:
# bot.add_handler(CallbackQueryHandler(default_callback_handler, pattern='^bot_.*'))
bot.add_handler(CallbackQueryHandler(default_callback_handler))
bot.run_polling()
