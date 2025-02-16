import sys
import traceback
from inspect import Traceback

from telegram import Update
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler, MessageHandler,
    filters)

from gpt import ChatGptService
from util import (load_message, send_text, send_image, show_main_menu, send_text_buttons,
                  load_prompt, Dialog)
from dotenv import load_dotenv

import credentials
import os
import openai
import logging

# Setting bot token environments from .env file
load_dotenv()

telegram_token = ''
try:
    telegram_token = os.environ.get('BOT_TOKEN')
except KeyError as e:
    print(f"{e} variable does not exist. Please set the {e} environment variable")

try:
    openai.api_key = os.environ.get('ChatGPT_TOKEN')

except  TypeError as e:
    print(f"{e} variable does not exist. Please set the {e} environment variable")

# print(telegram_token, openai.api_key)
# Logging:
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )



result, total = 0, 0
dialog = Dialog('start','undefined')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global result, total
    result, total = 0, 0
    dialog.set_mode('start')
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


async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.set_mode('random')
    text = load_message('random')
    await send_image(update, context,'random')
    await send_text(update, context, text)
    prompt = load_prompt('random')
    content = await chat_gpt.send_question(prompt, 'Дай ще цікавий факт')
    await send_text_buttons(update, context, content,
                            {'random_btn_request': 'Хочу ще факт', 'exit_btn': 'Закінчити'})


async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.set_mode('gpt')
    await send_image(update, context, 'gpt')
    text = load_message('gpt')
    await send_text(update, context, text)


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.set_mode('talk')
    text = load_message('talk')
    await send_image(update, context, 'talk')
    await show_main_menu(update, context, {
        'talk': 'Поговорити з відомою особистістю',
        'start': 'Головне меню'
            })
    await send_text_buttons(update, context, text,
                            {'talk_cobain': ' Курт Кобейн',
                             'talk_hawking': 'Стівен Гокінг',
                             'talk_nietzsche': 'Фрідріх Ніцше ',
                             'talk_queen': 'Єлизавета II',
                             'talk_tolkien': 'Джон Толкін'
                             })


# Checking who I'm connected to in a conversation
async def talk_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = await chat_gpt.add_message('Hello. Tell me your name?')
    await send_text(update, context, answer)


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
        dialog.set_mode('quiz')
        text = load_message('quiz')
        await send_image(update, context, 'quiz')
        await show_main_menu(update, context, {
            'quiz': 'Обери тему',
            'start': 'Головне меню'
        })
        await send_text_buttons(update, context, text,
                                {'quiz_prog': 'Тема програмування',
                                 'quiz_math': 'Тема математичних теорій',
                                 'quiz_biology': 'Тема біології ',
                                 'exit_btn': 'Закінчити'
                                 })


# text of the user's requests for GPT processing
async def handler_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    mode = dialog.get_mode()

    # You can send request only by button
    if mode == 'random' or mode == 'start':
        await update.message.reply_text(f"Ти ввів текст: {text}.  Користуйся кнопками або командами.")
        return
    elif mode == 'gpt':
        content = await chat_gpt.add_message(text)
        await send_text_buttons(update, context, content,
                                {'exit_btn': 'Закінчити'})
    elif mode == 'quiz':
        global total, result
        total += 1
        if total > 3 and result == 0 :
            await update.message.reply_text('Кількість спроб використано. Скористуйся кнопкою щоб отримати інше питання')
            return
        content = await chat_gpt.add_prompt_message(load_prompt('quiz_add_prompt'), text)
        if content == 'Правильно!':
            result += 1
        await send_text_buttons(update, context, content,
                                {'quiz_more': 'Ще питання на обрану тему', 'quiz_change': 'Змінити тему','exit_btn': 'Закінчити'})
        await send_image(update, context, 'score')
        await update.message.reply_text(f'Загальна кількість питань : {total}, Правильних відповідей : {result}')


    elif mode == 'talk':
        text = update.message.text
        answer = await chat_gpt.add_message(text)
        await send_text_buttons(update, context, answer,
                                {'talk_more':'Вибрати іншу особистість','exit_btn': 'Закінчити'})


# Bot buttons processing talk/random/quiz/Закінчити
async def button_talk(update: Update,
                 context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    query = update.callback_query.data

    if query == 'talk_more':
        await talk(update,context)
        return

    await send_image(update, context, f'{query}')
    chat_gpt.set_prompt(load_prompt(f'{query}'))

    # Checking who I'm connected to in a conversation
    await talk_conversation(update, context)


async def button_exit(update: Update,
                             context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)


async def button_random(update: Update,
                 context: ContextTypes.DEFAULT_TYPE):
    await random(update, context)


async def button_quiz(update: Update,
                 context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    query_in = update.callback_query.data

    if query_in == 'quiz_more':
        content = await chat_gpt.send_question(load_prompt('quiz'), f'{dialog.get_topic()}')
        await send_text(update, context, content)
    elif query_in == 'quiz_change':
        await quiz(update,context)
    else:
        dialog.set_topic(query_in)
        content = await chat_gpt.send_question(load_prompt('quiz'), f'{query_in}')
        await send_text(update, context, content)


chat_gpt = ChatGptService(openai.api_key)
bot = ApplicationBuilder().token(telegram_token).build()

# Зареєструвати обробник команди можна так:
bot.add_handler(CommandHandler('start',start))
bot.add_handler(CommandHandler('random', random))
bot.add_handler(CommandHandler('gpt', gpt))
bot.add_handler(CommandHandler('talk', talk))
bot.add_handler(CommandHandler('quiz', quiz))

bot.add_handler(MessageHandler(filters.TEXT, callback=handler_message))

# Зареєструвати обробник колбеку можна так:
bot.add_handler(CallbackQueryHandler(button_talk, pattern='^talk_.*'))
bot.add_handler(CallbackQueryHandler(button_random, pattern='^random_.*'))
bot.add_handler(CallbackQueryHandler(button_quiz, pattern='^quiz_.*'))
bot.add_handler(CallbackQueryHandler(button_exit, pattern='exit_btn'))
bot.run_polling()
