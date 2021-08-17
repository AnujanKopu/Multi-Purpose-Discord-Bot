import asyncio
import re
import requests
from Database import Database
import discord
from discord.ext import commands



class Misc(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
  
  @commands.Cog.listener()
  async def on_guild_join(self,guild):
    Database.new_server(str(guild.id))
    print(guild.id)

  @commands.command(pass_context=True)
  async def help(self,ctx):
    help = discord.Embed(title='Help',colour = discord.Colour.teal())
    help.add_field(name='kquote',value='Add a keyword and a quote to reference into database',inline=False)
    help.add_field(name='kdel',value='Delete keyword and the reference in database',inline=False)
    help.add_field(name='kshow',value='Display all keywords and quotes in kquote database',inline=False)
    help.add_field(name='ktime',value='Shows the current time in different timezones. Use ktime list for list of all timezones',inline=False)
    help.add_field(name='kmute',value='Mute kquote reference',inline=False)
    help.add_field(name='kunmute',value='Unmute kquote reference',inline=False)
    help.add_field(name='kpt',value='Use 1pt to shorten your link',inline=False)
    help.add_field(name='ksnipe',value='dankmemer x5',inline=False)
    await ctx.send(embed=help)

  @commands.command(pass_context=True)
  async def pt(self,ctx,url:str,*,short=None):
    if ctx.message.author != self.bot.user:
      user = ctx.message.author.id
      if url:
        if short:
          short = short.replace(" ","")
          if re.search(r'[^\.a-z0-9]', short):
            await ctx.send("Give proper keyword no char other than a-z;0-9")
          link = await self.shorterner(url,short,ctx.channel,user)
        else:
          link = await self.shorterner(url," ",ctx.channel,user)
        if link == "no spam please":
          pass
        elif link == "BAD LINK":
          await ctx.send(link)
          pass
        else:
          pt=discord.Embed(title=link,description='redirects to ' +url,colour=discord.Colour.blurple())
          pt.set_image(url='https://1pt.co/resources/assets/og-image.png')
          await ctx.send(embed=pt)
      else:
        await ctx.send('kpt <link> <optional:intended short_url>')


  async def shorterner(self,url,keyword,channel,num1):
    while(True): 
      r = requests.get('https://api.1pt.co/addURL?long=' + url + '&short='+ keyword)
      info = r.json()
      try:
        if info['status'] == 201:
          if info['short'] == keyword or keyword == " ":
            return('https://1pt.co/' + info['short'])
          else:
            ask = discord.Embed(description='sorry, keyword already taken. Give new keyword or press n to exit(60 seconds til timeout)',colour = discord.Colour.lighter_grey())
            await channel.send(embed=ask)
            msg = await self.bot.wait_for('message',timeout=60)
            if re.search(r'[^\.a-z0-9]',msg.content):
              await channel.send("Give proper keyword no char other than a-z;0-9")
              pass
            if msg.content.startswith('kpt'):
              return("1pt thinks you're trolling")
            if len(msg.content) == 1:
              if msg.author.id == num1:
                if msg.content == "n":
                  return('https://1pt.co/'+info['short'])
            elif msg.author == self.bot.user: 
              return("no spam please")
            else:
                keyword = msg.content 
        else:
          return("BAD LINK")
                  
      except asyncio.TimeoutError:
        await self.bot.delete_message()
        return('Timeout 60 seconds has passed https://1pt.co/'+info['short'])

  @staticmethod
  async def pages(bot,msg,contents):
    pages = len(contents)
    cur_page = 1
    message = await msg.channel.send(embed=contents[cur_page-1])
    # getting the message object for editing and reacting

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")
    buttons =  ["◀️", "▶️"]
    
    while True:
      try:
          reaction, user = await bot.wait_for("reaction_add", check=lambda reaction,user: user == msg.author and reaction.emoji in buttons, timeout=60)

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
              
      except asyncio.TimeoutError:
          await message.delete()
          break



def setup(bot):
  bot.add_cog(Misc(bot))