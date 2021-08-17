# This file is an accumulation of the rest of the programs. This file utilizes the old discord client compared to the new command subclass used in the new files. You may use this if you'd like. This file lacks a few qualities of the new programs and isn't well written. Make sure to turn on intents in the discord developer interface

#Note this bot is not multi-server servicable.It uses the same key for all servers compared to the new edition. 


import discord 
import os
import requests
from Running import running
from replit import db
from datetime import datetime as dt
import pytz
import asyncio
import re

intents = discord.Intents().all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  while(True):
    await checkTime(1,'US/Eastern')


    
    
Letter1 = '\N{Regional Indicator Symbol Letter A}'
Letter2 = '\N{Regional Indicator Symbol Letter N}'
Letter3 = '\N{Regional Indicator Symbol Letter I}'
Letter4 = '\N{Regional Indicator Symbol Letter M}'
Letter5 = '\N{Regional Indicator Symbol Letter E}'
Letter6 = '\N{Regional Indicator Symbol Letter G}'
Letter7 = '\N{Regional Indicator Symbol Letter O}'
Letter8 = '\N{Regional Indicator Symbol Letter D}'
Letter8 = '\N{Regional Indicator Symbol Letter D}'
Letter9 = '\N{Regional Indicator Symbol Letter X}'
Letter10 = '\N{Regional Indicator Symbol Letter T}'
Letter11 = '\N{Regional Indicator Symbol Letter Y}'


