#code only works on python3
#Do not run when another bot instance is running

import os
import telebot
import requests
import json
import datetime
import time

#---------------------------------------------------------------------------------------------------------
#Only required to check if raspberry pi is back online after daily restart (currently set at 4am)

#wait 1 minute 
#time.sleep(60)

#send to personal "status" telegram group
#base_url = "https://api.telegram.org/bot6255924455:AAEnvWt8M7nCFhE5J0myrod-f_cbLBTJDSs/sendMessage"


#dt=datetime.datetime.now()
#parameters = {
    
#    "chat_id" : "-961147267",
#    "text" : "Raspberry Pi has successfully restarted at %s, %s"%(dt.date(),dt.strftime("%H:%M:%S"))
    
#}
#resp = requests.get(base_url, data = parameters)
#---------------------------------------------------------------------------------------------------------

BOT_TOKEN = "6255924455:AAEnvWt8M7nCFhE5J0myrod-f_cbLBTJDSs"

bot = telebot.TeleBot(BOT_TOKEN)

#print("Parade State bot initialised")

#For parade state poll
@bot.message_handler(commands=['new','rollcallplus'])
def rollcallplus(resp):
    dt= datetime.datetime.now()
    #print(dt.hour)
    if dt.hour > 12:
      dt= dt + datetime.timedelta(days=1)
      
    base_url = "https://api.telegram.org/bot6255924455:AAEnvWt8M7nCFhE5J0myrod-f_cbLBTJDSs/sendpoll"
    #Parameters based on https://core.telegram.org/bots/api
    parameters = {
      "chat_id" : resp.chat.id,
      "question" : "Parade State for %s/%s/%s \n(Tick ALL that are applicable)" % (dt.day,dt.month,dt.year) ,
      "options" : json.dumps(["In Office", "WFH", "L/L", "O/L", "CCL", "CSL", "PCL", "Others","(Tick this as well if only AM in Office)","(Tick this as well if only PM in Office)"]),
      "allows_multiple_answers" : True ,
      "is_anonymous" : False,
    }

    resp = requests.get(base_url, data = parameters)
    #print(resp.text)
    #print("Parade State triggered at", dt)

#For users curious on how to use
@bot.message_handler(commands=['help'])
def send_help(message):
    dt=datetime.datetime.now()
    bot.reply_to(message, "Commands: \n/new - Create New Poll for Parade State\n/help - List of Commands \n/ping - Check if server still online \n\nFor any other issues, contact @ncf3535 ")
    #print("Help triggered at", dt)

#Check if server is online
@bot.message_handler(commands=['ping'])
def ping(ping):
    dt=datetime.datetime.now()
    bot.reply_to(ping, "Server is still online as of %s, %s"%(dt.date(),dt.strftime("%H:%M:%S")))
    #print("Ping triggered at", dt)

bot.infinity_polling()