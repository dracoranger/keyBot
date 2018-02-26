#keyBot
#By DracoRanger
import asyncio
import re
import time
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
keysNameHigher = conf[1][:-1]
keysNameLower = conf[2][:-1]
usedKeys = conf[3][:-1]
channelNumHigher = conf[4][:-1]
channelNumLower = conf[5][:-1]
timeToDecrease = float(conf[6][:-1])
userComp = conf[7][:-1]
secs = 0
keyTakenToday=[]

def setDelta():
    global secs
    # from https://stackoverflow.com/questions/15088037/python-script-to-do-something-at-the-same-time-every-day
    #should clear the keyLimiter
    x = datetime.today()
    #y=x.replace(day=x.day+1, hour=1, minute=0, second=0, microsecond=0)
    y = x + timedelta(days=1)
    delta_t = y-x
    secs = delta_t.seconds+1

def day_tick():
    global keyTakenToday
    keyTakenToday = []
    keep = []
    remove = []
    with open(keysNameHigher, 'r') as keysList:
        keys = keysList.readlines()
        for key in keys:
            comp = key.split(',')
            if time.time()-float(comp[3]) > timeToDecrease:
                remove.append(key)
            else:
                keep.append(key)
    k = ''
    r = ''
    for ke in keep:
        k = k + ke
    for re in remove:
        r = r + re
    with open(keysNameHigher, 'w') as keys:
        keys.write(k)
    with open(keysNameLower,'a') as keys:
        keys.write(r)
    setDelta()

setDelta()
t = Timer(secs, day_tick)
t.start()

def takeKeys(message, keysList, channelNum):
    global keyTakenToday
    item = message.content[6:]
    keys = open(keysList, 'r+')
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
        if channelNum == channelNumHigher:
            keyTakenToday.append(message.author)
    with open(usedKeys, 'a') as addToUsed:
        addToUsed.write(gibPerm)
    with open(keysList, 'w') as a:
        a.write(temp)
    return (gib,publicMessage)


def printKeys(keysList):
    with open(keysList, 'r') as keys:
        keylist = keys.readlines()
    temp = ''
    for i in keylist:
        temp = temp+i.split(',')[0]+'\n'#should only show name
    if temp == '':
        temp = 'No keys in storage'
    return temp


@client.event
async def on_ready():
    print('Logged in as ' + client.user.name)
    #print(client.user.id)
    print('------')
    message = client.user.name + " is up and running!"
    await client.send_message(client.get_channel(channelNumHigher), message)
    await client.send_message(client.get_channel(channelNumLower), message)

@client.event
@asyncio.coroutine
async def on_message(message):
    channelNum = 0
    keyList = ''
    if message.author == client.user:
        return
    if message.channel == client.get_channel(channelNumHigher):
        channelNum = channelNumHigher
        keyList = keysNameHigher
    elif message.channel == client.get_channel(channelNumLower):
        channelNum = channelNumLower
        keyList = keysNameLower

    #if message.channel == client.get_channel(channelNum) or message.channel.is_private:
    if message.channel == client.get_channel(channelNum):
        '''
        prints the list of keys
        '''
        if message.content.startswith('!keylist'):
            temp = printKeys(keyList)
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
        '''
        gives user a key
        '''
        global keyTakenToday
        if message.content.startswith('!take'):
            if not message.author in keyTakenToday or channelNum == channelNumLower:
                temp = takeKeys(message, keyList, channelNum)
                await client.send_message(message.author, temp[0])
                await client.send_message(client.get_channel(channelNum), temp[1])
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
            co = comp.match(temp[-1])
            if len(temp) > 2 and co:
                for i in range(0, len(temp)-1):
                    name = name+temp[i]
                key = temp[len(temp)-1]
                await client.send_message(message.author, "Thank you!\n I recieved "+name+" with a key of "+ key)
                with open(keysNameHigher, 'a') as keys:
                    keys.write(name + ',' + key + ',' + message.author.name + ',' + str(time.time()) +'\n')
            else:
                await client.send_message(message.author, "I think your game might be missing a key")

client.run(token)
