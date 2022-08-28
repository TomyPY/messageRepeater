import logging
from telegram_helper import bot
import asyncio
from recurrent_handler import create_new_message
import datetime
from models import RecurrentMessage

async def main():
    try:
        bot.infinity_polling()

    except:
        print('There was an error executing the bot')

if __name__=='__main__':
    bot.infinity_polling()