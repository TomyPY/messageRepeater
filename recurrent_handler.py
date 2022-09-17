import telebot
import asyncio
from config import TELEGRAM_TOKEN
import datetime
from models import RecurrentMessage

bot=telebot.TeleBot(TELEGRAM_TOKEN)

async def create_new_message():
    while True:
        await asyncio.sleep(1)
        print('a')
            # print('row')
            # data=RecurrentMessage().read()
            # last_delay=0
            # for row in data:
            #     print(row)
            #     try:
            #         delay=int(row[3])*60-last_delay
            #         if delay<0:
            #             delay=0
            #         await asyncio.sleep(delay-last_delay)
            #         print((int(row[4])))
            #         bot.send_message(int(row[4]), row[2])
            #         last_delay=delay
            #     except:
            #         print("The chat doesnt exist!")


# async def send_message(item):
#     while True:
#         print(item[1], 'is waiting to send the message')
#         await asyncio.sleep(int(item[3]))

#         exists=False
#         data=RecurrentMessage().read()

#         for row in data:
#             if int(item[0])==int(row[0]) and item[1]==row[1]:
#                 exists=True
        
#         if exists==False:
#             print(item[1], "Now is not sending messages anymore")
#             break
        