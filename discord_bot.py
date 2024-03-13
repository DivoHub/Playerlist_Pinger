import discord
import re

client = discord.Client()


def simplify_string(part_name):
    part_name = str(part_name.upper())
    simple_name = re.sub("[ -().]", "", part_name)
    return simple_name


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print('Ready!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content.lower()
    if (msg.startswith('$hello')):
        await message.channel.send('Hello!')

    elif (msg.startswith('$superuser')):


    elif (msg.startswith('$myid')):
        await message.channel.send('your Id is ' + str(client.user.id))
        await message.channel.send('my mention is' + str(client.user.mention))
        await message.channel.send(message.author.avatar_url)
        await message.channel.send('your name is ' + str(message.author.mention))

    elif (msg.startswith('$idof')):
        userid = msg[msg.find('@'):]
        await message.channel.send(userid)


with open("token.txt", "r") as file:
    token = str(file)
    file.close()
client.run(token)