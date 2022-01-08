import os
import discord
import praw
from tabulate import tabulate

# If running locally, support .env file for setting the environment variables
from dotenv import load_dotenv
load_dotenv()

class DeepDive:
    def __init__(self, type, name, biome):
        self.type = type
        self.name = name
        self.biome = biome
        self.stages = []
    
    def add_stage(self, stage, primary, secondary, anomaly, warning):
        self.stages.append([stage, primary, secondary, anomaly, warning])
    
    def to_beautiful_string(self):
        out = f'**{self.type}**\n```\n'
        out += tabulate(self.stages, headers=["Stage", "Primary", "Secondary", "Anomaly", "Warning"], tablefmt="fancy_grid")
        out += '```'
        return out

def parse_deep_dive_info(text, type):
    dd = None
    for line in text.split('\n'):
        sline = [x.strip() for x in line.split('|')]
        if len(sline) > 2 and sline[0] == f'**{type}**':
            dd = DeepDive(type, sline[1], sline[2])
        if dd and len(sline) >= 6 and sline[0] == '':
            [stage, primary, secondary, anomaly, warning] = sline[1:6]
            # ignore header
            if stage == '**Stage**' or stage == ':-':
                continue
            dd.add_stage(stage, primary, secondary, anomaly, warning)
            if stage == '3':
                break
    return dd

reddit = praw.Reddit(
    client_id=os.environ['REDDIT_CLIENT_ID'],
    client_secret=os.environ['REDDIT_SECRET'],
    user_agent="my user agent",
    check_for_async=False
)
subreddit = reddit.subreddit("DeepRockGalactic")

def get_last_deep_dive_submission():
    for submission in subreddit.hot(limit=5):
        if "Weekly Deep Dives Thread" in submission.title:
            return submission
    return None

def get_last_deep_dive_info(raw=False):
    submission = get_last_deep_dive_submission()
    if not submission:
        return None
    text = submission.selftext
    if raw:
        return text
    
    dd = parse_deep_dive_info(text, 'Deep Dive')
    edd = parse_deep_dive_info(text, 'Elite Deep Dive')

    if not dd or not edd:
        return None

    url = f'**Source**: <{submission.url}>'
    title = f'**{submission.title}**'

    result = '\n'.join([title,
                      '',
                      dd.to_beautiful_string(),
                      edd.to_beautiful_string(),
                      url])
    print(f"result len: {len(result)}")
    return result

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    raw_cmd = ['/deep-dive-raw']
    dd_cmd = ['/deep-dive', '/deepdive', '/dd']
    if any(map(message.content.startswith, raw_cmd)):
        info = get_last_deep_dive_info(True)
        await message.channel.send(info)
        return
    if any(map(message.content.startswith, dd_cmd)):
        info = get_last_deep_dive_info()
        if info:
            await message.channel.send(info)
        return
    
client.run(os.environ['TOKEN'])