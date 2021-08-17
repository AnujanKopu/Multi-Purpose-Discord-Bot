#Make sure to turn on intents in your discord developer interface. 
import os
from replit import db
import discord
from discord.ext import commands
intents = discord.Intents().all()
bot = commands.Bot(command_prefix = 'k',case_insensitive =True,intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
  print(f'{bot.user} is online')

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
      pass
  else:
      raise error

@bot.command()
async def load(ctx,extension):
  if ctx.author.id == 278646990777221120:
    bot.load_extension(f'cogs.{extension}')
    await ctx.send("{} loaded".format(extension))
  
@bot.command()
async def unload(ctx,extension):
  if ctx.author.id == 278646990777221120:
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send("{} unloaded".format(extension))
  
@bot.command()
async def reload(ctx,extension):
  if ctx.author.id == 278646990777221120:
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send("{} reloaded".format(extension))


@bot.command()
async def act(ctx, member: commands.MemberConverter,*, message=None):
  if message == None:
    await ctx.send(f'Please provide a message with that!')
    return
  await ctx.message.delete()
  webhook = await ctx.channel.create_webhook(name=member.name)
  await webhook.send(
      str(message), username=member.name, avatar_url=member.avatar_url)
  await webhook.delete()


for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')



bot.run(os.environ['TOKEN'])