@client.event
async def on_message(message):
  length = 0
  length1 = 0
  length2 = 0
  if "captured" in db.keys():
    capture = []
    capture = list(reversed(db["captured"]))
    length2 = len(capture)
  if "names" in db.keys(): 
    names = []
    names = db["names"]
    length = len(names)
  if "filters" in db.keys():
    filters = []
    filters = db["filters"]
    length1 = len(filters)
  if message.author != client.user:
    if message.author != discord.Member.bot:
      if message.content.lower().startswith('kquote'):
        msg = message.content.split(" ",2)
        if len(str(msg)) > 250:
          await message.channel.send("Please send messages with less than 250 characters")
          return 
        msg.pop(0)
        if len(msg) != 2:
          await message.channel.send("no noob kquote <name> <quote>")
          return 
        else: 
          for i in range(length):
            if names[i][0] == msg[0]:
              await message.channel.send('replaced '+ names[i][0]+ ': "'+ names[i][1] + '"')
              delete_database("names",i)
              continue
          update_database("names",msg) 
          await message.channel.send("New quote message added")

      elif message.content.lower().startswith('kshow'):
          if length1 ==1:
            status = '(**unmuted)**'
          else:
            status = '(**muted**)'
          embed = discord.Embed(title='List '+status,colour= discord.Colour.gold())
          j = 1 
          templength = 0
          for i in range(length):
            templength += len(str(names[i]))
            if templength >= 1024:
              await message.channel.send(embed=embed)
              templength = 0
              J = str(j)
              embed = discord.Embed(title='List '+J+status,colour= discord.Colour.gold())
              j += 1
            embed.add_field(name=names[i][0],value=names[i][1],inline=False)
          await message.channel.send(embed=embed)
          
      elif message.content.lower().startswith('ktime'):
        tzone = message.content.upper().split(" ", 2)
        atzone =  pytz.all_timezones
        latzone = len(atzone)
        i=0
        if len(tzone) == 2:
          if tzone[1] == "list":
            await message.channel.send('Please vist for all supported timezones: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568')
          elif tzone[1] == 'PST':
            today = await checkTime(2, 'US/Pacific')
          elif tzone[1] == 'GMT':
            today = await checkTime(2, 'Etc/Greenwich')
          elif tzone[1] == 'CT':
            today = await checkTime(2,'US/Central')
          else:
            for zone in atzone:
              if zone == tzone[1]:
                today = await checkTime(2,tzone[1])
              else:
                i = i+1
              if i == latzone:
                await message.channel.send('Please provide proper timezone. https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568')
                pass
          if i != latzone:
            today1 = int(today[:2])
            if today1 > 12:
              today1 = today1 - 12
              await message.channel.send('It is ' + str(today1)+today[-6:]+' PM currently in '+ tzone[1] +' time')
            else:
              await message.channel.send('It is ' + today[-8:]+' AM currently in '+ tzone[1] +' time')     
        elif len(tzone) == 1:
          today = await checkTime(2, 'US/Eastern')
          today1 = int(today[:2])
          if today1 > 12:
            today1 = today1 - 12
            await message.channel.send('It is ' + str(today1)+today[-6:]+' PM currently in US/Eastern time')
          else:
            await message.channel.send('It is ' + today[-8:]+' AM currently in US/Eastern time')
        else:
            await message.channel.send("Please give ktime <optional:Timezone> \nTimezones listed here: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568")

        """
        elif message.content.lower().startswith('kannoy'):
          if message.author.id == 304005557797257216 or message.author.id == 278646990777221120:
            n = 0
            msg = message.content.split(" ")
            print(len(msg))
            if len(msg) == 2 or len(msg) == 3:
              print("hi") 
              if len(msg) == 2:
                n = 5
              if len(msg) == 3:
                n = int(msg[2])
                if n < 20:
                  n = 20
              for i in range(n):
                await message.channel.send((n*msg[1]))"""

      elif message.content.lower().startswith('kdel'):
        if length == 1:
          await message.channel.send("Can't delete, please insert something else before deleting")
        else:
          msg = message.content.split(" ",1)
          for i in range(length):
            if names[i][0] == msg[1]:
              await message.channel.send('Successfuly deleted ' + names[i][0] + ': "'+ names[i][1] + '"')
              delete_database("names",i)
              continue
      elif message.content.lower().startswith('kmute'):
        if length1 == 2: 
          await message.channel.send('already muted')
        else:
          update_database("filters",1)
      elif message.content.lower().startswith('kunmute'):
        if length1 == 1:
          await message.channel.send('already unmuted')
        else:
          delete_database("filters",1)
      elif message.content.lower().startswith('khelp'):
        help = discord.Embed(title='Help',colour = discord.Colour.teal())
        help.add_field(name='kquote',value='Add a keyword and a quote to reference into database',inline=False)
        help.add_field(name='kdel',value='Delete keyword and the reference in database',inline=False)
        help.add_field(name='kshow',value='Display all keywords and quotes in kquote database',inline=False)
        help.add_field(name='ktime',value='Shows the current time in different timezones. Use ktime list for list of all timezones',inline=False)
        help.add_field(name='kmute',value='Mute kquote reference',inline=False)
        help.add_field(name='kunmute',value='Unmute kquote reference',inline=False)
        help.add_field(name='kpt',value='Use 1pt to shorten your link',inline=False)
        help.add_field(name='ksnipe',value='dankmemer x5',inline=False)
        await message.channel.send(embed=help)
      elif message.content.lower().startswith('kpt'):
        if message.author != client.user:
          channel = message.channel.id
          channel1 = client.get_channel(channel)
          user = message.author.id
          msg = message.content.split(" ", 3)
          pattern = r'[^\.a-z0-9]'
          if len(msg) == 3 or len(msg) ==2:
            if len(msg) == 3:
              if re.search(pattern, msg[2]):
                await message.channel.send("Give proper keyword no char other than a-z;0-9")
              link = await shorterner(msg[1],msg[2],channel,user)
            else:
              link = await shorterner(msg[1]," ",channel,user)
            if link == "no spam plox":
              pass
            elif link == "BAD LINK":
              await channel1.send(link)
              pass
            else:
              pt=discord.Embed(title=link,description='redirects to ' +msg[1],colour=discord.Colour.blurple())
              pt.set_image(url='https://1pt.co/resources/assets/og-image.png')
              await channel1.send(embed=pt)
          else:
            await message.channel.send('kpt <link> <optional:intended short_url>')
      elif message.content.lower().startswith('ksnipe'):
          if length2 == 0: 
            await message.channel.send("Nothing to snipe")
            return
          msg = message.content.lower().split(" ",2);
          current_time = await checkTime(2, 'US/Eastern')
          if len(msg) == 1:
              if capture[-1][4] == "message":
               embed = discord.Embed(title="0)"+capture[0][1],description=capture[0][3],colour=discord.Colour.magenta())
              else:
                embed = discord.Embed(title="0)"+capture[0][1]+"(Edit)",description=capture[0][3],colour=discord.Colour.green())
              embed.set_thumbnail(url=capture[0][0])
              embed.set_footer(text=(capture[0][2])[:10]+ " " +current_time)
              await message.channel.send(embed=embed)
          elif len(msg) > 1:
            if msg[1] == 'all':
              embeds = []
              b = 1
              embed = discord.Embed(title="Sniped Messages(1) - ksnipe <index> for more specfic details",colour=discord.Colour.blue())
              for i in range(length2):
                if i % 10 == 0 and i != 0:
                  embeds.append(embed)
                  #await message.channel.send(embed=embed)  
                  b += 1
                  embed = discord.Embed(title="Sniped Messages("+str(b)+")",colour=discord.Colour.blue())
                if len(capture[i][3]) > 100:
                  description = ((capture[i][3])[:100])
                else:
                  description = capture[i][3]
                if capture[i][4] == "message":
                  if not description:
                    description = "Nothing Found"
                  embed.add_field(name=str(i)+")"+capture[i][1] ,value=description, inline = False)
                else:
                    if not description:
                      description = "Nothing Found"
                    embed.add_field(name=str(i)+")"+capture[i][1]+"(Edit)",value=description, inline = False)
              embeds.append(embed)
              #await message.channel.send(embed=embed)   
              await pages(message,embeds)
            else:
              if msg[1].isdigit():
                length = int(msg[1])
                if length > length2:
                  length = length2
                for i in range(5):
                  await asyncio.sleep(1)
                  if (length+i) > len(capture)-1:
                    break
                  if capture[length+i][4] == "message":
                    embed = discord.Embed(title= str(length+i)+")"+capture[length+i][1],description=capture[length+i][3],colour=discord.Colour.magenta())
                  else:
                    print("hi")
                    embed = discord.Embed(title= str(length+i)+")"+capture[length+i][1]+"(Edit)",description=capture[length+i][3],colour=discord.Colour.green())
                  embed.set_thumbnail(url=capture[length+i][0])
                  embed.set_footer(text=capture[length+i][2][:10]+ " " +current_time)
                  await message.channel.send(embed=embed)
              else:  
                  await message.channel.send('ksnipe <optional:index/all> Index will be incremented 5 if possible')
 
  


