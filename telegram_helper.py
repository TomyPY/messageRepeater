from exceptions import *
from config import TELEGRAM_TOKEN, location
from models import RecurrentMessage

from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.types import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply)
from telebot.asyncio_storage import StateMemoryStorage
from telebot.asyncio_handler_backends import State, StatesGroup

import asyncio
import aioschedule
import datetime
import pytz
import calendar

bot=AsyncTeleBot(TELEGRAM_TOKEN, state_storage=StateMemoryStorage())

chat={}

weekdays=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


class MyStates(StatesGroup):
    title_always = State() 
    message_always = State()
    delay_always = State()
    only_in_always = State()
    time_always = State()
    destruction_always = State()

    column_row_id = State()
    changes = State()

    title_days = State() 
    message_days = State()
    delay_days = State()
    only_in_days = State()
    time_days = State()
    days_days = State()
    destruction_days = State()


    title_daily = State() 
    message_daily = State()
    delay_daily = State()
    only_in_daily = State()
    time_daily = State()
    days_daily = State()
    destruction_daily = State()
    

async def activate():
    time=0
    while True:
        await aioschedule.run_pending()
        if time%5==0:
            print(aioschedule.jobs)
            
        time+=1
        await asyncio.sleep(1)

async def send_message(arr):
    try:
        if 'stop_bot' not in chat:
            chat['stop_bot']=False

        if chat['stop_bot']==False:
            
                if arr[-1]=='days':
                    chat_id=int(arr[4])
                    message=arr[2]
                    if arr[7].lower()=='off':
                        notification=True
                    else:
                        notification=False

                    destruction_time=int(arr[8])

                    tz=pytz.timezone('Asia/Calcutta')
                    start_time=datetime.datetime.strptime(arr[5].split(" ")[0], '%H:%M').replace(year=1, month=1, day=1, tzinfo=tz)
                    end_time=datetime.datetime.strptime(arr[5].split(" ")[1], '%H:%M').replace(year=1, month=1, day=1, tzinfo=tz)
                    now=datetime.datetime.now(pytz.timezone('Asia/Calcutta'))
                    
                    send_weekdays=weekdays[weekdays.index(arr[6].split(" ")[0].lower()):weekdays.index(arr[6].split(" ")[1].lower())+1]

                    today=calendar.day_name[(datetime.datetime.utcnow()+datetime.timedelta(hours=5, minutes=30)).weekday()]

                    if today.lower() in send_weekdays:
                        if now.time()>=start_time.time():
                            if end_time.time()>=now.time():
                                msg=await bot.send_message(int(chat_id), message, disable_notification=notification)
                                aioschedule.every(int(destruction_time)).minutes.do(delete_message, msg=[msg.chat.id, msg.message_id])

                elif arr[-1]=='allways':
                    chat_id=int(arr[4])
                    message=arr[2]
                    if arr[7].lower()=='off':
                        notification=True
                    else:
                        notification=False
                    
                    destruction_time=arr[8]

                    tz=pytz.timezone('Asia/Calcutta')
                    start_time=datetime.datetime.strptime(arr[5].split(" ")[0], '%H:%M').replace(year=1, month=1, day=1, tzinfo=tz)
                    end_time=datetime.datetime.strptime(arr[5].split(" ")[1], '%H:%M').replace(year=1, month=1, day=1, tzinfo=tz)

                    now=datetime.datetime.now(pytz.timezone('Asia/Calcutta'))

                    if now.time()>=start_time.time():
                        if end_time.time()>=now.time():
                            msg=await bot.send_message(int(chat_id), message, disable_notification=notification)
                            aioschedule.every(int(destruction_time)).minutes.do(delete_message, msg=[msg.chat.id, msg.message_id])

                elif arr[-1]=='daily':
                    print(arr)
                    chat_id=int(arr[4])
                    message=arr[2]

                    if arr[7].lower()=='off':
                        notification=True
                    else:
                        notification=False

                    destruction_time=arr[8]

                    send_weekdays=weekdays[weekdays.index(arr[6].split(" ")[0].lower()):weekdays.index(arr[6].split(" ")[1].lower())+1]
                    today=calendar.day_name[(datetime.datetime.utcnow()+datetime.timedelta(hours=5, minutes=30)).weekday()]

                    if today.lower() in send_weekdays:
                        msg=await bot.send_message(int(chat_id), message, disable_notification=notification)
                        aioschedule.every(int(destruction_time)).minutes.do(delete_message, msg=[msg.chat.id, msg.message_id])
                    
        else:
            pass
    except Exception as e:
        print('send_message',e)

