from Database import Database
from cogs.Misc import Misc
import discord
from discord.ext import commands


class Quote(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  @commands.command(pass_context = True)
  async def quote(self,ctx,name:str,*,quote=None):
    if isinstance(ctx.channel, discord.DMChannel):
      return None
    serverId = str(ctx.guild.id)
    data = Database.get_data(serverId,"names")
    length = len(data) if data else 0
    if not quote:
      await ctx.send("no noob kquote <name> <quote>")
      return 
    elif len(quote) > 250:
      await ctx.send("Please send a quote with less than 250 characters")
      return 
    else: 
      for i in range(length):
        if data[i][0] == name:
          await ctx.send('replaced '+ data[i][0]+ ': "'+ data[i][1] + '"')
          Database.delete(serverId,"names",i)
          continue
      Database.update(serverId,"names",quote) 
      await ctx.send("New quote message added")

  @commands.command(pass_context = True)
  async def delete(self,ctx,name:str):
    if isinstance(ctx.channel, discord.DMChannel):
      return None
    serverId = str(ctx.guild.id)
    data = Database.get_data(serverId,"names")
    if data:
      length = len(data)
    else:
      await ctx.send("nothing to delete")
      return 
    for i in range(length):
      if data[i][0] == name:
        await ctx.send('Successfuly deleted ' + data[i][0] + ': "'+ data[i][1] + '"')
        Database.delete(serverId,"names",i)
        continue

  @commands.command(pass_context=True)
  async def mute(self,ctx):
    if isinstance(ctx.channel, discord.DMChannel):
      return None
    serverId = str(ctx.guild.id)
    data = Database.get_data(serverId,'mute')
    if data:
      await ctx.send('already muted')
    else:
      Database.update(serverId,'mute',True,assign=True)

  @commands.command(pass_context=True)
  async def unmute(self,ctx):
    if isinstance(ctx.channel, discord.DMChannel):
      return None
    serverId = str(ctx.guild.id)
    data = Database.get_data(serverId,'mute')
    if not data:
      await ctx.send('already unmuted')
    else:
      Database.update(serverId,'mute',False,assign=True)


  @commands.command(pass_context=True)
  async def show(self,ctx,sarg=None):
    if isinstance(ctx.channel, discord.DMChannel):
      if sarg:
        serverId = sarg
        data = Database.get_data(sarg,'names')
        if not data: 
          await ctx.send("Incorrect serverId")
          return None
        mute = Database.get_data(sarg,'mute')
      else:
        await ctx.send("Please use command in a server or search by <serverId> (needs dev opts on) as second argument to use in dms")
        return None
    else:
      serverId = str(ctx.guild.id)
      mute = Database.get_data(serverId,'mute')
      data = Database.get_data(serverId,"names")
    if data:
      length = len(data)
    else:
      await ctx.send("nothing to send")
      return
    if mute:
      status = '(**muted**)'
    else:
       status = '(**unmuted)**'
    embeds = []
    embed = discord.Embed(title='List '+status,colour= discord.Colour.gold())
    j = 1 
    templength = 0
    for i in range(length):
      templength += len(str(data[i]))
      if templength >= 1024:
        embeds.append(embed)
        templength = 0
        J = str(j)
        embed = discord.Embed(title='List '+J+status,colour= discord.Colour.gold())
        j += 1
      embed.add_field(name=data[i][0],value=data[i][1],inline=False)
    embeds.append(embed)
    await Misc.pages(self.bot,ctx.message,embeds)


  @commands.Cog.listener()
  async def on_message(self,message):
    if isinstance(message.channel, discord.DMChannel):
      return None
    if message.author.bot:
      return None
    serverId = message.guild.id
    mute = Database.get_data(serverId,'mute')
    if mute:
      return None
    data = Database.get_data(serverId,"names")
    if data:
      length = len(data)
    else:
      return None 
    for i in range(length):
      if data[i][0] in message.content:
        await message.channel.send(data[i][1])



def setup(bot):
  bot.add_cog(Quote(bot))