@client.event
async def on_message_delete(message):
  msg = message.content
  if not msg or len(msg) > 1048:
    return
  if not message.author.bot:
    if message.author != client.user and message.author.id !=278646990777221120:
      if isinstance(msg, str):
        tstamp = str(message.created_at)
        author = message.author
        pfp = author.avatar_url
        #data1 = "{} {} {} {}".format(pfp,author,tstamp,msg)
        data = [str(pfp),str(author),tstamp,msg,"message"]
        update_database("captured",data)
      
@client.event
async def on_message_edit(before, after):
  msg = before.content
  if not msg or len(msg) > 1048:
    return
  if not before.author.bot:
    if before.author != client.user and before.author.id !=278646990777221120:
      if isinstance(msg, str):
        tstamp = str(before.created_at)
        author = before.author
        pfp = author.avatar_url
        #data1 = "{} {} {} {}".format(pfp,author,tstamp,msg)
        data = [str(pfp),str(author),tstamp,msg,"edit"]
        update_database("captured",data)

  

"""
elif message.content.startswith('ksnipe'):
    embed = discord.Embed(title='Past 5 Snipes',colour= discord.Colour.magenta())
    for i in range(length2):
      embed.set_image(url=capture[i][0])
      embed.add_field(name=capture[i][1],value= capture[i][2],inline=False)
      embed.add_field(value='time: '+capture[i][3])
await message.channel.send(embed=embed)
"""