async def run_one_time():
    try:
        data=RecurrentMessage().read()
        chat['scheduled_tasks']={}
        for i in data:
            if i[-1]=='daily':
                scheduled_task=aioschedule.every().day.at(i[5]).do(send_message, arr=i)
                chat['scheduled_tasks'][int(i[0])]=scheduled_task
            elif i[-1]=='days':
                scheduled_task=aioschedule.every(int(i[3])).minutes.do(send_message, arr=i)
                chat['scheduled_tasks'][int(i[0])]=scheduled_task
            elif i[-1]=='allways':
                scheduled_task=aioschedule.every(int(i[3])).minutes.do(send_message, arr=i)
                chat['scheduled_tasks'][int(i[0])]=scheduled_task
        print(chat['scheduled_tasks'])
    except Exception as e:
        print(e)

async def delete_message(msg):
    await bot.delete_message(msg[0], msg[1])
    return aioschedule.CancelJob

@bot.message_handler(func=lambda message:message.text.lower().split("@")[0]=="/start")
async def welcome_and_explanation(message):
    cid=message.chat.id

    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add('/create_message_allways', '/create_message_days', '/create_message_daily', '/show_messages', '/delete_message', '/edit_message')
    await asyncio.sleep(2)
    await bot.send_message(cid, "Hello! i'm a bot to handle your messages! Go to /help section to see all the commands",reply_markup=markup)
    
@bot.message_handler(commands=['help'])
async def all_commands(message):
    await bot.send_message(message.chat.id, "________💫All commands💫________\n\n-/create_message_always - Create a message that works 24/7 has the ability of set a starter time and end time\n\n-/create_message_days - Create a message that works one or more days. To set to one day use monday monday or friday friday\n\n-/create_message_daily - Create a message that it sent daily at a certain time\n\n-/show_messages - To see all the active messages\n\n-/delete_message - to delete a message from the database\n\n-/edit_message - To edit a specific message from the database\n\n-/stop_bot - To stop all the schedule messages\n\n-/start_bot - To start all the schedule messages")

@bot.message_handler(state="*", commands='create_message_allways')
async def ask_title(message):
    cid=message.chat.id
    msg=message.text
    chat[cid]={}

    await bot.send_message(cid, "Set a title to indentify this task!")
    await bot.set_state(message.from_user.id, MyStates.title_always, message.chat.id)

