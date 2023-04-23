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
    if message.content.startswith('!summarize_from'):
        # Parse the message link from the command
        link = message.content.split(' ')[1]
        message_id = int(link.split('/')[-1])
        
        # Retrieve the specified message
        channel = message.channel
        msg = await channel.fetch_message(message_id)
        
        # Retrieve the most recent message in the channel
        async for recent_msg in channel.history(limit=1):
            pass
        
        # Count the number of messages between the two messages
        distance = 0
        async for past_msg in channel.history(after=msg.created_at, before=recent_msg.created_at):
            distance += 1
        
        conversation = ''
        async for msg in message.channel.history(limit=distance):
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
    elif message.content.startswith('!status'):
        await message.channel.send("Online!")
    elif message.content.startswith('!distance'):
        # Parse the message link from the command
        link = message.content.split(' ')[1]
        message_id = int(link.split('/')[-1])
        
        # Retrieve the specified message
        channel = message.channel
        msg = await channel.fetch_message(message_id)
        
        # Retrieve the most recent message in the channel
        async for recent_msg in channel.history(limit=1):
            pass
        
        # Count the number of messages between the two messages
        distance = 0
        async for past_msg in channel.history(after=msg.created_at, before=recent_msg.created_at):
            distance += 1
        
        # Send the distance as a reply
        await message.reply(f'The distance between {link} and the most recent message is {distance}')

client.run(os.getenv('BOTTOKEN'))