import discord
import openai
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
openai.api_key = os.getenv('OPENAIKEY')
intents = discord.Intents(emojis = True, emojis_and_stickers = True, integrations = True, 
    message_content = True, messages = True, reactions = True, typing = True) #discord, why do I have to do this
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('!get_messages'):
        channel = message.channel
        conversation = ''
        async for msg in message.channel.history(limit=25):
            if msg.author != client.user:
                conversation += f"{msg.author.name}: {msg.content}\n"
        
        #await message.channel.send(conversation)
        response = openai.Completion.create(
            engine = "text-davinci-003",
            prompt = f"{conversation}\n\nTl;dr",
            max_tokens=60,
            temperature=0.7
        )
        summary = response.choices[0].text.strip()
        print(response)
        print(summary)
        await message.channel.send("Summarized conversation:\n" + summary)

client.run(os.getenv('BOTTOKEN'))