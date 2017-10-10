"""
author = pranaylikhitkar
created_on = 7th October 2017
Train Status BOT for Telegram
Refer to the Guide https://core.telegram.org/bots#3-how-do-i-create-a-bot
"""
import time
from time import gmtime, strftime
import sys
import json
import requests
import telepot
from telepot.loop import MessageLoop

"""We will take the token for the BOT from the command line."""

"""Constants"""

TOKEN = sys.argv[1] #TOKEN from BOT Father
R_TOKEN = sys.argv[2] #TOKEN from Indian Railways API
COM_STRING = ['Sorry but I don\'t accepts anything other than valid texts.','Press:\n /pnr to Query your PNR number. \n/status to Query your Train Status.']
TODAY = strftime('%d-%m-%Y', gmtime())

#Methods

def handle(msg):
    """Handle function for the BOT to handle communication"""
    global content_type, chat_type, chat_id
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)
    if content_type == 'text':
        u_response = msg['text'] 
        print u_response
        #User Response
        if u_response == '/start':
            BOT.sendMessage(chat_id, COM_STRING[1])
        elif len(u_response) == 5:
            try:
                int(u_response)
                BOT.sendMessage(chat_id, 'Train Number Received')
                rail(u_response)
            except ValueError:
                print False
                BOT.sendMessage(chat_id, "Sorry but that doesn't look like a Valid Train/PNR Number.")    
        elif u_response == '/pnr':
            BOT.sendMessage(chat_id,'PNR Selected. Please send me your PNR Number')
        elif len(u_response) == 10:
            try:
                int(u_response)
                print True
                BOT.sendMessage(chat_id, 'PNR Received')
                pnr(u_response)
            except ValueError:
                print False
                BOT.sendMessage(chat_id, "This doesn't look like a Valid PNR Number")
        else:
            BOT.sendMessage(chat_id, "Send me the Train Number")
    elif content_type != 'text':
        BOT.sendMessage(chat_id, COM_STRING[0])    
            
def rail(t_no):
    """API Call to Indian Railway for Status"""
    url = "http://api.railwayapi.com/v2/live/train/" + t_no + "/date/10-10-2017/apikey/ga2a99h2j1/"
    request = requests.get(url)
    json_data = request.content
    obj = json.loads(json_data)

    if (obj['response_code'] == 200):
        print "Success"
        print obj['position']
        BOT.sendMessage(chat_id, obj['position'])

    elif obj['response_code'] == 210:
        print "Train Doesn't have a run Today."
        BOT.sendMessage(chat_id, "Train Doesn't have a run Today.")

    elif obj['response_code'] == 220:
        print "Flushed PNR"
        BOT.sendMessage(chat_id, "Flushed PNR")

    elif obj['response_code'] == 704:
        print "Contact Admin @pranaylikhitkar to renew account."
        BOT.sendMessage(chat_id, "Contact Admin @pranaylikhitkar to renew account..")

    elif obj['response_code'] == 504:
        print "Argument Error"
        BOT.sendMessage(chat_id, "Argument Error")

    else:
        print "Something went Wrong. Contacting Administrator."
        BOT.sendMessage(chat_id, "Something went Wrong. Contact Administrator. @pranaylikhitkar")

def pnr(pnr_no):
    """API Call for PNR"""
    url = "http://api.railwayapi.com/v2/live/train/" + pnr_no + "/date/10-10-2017/apikey/ga2a99h2j1/"
    request = requests.get(url)
    json_data = request.content
    obj = json.loads(json_data)

    if (obj['response_code'] == 200):
        print "Success"
        BOT.sendMessage(chat_id, "Date Of Journey" + obj['doj'] + "\nFrom Station : " + obj['from_station'] + "\To Station : "+ obj['to_station'])
    
    elif obj['response_code'] == 221:
        print "Train Doesn't have a run Today."
        BOT.sendMessage(chat_id, "Invalid PNR")

    elif obj['response_code'] == 220:
        print "Flushed PNR"
        BOT.sendMessage(chat_id, "Flushed PNR")
    elif obj['response_code'] == 304:
        print "Data Couldn't be fetched no Data Available"
        BOT.sendMessage(chat_id, "Data Couldn't be fetched no Data Available")
    elif obj['response_code'] == 504:
        print "Argument Error"
        BOT.sendMessage(chat_id, "Argument Error")
    elif obj['response_code'] == 704:
        print "Out of tokens"
        BOT.sendMessage(chat_id, "Contact Admin @pranaylikhitkar to renew account.")
    else:
        print "Something went Wrong. Contact Administrator. @pranaylikhitkar"
        BOT.sendMessage(chat_id, "Something went wrong. Contact Administrator @pranaylikhitkar")

BOT = telepot.Bot(TOKEN)
MessageLoop(BOT, handle).run_as_thread()
print "Listening"
while True:
    time.sleep(10)
