import discord
import os
import json
import requests
import locale
from keep_alive import keep_alive

client = discord.Client()

# ---

def showHelp():
    commands = '__The commands:__\n\n**$help** - Shows this message.\n**$stats <channel>** - Provides stats for the specified YouTube channel. Use the channel ID. The usage of channel names is still in developement.'
    return (commands)

# ---

def checkAccount(channel_id):
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + channel_id + "&key="
        + os.getenv('GOOGLEAPI'))
    data = json.loads(response.text)
    return (data['pageInfo']['totalResults'])

def getProfilePic(channel_id):
  response = requests.get(
    "https://www.googleapis.com/youtube/v3/channels?part=snippet&fields=items%2Fsnippet%2Fthumbnails%2Fdefault&id=" + channel_id + "&key="
    + os.getenv('GOOGLEAPI'))
  data = json.loads(response.text)
  return (data['items'][0]['snippet']['thumbnails']['default']['url'])

def formatNumber(number):
  parsedNr = int(number)
  locale.setlocale(locale.LC_ALL, '')
  formattedNumber = locale.format_string("%d", parsedNr, grouping=True)
  return (formattedNumber)

# Data for $stats
def stats_getSubs(channel_id):
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + channel_id + "&key="
        + os.getenv('GOOGLEAPI'))
    data = json.loads(response.text)
    return (data['items'][0]['statistics']['subscriberCount'])


def stats_getVideos(channel_id):
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + channel_id + "&key="
        + os.getenv('GOOGLEAPI'))
    data = json.loads(response.text)
    return (data['items'][0]['statistics']['videoCount'])


def stats_getViews(channel_id):
    response = requests.get(
        "https://www.googleapis.com/youtube/v3/channels?part=statistics&id=" + channel_id + "&key="
        + os.getenv('GOOGLEAPI'))
    data = json.loads(response.text)
    return (data['items'][0]['statistics']['viewCount'])

# ---

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

# ---------------------------------------------------------------
# $help - Shows the list of commands.
# ---------------------------------------------------------------

    if message.content.startswith('$help'):
        help = showHelp()
        await message.channel.send(help)
        print(message.guild.name + ' / ' + message.channel.name + ' - Help sent')
        return

# ---------------------------------------------------------------
# $stats - Provides the stats.
# ---------------------------------------------------------------

    if message.content.startswith('$stats'):

        unknown_channel = "`I don't know this channel. Please try another one.`"
        try:
          channel = message.content.split("$stats ", 1)[1]
        except:
          await message.channel.send(unknown_channel)
          print(message.guild.name + ' / ' + message.channel.name + ' - Empty channel')
          return
        yt_results = checkAccount(channel)

        # Response:
        if yt_results == 0:
          await message.channel.send(unknown_channel)
          print(message.guild.name + ' / ' + message.channel.name + ' - Unknown channel - Channel: ' + channel)
          return
        else:
          yt_subs = stats_getSubs(channel)
          yt_videos = stats_getVideos(channel)
          yt_views = stats_getViews(channel)
          # ---
          statsMessage = discord.Embed(title="YouTube Stats", description="**Channel: ** [Link](https://www.youtube.com/channel/" + channel + ")", color=0xf50000)
          statsMessage.set_thumbnail(url=getProfilePic(channel))
          statsMessage.add_field(name="Subscribers", value=formatNumber(yt_subs), inline=False)
          statsMessage.add_field(name="Total videos", value=formatNumber(yt_videos), inline=False)
          statsMessage.add_field(name="Total views", value=formatNumber(yt_views), inline=False)
          # ---
          await message.channel.send(embed=statsMessage)
          print(message.guild.name + ' / ' + message.channel.name + ' - Stats sent - Channel: ' + channel)
          return

# ---------------------------------------------------------------
# $ - Unknown commands
# ---------------------------------------------------------------

    if message.content.startswith('$'):
        await message.channel.send('```I dont know this command. Try $help```')
        print('Unknown Command - Answer sent')
        return


# ---------------------------------------------------------------
# Add reaction to messages that contain TubeStat
# ---------------------------------------------------------------

    if 'TubeStat' in message.content:
        reaction = '👀'
        await message.add_reaction(reaction)
        print(message.guild.name + ' / ' + message.channel.name + 'Added a reaction')
        return

keep_alive()
client.run(os.getenv('TOKEN'))
