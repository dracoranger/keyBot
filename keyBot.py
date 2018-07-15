#keyBot
#By DracoRanger
import asyncio
import re
import time
from datetime import datetime
from datetime import timedelta
from threading import Timer,Thread,Event
import discord
from discord.ext import commands
#import logging

client = discord.Client()
bot = commands.Bot(command_prefix="!", description="")

BOT_FOLDER = ""

config = open('botData.txt', 'r')
conf = config.readlines() #push to array or do directly
token = conf[0][:-1]
keysNameHigher = conf[1][:-1]
keysNameLower = conf[2][:-1]
usedKeys = conf[3][:-1]
channelNumHigher = conf[4][:-1]
channelNumLower = conf[5][:-1]
timeToDecrease = float(conf[6][:-1])
userComp = conf[7][:-1]
secs = 86400 #seconds in a day
keyTakenToday = []
keyTakenThisWeek = []
weeklyCount = 0

#https://stackoverflow.com/questions/12435211/python-threading-timer-repeat-function-every-n-seconds
class perpetualTimer():

    def __init__(self, t, hFunction):
        self.t=t
        self.hFunction = hFunction
        self.thread = Timer(self.t, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()

def day_tick():
    global keyTakenThisWeek
    global keyTakenToday
    global weeklyCount
    message = ''
    weeklyCount = weeklyCount + 1
    if weeklyCount > 6:
        weeklyCount = 0
        keyTakenThisWeek = []
        message = "Weekly and daily reset"
    else:
        message = "Daily reset"
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
    keep.sort()
    remove.sort()
    k = ''
    r = ''
    for ke in keep:
        k = k + ke
    for rem in remove:
        r = r + rem
    with open(keysNameHigher, 'w') as keys:
        keys.write(k)
    with open(keysNameLower,'a') as keys:
        keys.write(r)
    print(str(datetime.now())+message)

tim = perpetualTimer(secs,day_tick)
tim.start()


def takeKeys(message, keysList, usersTakenList):
    item = message.content[message.content.find(' ')+1:]
    #print(item)
    keys = open(keysList, 'r+')
    keylist = keys.readlines()
    keys.close()
    temp = ''
    gib = ''
    gibPerm = ''
    for key in keylist:
        check = key.split(',')[0]
        if check.upper() == item.upper():
            if gib == '':
                gibPerm = key
                gib = 'Game: ' + key.split(',')[0]+ ' Key: ' + key.split(',')[-3] + ' Given by: '+ key.split(',')[-2]
            else:
                temp = temp+key
        else:
            temp = temp+key
    if gib == '':
        publicMessage = "Item requested is not avalible"
        gib = "Not avalible.  Please tell Draco if this is wrong"
    else:
        publicMessage = message.author.name + " has claimed " + gibPerm.split(',')[0] + ' which was donated by ' + gibPerm.split(',')[-2]
        usersTakenList.append(message.author)
    with open(usedKeys, 'a') as addToUsed:
        addToUsed.write(gibPerm)
    with open(keysList, 'w') as remaining:
        remaining.write(temp)
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
    print(str(datetime.now()))
    print('------')
    message = client.user.name + " is up and running!"
    await client.send_message(client.get_channel(channelNumHigher), message)
    #await client.send_message(client.get_channel(channelNumLower), message)

@client.event
@asyncio.coroutine
async def on_message(message):
    channelNum = 0
    keyList = ''
    if message.author == client.user:
        return
    #if message.channel == client.get_channel(channelNumHigher):
    channelNum = channelNumHigher
    keyList = keysNameHigher
    #elif message.channel == client.get_channel(channelNumLower):
    #    channelNum = channelNumLower
    #    keyList = keysNameLower
    if message.channel == client.get_channel(channelNum) or message.channel.is_private:
    #if message.channel == client.get_channel(channelNum):

        '''
        prints all commands
        '''
        if message.content.startswith('!help'):
            keylistDaily = "**!keysDaily** = prints a list of the daily games, works in pms" #in either server or
            keylistWeekly = "**!keysWeekly** = prints a list of the weekly games, works in pms" #in either server or
            gib = "**!gib [gameName] [key]**= gives a key to the bot, only works in pms"
            takeDaily = "**!takeDaily [gameName]** = messages you with the game's key, works only in server, recieve key in pm, message posted to server"
            takeWeekly = "**!takeWeekly [gameName]** = messages you with the game's key, works only in server, recieve key in pm, message posted to server"

            ret = keylistDaily+'\n'+takeDaily+'\n\n'+keylistWeekly+'\n'+takeWeekly+'\n\n'+gib+'\n'
            await client.send_message(message.channel, ret)
    if message.channel == client.get_channel(channelNum):
        '''
        gives user a key
        '''
        global keyTakenToday
        global keyTakenThisWeek
        if message.content.startswith('!takeDaily') or message.content.startswith('!takedaily'):
            #if not message.author in keyTakenToday or channelNum == channelNumLower:
            if not message.author in keyTakenToday:
                temp = takeKeys(message, keysNameLower, keyTakenToday)
                await client.send_message(message.author, temp[0])
                await client.send_message(client.get_channel(channelNumHigher), temp[1])

            else:
                await client.send_message(message.author,"Sorry, due to potential security issues, we're limiting the number of keys taken to 1 per day")
        elif message.content.startswith('!takeWeekly') or message.content.startswith('!takeweekly'):
            #if not message.author in keyTakenToday or channelNum == channelNumLower:
            if not message.author in keyTakenThisWeek:
                temp = takeKeys(message, keysNameHigher, keyTakenThisWeek)
                await client.send_message(message.author, temp[0])
                await client.send_message(client.get_channel(channelNumHigher), temp[1])
                #.append(message.author)
            else:
                await client.send_message(message.author,"Sorry, due to potential security issues, we're limiting the number of keys taken to 1 per week")
    if message.channel.is_private:
        '''
        prints the list of keys
        '''
        if message.content.startswith('!keysDaily') or message.content.startswith('!keysdaily'):
            temp = printKeys(keysNameLower)
            if len(temp[0]) > 1999:
                keys = []
                curr = ''
                num = 0
                for i in temp:
                    curr = curr + i
                    num = num + 1
                    if num > 1500:
                        if i == '\n':
                            keys.append(curr)
                            curr = ''
                            num = 0
                for i in keys:
                    await client.send_message(message.channel, i)
            else:
                await client.send_message(message.channel, temp)
        elif message.content.startswith('!keysWeekly') or message.content.startswith('!keysweekly'):
            temp = printKeys(keysNameHigher)
            if len(temp[0]) > 1999:
                keys = []
                curr = ''
                num = 0
                for i in temp:
                    curr = curr + i
                    num = num + 1
                    if num > 1500:
                        if i == '\n':
                            keys.append(curr)
                            curr = ''
                            num = 0
                for i in keys:
                    await client.send_message(message.channel, i)
            else:
                await client.send_message(message.channel, temp)
        '''
        takes a key from a user
        '''
        if message.content.startswith('!gib'):
            item = message.content[4:]
            temp = item.split(' ')
            name = ''
            comp = re.compile(r'((\w\w\w\w\w\-\w\w\w\w\w\-\w\w\w\w\w\-\w\w\w\w\w\-\w\w\w\w\w\b)|(\w\w\w\w\w\-\w\w\w\w\w\-\w\w\w\w\w\b))')#and third one?
            co = comp.match(temp[-1])
            if len(temp) > 2 and co:
                for i in range(1, len(temp)-1):
                    if temp[i] != '':
                        name = name+temp[i] + ' '
                name = name[0:-1]
                if len(name) > 75:
                    name = name[0:75]
                key = temp[-1]
                await client.send_message(message.author, "Thank you!\n I recieved "+name+" with a key of "+ key)
                with open(keysNameHigher, 'a') as keys:
                    keys.write(name + ',' + key + ',' + message.author.name + ',' + str(time.time()) +'\n')
            else:
                await client.send_message(message.author, "I think your game might be missing a key")

client.run(token)
