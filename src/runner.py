from telegram_helper import bot
from message_handler import manage_messages
from telebot import asyncio_filters
import asyncio

async def main():
    try:
        
        bot.add_custom_filter(asyncio_filters.StateFilter(bot))
        await asyncio.gather(bot.infinity_polling(), manage_messages())

    except Exception as e:

        print(f"The bot stops working cause an error: {e}")

if __name__=='__main__':
    asyncio.run(main())