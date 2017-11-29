#keyBot
#By DracoRanger

import discord
from discord.ext import commands
import asyncio
import time
#import logging

client = discord.Client()
bot = commands.Bot(command_prefix="!",description="")

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
            keys = open(keysName,'r')
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
        if message.content.startswith('!take'):
            item = message.content[6:]
            keys = open(keysName,'r+')
            keylist = keys.readlines()
            keys.close()
            temp = ''
            gib = ''
            for i in keylist:
                if i.split(',')[0]==item:
                    if gib == '':
                        gib = i
                    else:
                        temp = temp+i
                else:
                    temp = temp+i
            if gib == '':
                publicMessage = "Item requested is not avalible"
                gib = "Not avalible.  Please tell Draco if this is wrong"
            else:
                publicMessage = "Someone has claimed " + gib.split(',')[0]
            await client.send_message(message.author,gib)
            await client.send_message(client.get_channel(channelNum), publicMessage)
            addToUsed = open(usedKeys, 'a')
            addToUsed.write(gib+'\n')
            addToUsed.close()
            a = open(keysName, 'w')
            a.write(temp)
            a.close()
    if message.channel.is_private:
        '''
        takes a key from a user
        '''
        if message.content.startswith('!gib'):
            item = message.content[4:]
            temp = item.split(' ')
            name = ''
            for i in range(0,len(temp)-1):
                name = name+temp[i]
            key = temp[len(temp)-1]
            await client.send_message(message.author,"Thank you!\n I recieved "+name+" with a key of "+ key)
            a = open(keysName, 'a')
            a.write(name+','+key+'\n')
            a.close()
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