@bot.message_handler(state=MyStates.title_always)
async def ask_message(message):
    try:
        cid=message.chat.id
        msg=message.text
        chat[cid]['title']=msg


        if chat[cid]['title'].lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return


        await bot.send_message(cid, "Excellent!")
        await bot.send_message(cid, "What message do you want to send?")
        await bot.set_state(message.from_user.id, MyStates.message_always, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['title'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.message_always)
async def ask_delay(message):
    try:
        cid=message.chat.id
        msg=message.text
        chat[cid]['message']=msg


        if chat[cid]['message'].lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return


        await bot.send_message(cid, "We are almost done!")
        await bot.send_message(cid, "What delay do you want between the messages?")
        await bot.set_state(message.from_user.id, MyStates.delay_always, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['message'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)
        
@bot.message_handler(state=MyStates.delay_always)
async def ask_only_in(message):
    try:
        cid=message.chat.id
        msg=message.text
        chat[cid]['delay']=msg


        if chat[cid]['delay'].lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return


        await bot.send_message(cid, "Almost..")
        await bot.send_message(cid, "Can you give me id of the channel/group?")
        await bot.set_state(message.from_user.id, MyStates.only_in_always, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['delay'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.only_in_always)
async def ask_destruction(message):
    try:
        cid=message.chat.id
        msg=message.text
        chat[cid]['row_only_in']=msg


        if chat[cid]['row_only_in'].lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return

        int(chat[cid]['row_only_in'])

        await bot.send_message(cid, "Almost..")
        await bot.send_message(cid, "Give me a self destruction time in minutes")
        await bot.set_state(message.from_user.id, MyStates.destruction_always, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['destruction'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.destruction_always)
async def ask_time(message):
    try:
        cid=message.chat.id
        msg=message.text

        if msg.lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return

        int(msg)

        chat[cid]['destruction']=msg

        await bot.send_message(cid, "Finally..")
        await bot.send_message(cid, "Please specify a time, Ex: 7:00 21:00 or write 'default' to put it as default (12:00 21:00)")
        await bot.set_state(message.from_user.id, MyStates.time_always, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['only_in'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.time_always)
async def save_data(message):
    try:

        cid=message.chat.id
        msg=message.text
        
        if msg.lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return

        if msg.lower()=='default':
            start_time=datetime.datetime.strptime('12:00', "%H:%M")
            end_time=datetime.datetime.strptime('21:00', "%H:%M")
        
            start_time_final=datetime.datetime.strftime(start_time, "%H:%M")
            end_time_final=datetime.datetime.strftime(end_time, "%H:%M")

            chat[cid]['time']=start_time_final+" "+end_time_final
        else:
            start_time=datetime.datetime.strptime(msg.split(" ")[0], "%H:%M")
            end_time=datetime.datetime.strptime(msg.split(" ")[1], "%H:%M")
        
            start_time_final=datetime.datetime.strftime(start_time, "%H:%M")
            end_time_final=datetime.datetime.strftime(end_time, "%H:%M")

            chat[cid]['time']=start_time_final+" "+end_time_final
        
        await bot.send_message(message.chat.id, f"Ready, take a look:\n<b>Title: {chat[cid]['title']}\nMessage: {chat[cid]['message']}\nDelay: {chat[cid]['delay']}\nOnly_in: {chat[cid]['row_only_in']}\nTime: {msg}\nNotification: On\nDestruction: {chat[cid]['destruction']}\nType: Allways</b>", parse_mode="html")

        item=(
            len(RecurrentMessage().read())+1,
            chat[cid]['title'],
            chat[cid]['message'],
            chat[cid]['delay'],
            chat[cid]['row_only_in'],
            chat[cid]['time'],
            'None',
            'On',
            chat[cid]['destruction'],
            'allways'
            )

        scheduled_task=aioschedule.every(int(chat[cid]['delay'])).minutes.do(send_message, arr=item)
        chat['scheduled_tasks'][len(RecurrentMessage().read())+1]=scheduled_task

        await bot.delete_state(message.from_user.id, message.chat.id)

        RecurrentMessage().insert(item)

    except Exception as e:
        await bot.send_message(cid, e)


@bot.message_handler(state="*", commands='create_message_days')
async def ask_title_days(message):
    cid=message.chat.id
    msg=message.text
    chat[cid]={}

    await bot.send_message(cid, "Set a title to indentify this task!")
    await bot.set_state(message.from_user.id, MyStates.title_days, message.chat.id)

@bot.message_handler(state=MyStates.title_days)
async def ask_message_days(message):
    try:
        cid=message.chat.id
        msg=message.text
        chat[cid]['title']=msg


        if chat[cid]['title'].lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return


        await bot.send_message(cid, "Excellent!")
        await bot.send_message(cid, "What message do you want to send?")
        await bot.set_state(message.from_user.id, MyStates.message_days, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['title'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.message_days)
async def ask_delay_days(message):
    try:
        cid=message.chat.id
        msg=message.text
        chat[cid]['message']=msg


        if chat[cid]['message'].lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return


        await bot.send_message(cid, "We are almost done!")
        await bot.send_message(cid, "What delay do you want between the messages?")
        await bot.set_state(message.from_user.id, MyStates.delay_days, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['message'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.delay_days)
async def ask_only_in_days(message):
    try:
        cid=message.chat.id
        msg=message.text
        chat[cid]['delay']=msg


        if chat[cid]['delay'].lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return


        await bot.send_message(cid, "Almost..")
        await bot.send_message(cid, "Can you give me id of the channel/group?")
        await bot.set_state(message.from_user.id, MyStates.only_in_days, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['delay'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.only_in_days)
async def ask_destruction(message):
    try:
        cid=message.chat.id
        msg=message.text
        chat[cid]['row_only_in']=msg


        if chat[cid]['row_only_in'].lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return

        int(chat[cid]['row_only_in'])

        await bot.send_message(cid, "Almost..")
        await bot.send_message(cid, "Give me a self destruction time in minutes")
        await bot.set_state(message.from_user.id, MyStates.destruction_days, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['destruction'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.destruction_days)
async def ask_time_days(message):
    try:
        cid=message.chat.id
        msg=message.text
        chat[cid]['destruction']=msg

        if chat[cid]['destruction'].lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return

        await bot.send_message(cid, "You're doing it right...")
        await bot.send_message(cid, "Please specify a time, Ex: 7:00 21:00 or write 'default' to put it as default (12:00 21:00)")
        await bot.set_state(message.from_user.id, MyStates.time_days, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['only_in'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.time_days)
async def ask_days_days(message):
    try:
        cid=message.chat.id
        msg=message.text

        if msg.lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return
        
        if msg.lower()=='default':
            start_time=datetime.datetime.strptime('12:00', "%H:%M")
            end_time=datetime.datetime.strptime('21:00', "%H:%M")
        
            start_time_final=datetime.datetime.strftime(start_time, "%H:%M")
            end_time_final=datetime.datetime.strftime(end_time, "%H:%M")

            chat[cid]['time']=start_time_final+" "+end_time_final
        else:
            start_time=datetime.datetime.strptime(msg.split(" ")[0], "%H:%M")
            end_time=datetime.datetime.strptime(msg.split(" ")[1], "%H:%M")
        
            start_time_final=datetime.datetime.strftime(start_time, "%H:%M")
            end_time_final=datetime.datetime.strftime(end_time, "%H:%M")

            chat[cid]['time']=start_time_final+" "+end_time_final

        chat[cid]['time_IST']=msg


        await bot.send_message(cid, "Finally!")
        await bot.send_message(cid, "Please specify a lapse of days, Ex: Monday Friday")
        await bot.set_state(message.from_user.id, MyStates.days_days, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['only_in'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.days_days)
async def save_data_days(message):
    try:

        cid=message.chat.id
        msg=message.text

        if msg.lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return

        chat[cid]['days']=msg
        
        await bot.send_message(message.chat.id, f"Ready, take a look:\n<b>Title: {chat[cid]['title']}\nMessage: {chat[cid]['message']}\nDelay: {chat[cid]['delay']}\nOnly_in: {chat[cid]['row_only_in']}\nTime: {chat[cid]['time_IST']}\nDays: {chat[cid]['days']}\nNotification: On\nDestruction: {chat[cid]['destruction']}\nType: Days</b>", parse_mode="html")

        item=(
            len(RecurrentMessage().read())+1,
            chat[cid]['title'],
            chat[cid]['message'],
            chat[cid]['delay'],
            chat[cid]['row_only_in'],
            chat[cid]['time'],
            chat[cid]['days'],
            'On',
            chat[cid]['destruction'],
            'days'
            )

        scheduled_task=aioschedule.every(int(chat[cid]['delay'])).minutes.do(send_message, arr=item)
        chat['scheduled_tasks'][len(RecurrentMessage().read())+1]=scheduled_task

        await bot.delete_state(message.from_user.id, message.chat.id)

        RecurrentMessage().insert(item)

    except Exception as e:
        await bot.send_message(cid, e)


@bot.message_handler(state="*", commands='create_message_daily')
async def ask_title_daily(message):
    cid=message.chat.id
    msg=message.text
    chat[cid]={}

    await bot.send_message(cid, "Set a title to indentify this task!")
    await bot.set_state(message.from_user.id, MyStates.title_daily, message.chat.id)

@bot.message_handler(state=MyStates.title_daily)
async def ask_message_daily(message):
    try:
        cid=message.chat.id
        msg=message.text
        chat[cid]['title']=msg


        if chat[cid]['title'].lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return


        await bot.send_message(cid, "Excellent!")
        await bot.send_message(cid, "What message do you want to send?")
        await bot.set_state(message.from_user.id, MyStates.message_daily, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['title'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.message_daily)
async def ask_delay_daily(message):
    try:
        cid=message.chat.id
        msg=message.text
        chat[cid]['message']=msg


        if chat[cid]['message'].lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return


        await bot.send_message(cid, "We are almost done!")
        await bot.send_message(cid, "At what time of the day do you want to send the messages? Ex: 01:09")
        await bot.set_state(message.from_user.id, MyStates.delay_daily, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['message'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.delay_daily)
async def ask_only_in_days(message):
    try:
        cid=message.chat.id
        msg=message.text

        if msg.lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return

        time=datetime.datetime.strptime(msg, '%H:%M')
        time_final=time-datetime.timedelta(hours=5, minutes=30)
        chat[cid]['time']=datetime.datetime.strftime(time_final, '%H:%M')

        chat[cid]['time_IST']=msg

        await bot.send_message(cid, "Finally..")
        await bot.send_message(cid, "Can you give me id of the channel/group?")
        await bot.set_state(message.from_user.id, MyStates.only_in_daily, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['delay'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.only_in_daily)
async def ask_destruction_days(message):
    try:
        cid=message.chat.id
        msg=message.text
        chat[cid]['only_in']=msg

        if chat[cid]['only_in'].lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return

        int(chat[cid]['only_in'])

        await bot.send_message(cid, "Almost..")
        await bot.send_message(cid, "Give me a self destruction time in minutes")
        await bot.set_state(message.from_user.id, MyStates.destruction_daily, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['destruction'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.destruction_daily)
async def ask_days_daily(message):
    try:
        cid=message.chat.id
        msg=message.text
        chat[cid]['destruction']=msg
        
        if chat[cid]['destruction'].lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return

        await bot.send_message(cid, "Finally...")
        await bot.send_message(cid, "Please specify a lapse of days, Ex: Monday Friday")
        await bot.set_state(message.from_user.id, MyStates.days_daily, message.chat.id)
        async with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['message'] = message.text
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.days_daily)
async def save_data_daily(message):
    try:

        cid=message.chat.id
        msg=message.text
        chat[cid]['days']=msg
        
        if msg.lower()=='cancel':
            await bot.send_message(cid, "Task cancelled")
            return
    
        await bot.send_message(message.chat.id, f"Ready, take a look:\n<b>Title: {chat[cid]['title']}\nMessage: {chat[cid]['message']}\nTime: {chat[cid]['time']}\nOnly_in: {chat[cid]['only_in']}\nNotification: True\nDestruction: {chat[cid]['destruction']}\nType: Daily</b>", parse_mode="html")

        item=(
            len(RecurrentMessage().read())+1,
            chat[cid]['title'],
            chat[cid]['message'],
            'None',
            chat[cid]['only_in'],
            chat[cid]['time'],
            chat[cid]['days'],
            'On',
            chat[cid]['destruction'],
            'daily'
            )
        
        scheduled_task=aioschedule.every().day.at(chat[cid]['time']).do(send_message, arr=item)
        chat['scheduled_tasks'][len(RecurrentMessage().read())+1]=scheduled_task

        await bot.delete_state(message.from_user.id, message.chat.id)

        RecurrentMessage().insert(item)

    except Exception as e:
        await bot.send_message(cid, e)


@bot.message_handler(func=lambda message:message.text.lower().split("@")[0]=="/show_messages")
async def show_recurrent_messages(message):
    try:
        cid=message.chat.id
        msg=message.text

        data=RecurrentMessage().read()
        txt=''

        if len(data)>0:
            for row in data:
                txt+=f'<b>Row_id: {row[0]} Title: {row[1]}  Delay: {row[3]}  Only_in: {row[4]} Time: {row[5]} Days: {row[6]} Notification: {row[7]} Destruction: {row[8]} Type: {row[-1]}\nMessage: {row[2]}</b>\n\n'

            await bot.send_message(cid, txt, parse_mode='HTML')

        else:
            await bot.send_message(cid, "There is no recurrent messages in the database yet")
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(func=lambda message:message.text.lower().split("@")[0].split(" ")[0]=="/delete_message")
async def delete_recurrent_messages(message):
    cid=message.chat.id
    msg=message.text
    try:
        if len(msg.split(" "))!=2:
            raise ParameterMissing("The correct format is: /delete_message row_id")
        else:

            row_id=int(msg.split(" ")[1])

            result=RecurrentMessage().delete(row_id)
       
            if result==False:
                await bot.send_message(cid, "The row doesn't exists or there was an error :(")
            else:
                await bot.send_message(cid, "The task was deleted successfully!")
                aioschedule.cancel_job(chat['scheduled_tasks'][int(row_id)])

           

    except ParameterMissing as e:
        await bot.send_message(cid, e)

@bot.message_handler(func=lambda message:message.text.lower().split("@")[0]=="/edit_message", state='*')
async def edit_recurrent_messages(message):
    cid=message.chat.id
    msg=message.text
    chat[cid]={}

    await bot.send_message(cid, "Please write the column name and row id in the next format: column row_id")
    await bot.set_state(message.from_user.id, MyStates.column_row_id, message.chat.id)

@bot.message_handler(state=MyStates.column_row_id)
async def new_cell_handler(message):
    try:
        cid=message.chat.id
        msg=message.text

        if message.text=='cancel':
            return

        chat[cid]["column"]=msg.split(" ")[0].lower()
        chat[cid]["row_id"]=msg.split(" ")[1].lower()

        await bot.send_message(cid, f"Awesome! Can you please write the new changes to {chat[cid]['column']}")
        await bot.set_state(message.from_user.id, MyStates.changes, message.chat.id)
    except ValueError as e:
        await bot.send_message(cid, e)

@bot.message_handler(state=MyStates.changes)
async def edit_message_handler(message):
    
    cid=message.chat.id
    msg=message.text

    chat[cid]['changes']=msg

    result=RecurrentMessage().edit(chat[cid]["column"], int(chat[cid]["row_id"]), chat[cid]['changes'])

    if result==False:
        await bot.send_message(cid, "Changes could not be saved due to an error")
    try:
        if chat[cid]["column"].lower()=='delay':
            aioschedule.cancel_job(chat['scheduled_tasks'][int(chat[cid]['row_id'])])
            data=RecurrentMessage().read()
            for i in data:
                if int(i[0])==int(chat[cid]["row_id"]):
                    scheduled_task=aioschedule.every(int(i[3])).minutes.do(send_message, arr=[i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]])
                    chat['scheduled_tasks'][int(chat[cid]["row_id"])]=scheduled_task
        
        elif chat[cid]["column"].lower()=='time':
            print(chat['scheduled_tasks'])
            await aioschedule.cancel_job(chat['scheduled_tasks'][int(chat[cid]['row_id'])])
            data=RecurrentMessage().read()
            for i in data:
                if int(i[0])==int(chat[cid]["row_id"]):
                    scheduled_task=aioschedule.every().day.at(i[5]).do(send_message, arr=[i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]])
                    chat['scheduled_tasks'][int(i[0])]=scheduled_task

        await bot.send_message(cid, "The task was edited successfully!")
        await bot.delete_state(message.from_user.id, message.chat.id)
    except Exception as e:
        await bot.send_message(cid, e)

@bot.message_handler(func=lambda message:message.text.lower().split("@")[0]=="/stop_bot", state='*')
async def stop_schedules(message):
    chat['stop_bot']=True
    await bot.send_message(message.chat.id, "The bot was stopped!")

@bot.message_handler(func=lambda message:message.text.lower().split("@")[0]=="/start_bot", state='*')
async def start_schedules(message):
    chat['stop_bot']=False
    await bot.send_message(message.chat.id, "The bot is running again!")

async def main():
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    await run_one_time()
    await asyncio.gather(bot.polling(non_stop=True, timeout=40), activate())

if __name__=='__main__':
    asyncio.run(main())