async def checkTime(number,tzone):
    tzinfo=pytz.timezone(tzone)
    now = dt.now(tzinfo).time()
    current_time = now.strftime("%H:%M:%S")
    current_date=dt.today().strftime("%A")
    if number == 2:
      return(current_time)
       
       
async def call(num,num2):
  embed = discord.Embed(
    title="Please fetch google classroom link",
    description="https://mail.google.com/mail/u/0/",colour = discord.Colour.lighter_grey()
  )
  channel = client.get_channel(num)
  await channel.send(embed = embed)
  channel = client.get_channel(num2)
  await channel.send(embed = embed)
  while(True):
    try:
      msg = await client.wait_for('message', timeout=660)
      if msg.content.startswith('https://meet.google.com/'):
        if msg.channel.id == num or msg.channel.id == num2:
          return("**GMEET**" + msg.content,msg.channel.id)
    except asyncio.TimeoutError:
      return('**GMAIL:**https://mail.google.com/mail/u/0/ (60 seconds had passed')

async def shorterner(url,keyword,num,num1):
  pattern = r'[^\.a-z0-9]'
  while(True): 
    channel = client.get_channel(num)
    r = requests.get('https://api.1pt.co/addURL?long=' + url + '&short='+ keyword)
    info = r.json()
    try:
      if info['status'] == 201:
        if info['short'] == keyword or keyword == " ":
          return('https://1pt.co/' + info['short'])
        else:
          ask = discord.Embed(description='sorry, keyword already taken. Give new keyword or press n to exit(60 seconds til timeout)',colour = discord.Colour.lighter_grey())
          await channel.send(embed=ask)
          msg = await client.wait_for('message',timeout=60)
          if re.search(pattern,msg.content):
            await channel.send("Give proper keyword no char other than a-z;0-9")
            pass
          if msg.content.startswith('kpt'):
            return("1pt thinks you're trolling")
          if len(msg.content) == 1:
            if msg.author.id == num1:
              if msg.content == "n":
                return('https://1pt.co/'+info['short'])
          elif msg.author == client.user: 
            return("no spam plox")
          else:
              keyword = msg.content 
      else:
        return("BAD LINK")
                
    except asyncio.TimeoutError:
      await client.delete_message()
      return('Timeout 60 seconds has passed https://1pt.co/'+info['short'])


async def pages(msg,contents):
    pages = len(contents)
    print(pages)
    cur_page = 1
    message = await msg.channel.send(embed=contents[cur_page-1])
    # getting the message object for editing and reacting

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")
    buttons =  ["◀️", "▶️"]
    
    while True:
        try:
            reaction, user = await client.wait_for("reaction_add", check=lambda reaction,user: user == msg.author and reaction.emoji in buttons, timeout=60)
            # waiting for a reaction to be added - times out after x seconds, 60 in this
            # example

            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                await message.edit(embed=contents[cur_page-1])
                await message.remove_reaction(reaction, user)

            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                await message.edit(embed=contents[cur_page-1])
                await message.remove_reaction(reaction, user)

            else:
                await message.remove_reaction(reaction, user)
                # removes reactions if the user tries to go forward on the last page or
                # backwards on the first page
        except asyncio.TimeoutError:
            await message.delete()
            break
            # ending the loop if user doesn't react after x seconds

      
def update_database(name,data):
  if name in db.keys():
    temp = db[name]
    temp.append(data)
    if name == "captured":
      if len(temp) == 50:
        del temp[0]
    db[name] = temp
  else:
    db[name] = [data]

def delete_database(name,index):
  if name in db.keys():
    temp = db[name]
    del temp[index]
    db[name] = temp



  

running()
client.run(os.getenv('TOKEN'))





















 