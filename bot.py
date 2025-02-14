from pydantic.v1.validators import pattern_validator
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler, MessageHandler,
    filters, ConversationHandler, CallbackContext)


from gpt import ChatGptService
from util import (load_message, send_text, send_image, show_main_menu, send_text_buttons,
                  load_prompt, Dialog, send_html)

import credentials
import re

# MENU, talk_cobain, talk_hawking, talk_nietzsche, talk_queen = range(5)
# async def default_callback_handler(update: Update,
#                                    context: ContextTypes.DEFAULT_TYPE):
#     await update.callback_query.answer()
#     query = update.callback_query.data
#     if query == "bot_random_btn_request":
#         await random(update, context)
#     elif query == "bot_random_btn_exit":
#         await start(update, context)
#     elif query == "bot_gpt_btn_exit":
#         await start(update, context)

'''main menu'''
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

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "random"
    text = load_message('random')
    await send_image(update, context,'random')
    await send_text(update, context, text)
    prompt = load_prompt('random')
    content = await chat_gpt.send_question(prompt, 'Дай цікавий факт')
    await send_text(update, context, content)
    await send_text_buttons(update, context, content,
                            {'random_btn_request': 'Хочу ще факт', 'exit_btn': 'Закінчити'})


async def gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dialog.mode = "gpt"
    await send_image(update, context, 'gpt')
    text = update.message.text
    await update.message.reply_text(f"You sent: {text}. Wait for answer please.")
    await chat_gpt.add_message(text)
    answer = await chat_gpt.send_message_list()
    await send_text(update, context, answer)
    text = load_message('gpt')
    await send_text_buttons(update, context, text,
                            {'exit_btn': 'Закінчити'})


async def talk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    func_name = talk.__name__
    dialog.set_name(func_name)
    # print(dialog.mode)
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
async def talk_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = await chat_gpt.add_message('Hello. Tell me your name?')
    await send_text(update, context, answer)

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
        dialog.mode = "quiz"
        # print(dialog.mode)
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
                                 'quiz_more': 'Ще питання на обрану тему',
                                 'exit_btn': 'Закінчити'
                                 })


'''text of user's request to the bot processing'''
async def handler_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await chat_gpt.add_message(text)
    answer = await chat_gpt.send_message_list()
    await send_text_buttons(update, context, answer,
                            {'exit_btn': 'Закінчити'})

'''Bot buttons processing'''
async def button_talk(update: Update,
                 context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    query = update.callback_query.data
    await send_image(update, context, f'{query}')
    chat_gpt.set_prompt(load_prompt(f'{query}'))
    #
    # if query == 'talk_cobain':
    #     print('test')
    #     await send_image(update, context, 'talk_cobain')
    #     chat_gpt.set_prompt(load_prompt('talk_cobain'))
    # elif query == 'talk_hawking':
    #         print('test')
    #         await send_image(update, context, 'talk_hawking')
    #         chat_gpt.set_prompt(load_prompt('talk_hawking'))
    # elif query == 'talk_nietzsche':
    #         print('test')
    #         await send_image(update, context, 'talk_nietzsche')
    #         chat_gpt.set_prompt(load_prompt('talk_nietzsche'))
    # elif query == 'talk_queen':
    #         print('test')
    #         await send_image(update, context, 'talk_queen')
    #         chat_gpt.set_prompt(load_prompt('talk_queen'))
    # elif query == 'talk_tolkien':
    #         print('test')
    #         await send_image(update, context, 'talk_tolkien')
    #         chat_gpt.set_prompt(load_prompt('talk_tolkien'))
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
    query = update.callback_query.data
    content = await chat_gpt.send_question(load_prompt('quiz'), f'{query}')
    await send_text(update, context, content)



# async def cancel(update: Update, context: CallbackContext) -> int:
#     await update.message.reply_text("Operation cancelled.")
#     return ConversationHandler.END

dialog = Dialog('default')
dialog.mode = "default"

chat_gpt = ChatGptService(credentials.ChatGPT_TOKEN)
bot = ApplicationBuilder().token(credentials.BOT_TOKEN).build()

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
