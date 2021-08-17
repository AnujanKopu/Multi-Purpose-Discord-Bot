import asyncio
from Database import Database
from cogs.Time import Time as tme
from cogs.Misc import Misc
import discord
from discord.ext import commands


class Snipe(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
  
  @commands.Cog.listener()
  async def on_message_delete(self,message):
    if isinstance(message.channel, discord.DMChannel):
      return None
    arg = message.content
    if not arg:
      return
    if len(arg) > 100:
      arg = arg[:100]
    if not message.author.bot and message.author.id !=278646990777221120:
      if isinstance(arg, str):
        tstamp = str(message.created_at)
        author = message.author
        pfp = author.avatar_url
        data = [str(pfp),str(author),tstamp,arg,"message"]
        serverId = str(message.guild.id)
        Database.update(serverId,"captured",data)

  @commands.Cog.listener()
  async def on_message_edit(self,before, after):
    if isinstance(before.channel, discord.DMChannel):
      return None
    msg = before.content
    serverId = str(before.guild.id)
    if not msg:
      return
    if len(msg) > 100:
      msg = msg[:100]
    if not before.author.bot and before.author.id !=278646990777221120:
      if isinstance(msg, str):
        tstamp = str(before.created_at)
        author = before.author
        pfp = author.avatar_url
        #data1 = "{} {} {} {}".format(pfp,author,tstamp,msg)
        data = [str(pfp),str(author),tstamp,msg,"edit"]
        Database.update(serverId,"captured",data)

  @commands.command(pass_context = True)
  async def snipe(self,ctx,*,arg=None):
    if isinstance(ctx.channel, discord.DMChannel):
      if arg:
        serverId = arg.split(" ",1)[0]
        data = Database.get_data(serverId,'captured')
        if not data: 
          await ctx.send("Incorrect serverId")
          return None
        arg = arg.split(" ",1)[1] if len(arg.split(" ",1)) > 1 else None
      else:
        await ctx.send("Please use command in  a server or search by <serverId>(needs dev opts on) as second argument to use in dms")
        return None
    else:
      serverId = str(ctx.guild.id)
      data = Database.get_data(serverId,"captured")
      if not data: 
        await ctx.send("Nothing to snipe")
        return
    length = len(data)
    current_time = tme.checkTime('US/Eastern')
    if not arg:
        if data[-1][4] == "message":
          embed = discord.Embed(title="0)"+data[0][1],description=data[0][3],colour=discord.Colour.magenta())
        else:
          embed = discord.Embed(title="0)"+data[0][1]+"(Edit)",description=data[0][3],colour=discord.Colour.green())
        embed.set_thumbnail(url=data[0][0])
        embed.set_footer(text=(data[0][2])[:10]+ " " +current_time)
        await ctx.send(embed=embed)
    else:
      if arg == 'all':
        embeds = []
        b = 1
        embed = discord.Embed(title="Sniped Messages(1) - ksnipe <index> for more specfic details",colour=discord.Colour.blue())
        for i in range(length):
          if i % 10 == 0 and i != 0:
            embeds.append(embed)
            b += 1
            embed = discord.Embed(title="Sniped Messages("+str(b)+")",colour=discord.Colour.blue())
          description = data[i][3]
          if data[i][4] == "message":
            if not description:
              description = "Nothing Found"
            embed.add_field(name=str(i)+")"+data[i][1] ,value=description, inline = False)
          else:
              if not description:
                description = "Nothing Found"
              embed.add_field(name=str(i)+")"+data[i][1]+"(Edit)",value=description, inline = False)
        if embeds:
          embeds.append(embed)
          await Misc.pages(self.bot,ctx.message,embeds)
        else:
          await ctx.send(embed=embed)
      else:
        if arg.isdigit():
          search = int(arg)
          if search > length:
            search = length
          for i in range(5):
            await asyncio.sleep(1)
            if (search+i) > len(data)-1:
              break
            if data[search+i][4] == "message":
              embed = discord.Embed(title= str(search+i)+")"+data[search+i][1],description=data[search+i][3],colour=discord.Colour.magenta())
            else:
              embed = discord.Embed(title= str(search+i)+")"+data[search+i][1]+"(Edit)",description=data[search+i][3],colour=discord.Colour.green())
            embed.set_thumbnail(url=data[search+i][0])
            embed.set_footer(text=data[search+i][2][:10]+ " " +current_time)
            await ctx.send(embed=embed)
        else:  
            await ctx.send('ksnipe <optional:index/all> Index will be incremented 5 if possible')



def setup(bot):
  bot.add_cog(Snipe(bot))