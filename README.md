# Edd-Bot_GPT
Edd-Bot_GPT bot is a simple and easy-to-use conversational AI-assistant.

It provides the ability to interact with the bot, ask any questions, communicate with some famous people, 
and play a quiz on three topics: Python programming, Mathematical theories and Biology topic .

## Features

###### Selection people for conversation and topic to for quiz

###### Calculation of test results and their reset if necessary

###### Logging. In file bot_quiz.log

## Requirements
Python 3.x installed

Install necessary Python packages using the requirements.txt file

`pip install -r requirements.txt`

## Credentials

###### BOT_TOKEN: Your Telegram Bot Token which can be obtained from BotFather.

###### ChatGPT_TOKEN: Your OpenAI API Key, which can be found on the OpenAI Dashboard.

#### Usage

PyCharm:

set in .env file:
* BOT_TOKEN="your_telegram_token"
* ChatGPT_TOKEN="your_openai_token"

Linux:
* export BOT_TOKEN=your_telegram_token
* export ChatGPT_TOKEN=your_openai_token

Windows:
1. To add/change an environment variable permanently in Windows
2. Launch "Control Panel"
3. "System"
4. "Advanced system settings"
5. Switch to "Advanced" tab
6. "Environment variables"
7. Choose "System Variables" (for all users)
8. To add a new environment variable:
   * Choose "New"
   * Enter the variable "BOT_TOKEN" and "your_telegram_token".
   * Enter the variable "ChatGPT_TOKEN" and "your_openai_token".