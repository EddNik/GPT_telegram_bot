
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler, MessageHandler,filters, ConversationHandler

from gpt import ChatGptService
from util import (load_message, send_text, send_image, show_main_menu, send_text_buttons,
                   load_prompt, Dialog)

import credentials

MENU, OPTION1, OPTION2 = range(3)
async def default_callback_handler(update: Update,
                                   context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    query = update.callback_query.data
    # if query == 'start':
    #     await start(update, context)
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
    print('start message')
    # await update.callback_query.answer()
    # command = update.callback_query.data
    text = load_message('main')
    await send_image(update, context, 'main')
    keyboard = [
        [InlineKeyboardButton("Option 1", callback_data="option1")],
        [InlineKeyboardButton("Option 2", callback_data="option2")],
        [InlineKeyboardButton("Option 2", callback_data="option2")],
        [InlineKeyboardButton("Option 2", callback_data="option2")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Welcome! Please choose an option:", reply_markup=reply_markup
    )
    
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
    return MENU

# async def app_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Random message")
    dialog.mode = "random"
    text = load_message('random')
    await send_image(update, context,'random')
    await send_text(update, context, text)
    prompt = load_prompt('random')
    # content = await chat_gpt.send_question(prompt, 'Дай цікавий факт' )
    # await send_text(update, context, content)

    text = load_message('thanksgiving')
    print(text)
    content = await chat_gpt.send_question(text, 'Thank you')
    print(text)
    await send_text_buttons(update, context, content,
                            {'bot_random_btn_request': 'Give me more facts', 'bot_random_btn_exit': 'Exit'})

async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "gpt"
    # print('gpt message')

    # await send_text(update, context, text)
    # prompt = load_prompt('gpt')

    text = load_message('gpt')
    await send_image(update, context, 'gpt')
    await send_text_buttons(update, context, text,
    #                         {'bot_gpt_btn_promt': 'Type your question again',       'bot_gpt_btn_exit': 'Exit'})
                            {'bot_gpt_btn_exit': 'Exit'})
    # message_type = update.message.chat.type
    # text = update.message.text
    # # await update.message.reply_text(text)
    # time.sleep(15)
    text = update.message.text
    await update.message.reply_text(f"You sent: {text}. Now send something else.")
    # await update.message.reply_text('I am GPT please enter your request')
    # time.sleep(5)

    # print(text)
    # await update.message.reply_text(text)
    await chat_gpt.add_message(text)
    answer = await chat_gpt.send_message_list()
    # print(answer)
    # user_text = update.message.from_user.username
    await send_text(update, context, answer)

    # content = await chat_gpt.send_question(prompt, 'Give my horoscope information')
    # content = await chat_gpt.send_question(prompt, text)
    # await send_text(update, context, content)

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
