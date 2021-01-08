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
    "\"It is what it is.\" ~(Kartikeya 'Solaire' Mishra)",
    "\"Ass\" ~(Aaaaaaaaayush)",
    "\"Time to hit the strip club\" ~(Vidhu 'Kalki' Sharma)",
    "\"Bahot Badhiya.\" ~(Kartikeya 'Solaire' Mishra)",
    "\"Hmmmm.... I see\" ~(Nikhil Kumar)"
]

help_doc = {"command": "description", "$hello": "Hello, <user_name>", "$quote": "A motivational quote with author's name to keep you going.", "$help": "To display all commands with descriptions", "$respond true": "to allow the bot to respond to sad messages with inspiration", "$respond false": "to disallow the bot to respond to sad messages with inspiration", "$ajia": "to randomly quote an Ajia Bunker Club member", "$logo": "logo of the club will be shared on the channel", "$mascot": "photo of the club mascot shall be shared on the channel" , "...": "More features are coming soon -- ..."}

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

def dad_joke():
    response = requests.get('https://icanhazdadjoke.com/', headers={'method': 'GET', 'Accept': 'text/plain'}).text
    return response

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
    if msg.startswith('$hello'):
        await message.channel.send(f'Hello, {author}!')

    if msg.startswith('$quote'):
        await message.channel.send(get_quote())

    if msg.startswith('$ajia'):
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
        help_message = "Kon'nichiwa, I'm Ajia Bunker bot. Kore herupu risuto mite kudasai:\n" + formatter(help_doc)
        await message.channel.send(help_message)
    
    if msg.startswith('$logo'):
        await message.channel.send(file=discord.File('./resources/images/bot_avatar.png'))
    
    if msg.startswith('$mascot'):
        await message.channel.send(file=discord.File('./resources/images/mascot.jpg'))
    
    if msg.startswith('$paisado'):
        await message.channel.send(file=discord.File('./resources/images/bheek.jpg'))
    
    if msg.startswith('$badhiya'):
        await message.channel.send(file=discord.File('./resources/images/badhiya.png'))
    
    if msg.startswith('$isee'):
        await message.channel.send(file=discord.File('./resources/images/isee.jpg'))

    if msg.startswith('$dadjoke'):
        string_joke = ''
        number_of_jokes = int(re.search(r"([\d]{1,2})", msg).group(0))
        if number_of_jokes >=10 or number_of_jokes<=0:
            await message.channel.send('Specify the number of jokes to be less than 10 and greater than 0')
        else:
            for _ in range(number_of_jokes):
                string_joke += dad_joke() +'\n\n'
            await message.channel.send(string_joke)

keep_alive()
client.run(os.getenv('TOKEN'))
