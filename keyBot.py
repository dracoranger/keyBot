#keyBot
#By DracoRanger
import asyncio
import re
from datetime import datetime
from datetime import timedelta
from threading import Timer
import discord
from discord.ext import commands
#import logging

client = discord.Client()
bot = commands.Bot(command_prefix="!", description="")

BOT_FOLDER=""

config = open('botData.txt','r')
conf = config.readlines() #push to array or do directly
token = conf[0][:-1]
print(token)
keysName = conf[1][:-1]
print(keysName)
usedKeys = conf[2][:-1]
print(usedKeys)
channelNum = conf[3][:-1]
userComp = conf[4][:-1]

keyTakenToday=[]


# from https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day
#should clear the keyLimiter
x=datetime.today()
#y=x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
y=x + timedelta(days=1)
delta_t=y-x

secs=delta_t.seconds+1

def clear_keys_taken():
    global keyTakenToday
    keyTakenToday = []

t = Timer(secs, clear_keys_taken)
t.start()

@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    print(client.user.id)
    print('------')
    message = client.user.name + " is up and running!"
    await client.send_message(client.get_channel(channelNum), message)

@client.event
async def on_message(message):
    global channelNum
    if message.author == client.user:
        return
    if message.channel == client.get_channel(channelNum) or message.channel.is_private:
        '''
        prints the list of keys
        '''
        if message.content.startswith('!keylist'):
            keys = open(keysName, 'r')
            keylist = keys.readlines()
            keys.close()
            temp = ''
            for i in keylist:
                temp = temp+i.split(',')[0]+'\n'#should only show name
            if temp == '':
                temp = 'No keys in storage'
            await client.send_message(message.channel, temp)
        '''
        prints all commands
        '''
        if message.content.startswith('!help'):
            keylist = "!keylist = prints a list of games that have keys, works in either server or in pms"
            gib = "!gib [gameName] [key]= gives a key to the bot, only works in pms"
            take = "!take [gameName] = messages you with the game's key, works only in server, recieve key in pm, message posted to server"
            ret = keylist+'\n'+gib+'\n'+take+'\n'
            await client.send_message(message.channel, ret)
    if message.channel == client.get_channel(channelNum):
        '''
        gives user a key
        '''
        global keyTakenToday
        if message.content.startswith('!take'):
            if not message.author in keyTakenToday:
                item = message.content[6:]
                keys = open(keysName, 'r+')
                keylist = keys.readlines()
                keys.close()
                temp = ''
                gib = ''
                gibPerm = ''
                for i in keylist:
                    if i.split(',')[0].upper() == item.upper():
                        if gib == '':
                            gibPerm = i
                            gib = 'Game: ' + i.split(',')[0]+ ' Key: ' + i.split(',')[1] + ' Given by: '+ i.split(',')[2]
                        else:
                            temp = temp+i
                    else:
                        temp = temp+i
                if gib == '':
                    publicMessage = "Item requested is not avalible"
                    gib = "Not avalible.  Please tell Draco if this is wrong"
                else:
                    publicMessage = message.author.name + " has claimed " + gibPerm.split(',')[0] + ' which was donated by ' + gibPerm.split(',')[2]
                await client.send_message(message.author,gib)
                await client.send_message(client.get_channel(channelNum), publicMessage)
                addToUsed = open(usedKeys, 'a')
                addToUsed.write(gibPerm)
                addToUsed.close()
                a = open(keysName, 'w')
                a.write(temp)
                a.close()
                keyTakenToday.append(message.author)
            else:
                await client.send_message(message.author,"Sorry, due to potential security issues, we're limiting the number of keys taken to 1 per day")

    if message.channel.is_private:
        '''
        takes a key from a user
        '''
        if message.content.startswith('!gib'):
            item = message.content[4:]
            temp = item.split(' ')
            name = ''
            comp = re.compile(r'(\w\w\w\w\w\-\w\w\w\w\w\-\w\w\w\w\w\-\w\w\w\w\w\-\w\w\w\w\w)|(\w\w\w\w\w\-\w\w\w\w\w\-\w\w\w\w\w)')#and third one?
            co = comp.match(temp[len(temp)-1])
            if len(temp) > 2: # and len(co)>0:
                for i in range(0, len(temp)-1):
                    name = name+temp[i]
                key = temp[len(temp)-1]
                await client.send_message(message.author, "Thank you!\n I recieved "+name+" with a key of "+ key)
                a = open(keysName, 'a')
                a.write(name + ',' + key + ',' + message.author.name + '\n')
                a.close()
            else:
                await client.send_message(message.author, "I think your game might be missing a key")
    '''
        {
    "id": "162701077035089920",
    "channel_id": "131391742183342080",
    "author": {},
    "content": "Hey guys!",
    "timestamp": "2016-03-24T23:15:59.605000+00:00",
    "edited_timestamp": null,
    "tts": false,
    "mention_everyone": false,
    "mentions": [],
    "mention_roles": [],
    "attachments": [],
    "embeds": [],
    "reactions": []
}
    '''

client.run(token)
