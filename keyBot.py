#keyBot
#By DracoRanger

import discord
from discord.ext import commands
import asyncio
import time
#import logging

client=discord.Client()
bot=commands.Bot(command_prefix="!",description="")

BOT_FOLDER=""

config=open('botData.txt','r')
temp=config.readlines() #push to array or do directly
token=temp[0][:-1]
print(token)
keysName=temp[1][:-1]
print(keysName)
usedKeys=temp[2][:-1]
print(usedKeys)
temp=open(keysName,'w+')
temp.close
temp=open(usedKeys,'w+')
temp.close

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!keylist'):
        keys = open(keysName,'r+')
        keylist=keys.readlines()
        keys.close
        temp=''
        for i in keylist:
            temp=temp+i.split(',')[0]#should only show name
        await client.send_message(message.channel, temp)
    if message.content.startswith('!take'):
        item = message.content[5:]
        keys = open(keysName,'r+')
        keylist=keys.readlines()
        keys.close
        temp=''
        gib=''
        newKeys=''
        for i in keylist:
            if i.split(',')[0]==item:
                if gib == '':
                    gib=i
                else:
                    temp=temp+i
        await client.send_message(message.author,gib)
        addToUsed= open(usedKeys,'a')
        write(gib)
        addToUsed.close
        a=open(keysName,'w')
        write(temp)
        a.close
    if message.content.startswith('!gib'):
        item = message.content[4:]
        temp=item.split(' ')
        name=''
        for i in range(0,len(temp)-1):
            name=name+temp[i]
        key = temp[len(temp)-1]
        await client.send_message(message.author,"Thank you!\n I recieved "+name+" with a key of "+ key)
    if message.content.startswith('!help'):
        keylist="!keylist = prints a list of games that have keys"
        gib="!gib [gameName] [key]= gives a key to the bot"
        take="!take [gameName] = messages you with the game's key"
        ret=keylist+'\n'+gib+'\n'+take+'\n'
        await client.send_message(message.channel, ret)

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
