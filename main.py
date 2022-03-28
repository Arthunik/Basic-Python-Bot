import os
import discord
from discord.ext import commands, tasks
import requests
import json
import random
from replit import db
from keep_alive import keep_alive


#simple bot reply to specific msg
bot = commands.Bot(command_prefix='$')
channel = int(os.environ['CHANNEL'])

sad_words = ["sad", "depressed", "unhappy", "angry", "bad", "miserable", "depressing"]

starter_encouragements = [
  "Cheer up!",
  "Hang in there.",
  "You are a great person :smiling_face_with_3_hearts: / bot! ",
  "Fighting!! you can do it!",
  "Positive things will come to you soon :grin: !"
]
 
def handle_socket_message(msg):
  print(f"message type: {msg['e']}")
  print(msg)

def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragment(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements
  
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@bot.command(name="quote")
async def send_quote(ctx):
  await ctx.send(get_quote())
  
@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))
  send_channel = bot.get_channel(channel)
  await send_channel.send("Bot is now OPEN")
    
@bot.command(name='hello')
async def send_hello(ctx):
  await ctx.send('Hello {0.author.display_name} :smiling_face_with_3_hearts: '.format(ctx))

@bot.command(name='help_command')
async def send_help(ctx):
  await ctx.send("GET INSPIRATION QUOTE BY USING '$quote' !")

@bot.command(name='copy')
async def send_reply(ctx, arg):
  await ctx.send('{}'.format(arg))

@bot.command(name='new')
async def add_encourage(ctx, arg):
  update_encouragements(arg)
  await ctx.send("New encouraging message added.")

@bot.command(name='del')
async def del_encourage(ctx, arg):
  encouragements = []
  if "encouragements" in db.keys():
    delete_encouragment(int(arg))
    encouragements = db["encouragements"]
    await ctx.send(encouragements)

@bot.command(name='list')
async def list_encourage(ctx, arg):
  encouragements = []
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
  await ctx.send(encouragements)
  
@bot.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(
    f'Hi {member.name}, welcome to Artscape Discord server :smiling_face_with_3_hearts: !'
  )
  await channel.send('Välkommen :smiling_face_with_3_hearts: !! {0.name}'.format(member))
  

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  msg = message.content
  options = starter_encouragements
  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(options))
  if msg.startswith('hello'):
    await message.channel.send('Hello {0.author.display_name}'.format(message))
  await bot.process_commands(message)
  
    

    
#run the bot
keep_alive()
bot.run(os.environ['TOKEN'])