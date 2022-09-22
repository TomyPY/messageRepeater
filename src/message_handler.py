from telebot.async_telebot import AsyncTeleBot
import pytz

from config import TELEGRAM_TOKEN
from models import RecurrentMessage

from datetime import datetime, timedelta
import calendar
import asyncio
import traceback


bot=AsyncTeleBot(TELEGRAM_TOKEN)


async def manage_messages():
    
    RecurrentMessage()
    current_sec = int(datetime.now().strftime("%S"))
    delay=0

    if current_sec!=0:
        delay=60-current_sec
    
    


    while True:
            data=RecurrentMessage().read()
            if len(data)>0:
                for message in data:
                    try:
                        weekdays=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
                        
                        now=datetime.now(pytz.timezone("Asia/Calcutta")).replace(tzinfo=None) #TODAY DATETIME
                        
                        weekday=calendar.day_name[(now.weekday())] #TODAY DAY
                        chat_id=int(message[4]) #CHAT_ID OF RECEPTOR

                        #IF IS NOT THE TIME TO SEND THE MESSAGE, SKIP
                        if message[10]!=None:
                            pass
                            if now<datetime.strptime(message[10], "%Y-%m-%d %H:%M:%S.%f"):
                                #print("Skiping... delay is not ready")
                                continue
                        
                        #start time and endtime manage
                        if message[5]!=None:
                            if message[9]=='daily':
                                if message[10]==None:
                                    #print(datetime.strptime(message[5]+':00', "%H:%M:%S"), datetime.strptime(now.strftime("%H:%M:%S"), "%H:%M:%S"), '-----', datetime.strptime(message[5]+':10', "%H:%M:%S"), datetime.strptime(now.strftime("%H:%M:%S"), "%H:%M:%S"))
                                    if datetime.strptime(message[5]+':00', "%H:%M:%S")>datetime.strptime(now.strftime("%H:%M:%S"), "%H:%M:%S") or datetime.strptime(message[5]+':10', "%H:%M:%S")<datetime.strptime(now.strftime("%H:%M:%S"), "%H:%M:%S"):
                                        #print("skiping not time")
                                        continue
                                else:
                                    if datetime.strptime(message[10], "%Y-%m-%d %H:%M%:S.%f")<now:
                                        continue
                            else:
                                start_time=datetime.strptime(message[5].split(" ")[0], "%H:%M")
                                end_time=datetime.strptime(message[5].split(" ")[1], "%H:%M")
                                now_time=datetime.strptime(now.strftime("%H:%M"), "%H:%M")

                                if start_time>now_time>end_time:
                                    #print("Skiping... not time to send the msg")
                                    continue

                        # DELETE OLD MESSAGES
                        if message[8]!=None and message[11]!='' and message[12]!=None:
                            if datetime.strptime(message[12], "%Y-%m-%d %H:%M:%S.%f")<=datetime.now(pytz.timezone("Asia/Calcutta")).replace(tzinfo=None):
                                message_id=message[11].split(" ")[0] if message[11].split(" ")[0]!='' else message[11].split(" ")[1]
                                try:
                                    await bot.delete_message(chat_id, int(message_id))
                                except:
                                    pass
                                
                                new_msg_ids=message[11].replace(str(message_id), "").strip()

                                RecurrentMessage().edit('destruction_ids', int(message[0]), new_msg_ids)

                        #SKIP IF ISNT THE DAY
                        if message[6]!="None":
                            weekdays=weekdays[weekdays.index(message[6].split(" ")[0].lower()):weekdays.index(message[6].split(" ")[1].lower())+1]
                            if weekday.lower() not in weekdays:
                                print("Skiping, is not the day")
                                continue

                        
                        
                        message_text=message[2]
                        msg=await bot.send_message(chat_id, message_text)

                        
                        if message[9]!='daily':
                            RecurrentMessage().edit('next_message',int(message[0]),(now+timedelta(minutes=int(message[3]))).strftime("%Y-%m-%d %H:%M:%S.%f"))
                            if message[11]!=None:
                                try:
                                    RecurrentMessage().edit('destruction_ids', int(message[0]), " ".join(new_msg_ids)+f" {msg.message_id}")
                                except:
                                    RecurrentMessage().edit('destruction_ids', int(message[0]), " ".join(message[11])+f" {msg.message_id}")
                            else:
                                RecurrentMessage().edit('destruction_ids', int(message[0]), msg.message_id)
                            
                            RecurrentMessage().edit('next_destruction', int(message[0]), (datetime.now(pytz.timezone("Asia/Calcutta")).replace(tzinfo=None)+timedelta(minutes=int(message[8]))).strftime("%Y-%m-%d %H:%M:%S.%f"))
                        else:
                            # RecurrentMessage().edit('next_message',int(message[0]),(now+timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S.%f"))
                            if message[11]!=None:
                                try:
                                    RecurrentMessage().edit('destruction_ids', int(message[0]), " ".join(new_msg_ids)+f" {msg.message_id}")
                                except:
                                    RecurrentMessage().edit('destruction_ids', int(message[0]), " ".join(message[11])+f" {msg.message_id}")
                            else:
                                RecurrentMessage().edit('destruction_ids', int(message[0]), msg.message_id)
                            
                            RecurrentMessage().edit('next_destruction', int(message[0]), (datetime.now(pytz.timezone("Asia/Calcutta")).replace(tzinfo=None)+timedelta(minutes=int(message[8]))).strftime("%Y-%m-%d %H:%M:%S.%f"))
                        
                    except Exception as e:
                        print(traceback.format_exc())

            await asyncio.sleep(10)