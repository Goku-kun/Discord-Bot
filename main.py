import discord
import os
import re
import requests
import json
import random
from replit import db
from keep_alive import keep_alive



client = discord.Client()

sad_words = ["sad", "depressed", "worried",
             "unhappy", "angry", "depressing", "miserable"]

encouragements_start = [
    "You got this!",
    "Mou Daijobu!",
    "Hang on. You can do it!"
]

ajia_quotes = [
    "\"Tu pani pi.\" ~(Jay 'Sasuke' Hirpara)",
    "\"It is what it is.\" ~(Kartikeya  Mishra)",
    "\"Ass\" ~(Aaaaaaaaayush)",
    "\"Time to hit the strip club\" ~(Vidhu 'Kalki' Sharma)"
]

help_doc = {"command": "description", "$hello": "Hello, <user_name>", "$quote": "A motivational quote with author's name to keep you going.", "$help": "To display all commands with descriptions", "$respond true": "to allow the bot to respond to sad messages with inspiration", "$respond false": "to disallow the bot to respond to sad messages with inspiration", "$ajia": "to randomly quote an Ajia Bunker Club member", "...": "More features are coming soon -- ..."}

if "responding" not in db.keys():
    db['responding'] = True

def formatter(dictionary):
  string = ""
  for key, value in dictionary.items():
    string += key  + " -- " +value +"\n"
  return string

def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    response_dictionary = json.loads(response.text)
    quote = response_dictionary[0]['q']
    author = response_dictionary[0]['a']
    return "\"" + quote + "\"" + " ~(" + author+")"

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='to Your Commands!'))


@client.event
async def on_message(message):
    msg = message.content
    author = re.search(r'(.*)(#\d{4})', str(message.author)).group(1)
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send(f'Hello, {author}!')

    if message.content.startswith('$quote'):
        await message.channel.send(get_quote())

    if message.content.startswith('$ajia'):
        await message.channel.send(random.choice(ajia_quotes))
    
    if db["responding"]:
        if (any(word in msg for word in sad_words)):
            await message.channel.send(random.choice(encouragements_start))
        
    if msg.startswith('$respond'):
        value = msg.split("$respond ", 1)[1]

        if value.lower() == 'true':
            db['responding'] = True
            await message.channel.send('Bot shall respond')
        else:
            db['responding'] = False
            await message.channel.send("Bot shalln't respond")
    
    if msg.startswith('$help'):
        help_message = "Goku's Encouraging bot is now live with Open Beta 1.0\n" + formatter(help_doc)
        await message.channel.send(help_message)

keep_alive()
client.run(os.getenv('TOKEN'))
