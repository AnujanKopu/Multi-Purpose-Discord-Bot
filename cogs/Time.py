from datetime import datetime as dt
import pytz
from discord.ext import commands


class Time(commands.Cog):
  def __init__(self,bot):
    self.bot = bot

  @commands.command(pass_context = True)
  async def time(self,ctx,*,timez=None):
    today = None
    atzone =  pytz.all_timezones
    if timez:
      if timez.lower() == "list":
        await ctx.send('Please vist for all supported timezones: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568')
      elif timez.lower() == 'pst':
        today = Time.checkTime('US/Pacific')
      elif timez.lower() == 'gmt':
        today = Time.checkTime('Etc/Greenwich')
      elif timez.lower() == 'ct':
        today = Time.checkTime('US/Central')
      else:
        for zone in atzone:
          if zone == timez:
            today = Time.checkTime(timez)
            break
      if not today:
          await ctx.send('Please provide proper timezone. https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568')
          pass
      else:
        today1 = int(today[:2])
        if today1 > 12:
          today1 = today1 - 12
          await ctx.send('It is ' + str(today1)+today[-6:]+' PM currently in '+ timez +' time')
        else:
          await ctx.send('It is ' + today[-8:]+' AM currently in '+ timez +' time')  
    else:
      today = Time.checkTime('US/Eastern')
      today1 = int(today[:2])
      if today1 > 12:
        today1 = today1 - 12
        await ctx.send('It is ' + str(today1)+today[-6:]+' PM currently in US/Eastern time')
      else:
        await ctx.send('It is ' + today[-8:]+' AM currently in US/Eastern time')

  @staticmethod
  def checkTime(tzone):
    tzinfo=pytz.timezone(tzone)
    now = dt.now(tzinfo).time()
    current_time = now.strftime("%H:%M:%S")
    return current_time


def setup(bot):
  bot.add_cog(Time(bot))

#being worked on currently
class Reminder(commands.Cog):
  def __init__(self,bot):
    self.bot = bot
    

def setup(bot):
  bot.add_cog(Reminder(bot))

    