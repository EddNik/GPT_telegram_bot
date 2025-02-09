
from telegram import Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler, MessageHandler

from gpt import ChatGptService
from util import (load_message, send_text, send_image, show_main_menu, send_text_buttons,
                   load_prompt)

import credentials

async def default_callback_handler(update: Update,
                                   context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    query = update.callback_query.data
    # if query == 'start':
    #     await start(update, context)
    if query == "random_btn_request":
        await random(update, context)
    elif query == "random_btn_exit":
        await start(update, context)
    elif query == "gpt_button_1":
        await gpt(update, context)
    elif query == "gpt_button_2":
        await start(update, context)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    text = load_message('random')
    await send_image(update, context,'random')
    await send_text(update, context, text)
    prompt = load_prompt('random')
    content = await chat_gpt.send_question(prompt, 'Дай цікавий факт' )
    await send_text(update, context, content)
    await send_text_buttons(update,context,content,{'random_btn_request':'Give me more facts', 'random_btn_exit':'Exit'})

async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('gpt')
    # message_type = update.message.chat.type
    # text = update.message.text
    # # await update.message.reply_text(text)
    # time.sleep(15)
    # await update.message.reply_text(f"You sent: {text}. Now send something else.")


    await send_image(update, context, 'gpt')
    # await update.message.reply_text('I am GPT please enter your request')
    # time.sleep(5)
    # text = update.message.text
    # await update.message.reply_text(text)
    # user_text = update.message.from_user.username
    # await send_text(update, context, text)
    prompt = load_prompt('gpt')
    # content = await chat_gpt.send_question(prompt, 'Give my horoscope information')
    content = await chat_gpt.send_question(prompt, text)
    await send_text_buttons(update, context, content,
                            {'gpt_button_1': 'Type your request again', 'gpt_button_2': 'I have not more questions'})
    await send_text(update, context, content)

async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = load_message('talk')
    await send_image(update, context, 'talk')
    await send_text(update, context, text)
    await show_main_menu(update, context, {
        'talk': 'Поговорити з відомою особистістю ��',
            })
    # content = await chat_gpt.send_question(prompt, 'Дай цікавий факт')





chat_gpt = ChatGptService(credentials.ChatGPT_TOKEN)
bot = ApplicationBuilder().token(credentials.BOT_TOKEN).build()

# Зареєструвати обробник команди можна так:
# app.add_handler(CommandHandler('command', handler_func))
bot.add_handler(CommandHandler('start',start))
bot.add_handler(CommandHandler('random', random))
bot.add_handler(CommandHandler('gpt', gpt))
bot.add_handler(CommandHandler('talk', talk))

# Зареєструвати обробник колбеку можна так:
# app.add_handler(CallbackQueryHandler(app_button, pattern='^bot_.*'))
bot.add_handler(CallbackQueryHandler(default_callback_handler))
bot.run_polling()
