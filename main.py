import discord
import os
import praw
import random
from discord import app_commands
from tabulate import tabulate
from urllib3 import Retry

from random_drg import Build, is_valid_class

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
        line = line.replace('*', '')
        sline = [x.strip() for x in line.split('|')]
        if len(sline) > 2 and sline[0] == type:
            dd = DeepDive(type, sline[1], sline[2])
        if dd and len(sline) >= 6 and sline[0] == '':
            [stage, primary, secondary, anomaly, warning] = sline[1:6]
            # ignore header
            if stage == 'Stage' or stage == ':-':
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
    print('No deep dive submission found')
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
        print('No deep dive (or elite deep dive) info found')
        return None

    url = f'**Source**: <{submission.url}>'
    title = f'**{submission.title}**'

    result = '\n'.join([title,
                      '',
                      dd.to_beautiful_string(),
                      edd.to_beautiful_string(),
                      url])
    print(f"Result len: {len(result)}")
    return result

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print('Syncing commands')
    await tree.sync()
    print('We have logged in as {0.user}'.format(client))

@tree.command(name="deep-dive-info", description = "Get this week DD/EDD information")
async def deep_dive(interaction : discord.Interaction):
    info = get_last_deep_dive_info()
    if info:
        await interaction.response.send_message(info)

@tree.command(name="drg-rand-build", description = "Get a random build for DRG")
@app_commands.choices(character=[
        app_commands.Choice(name="Rand!", value='rand'),
        app_commands.Choice(name="Driller", value='driller'),
        app_commands.Choice(name="Scout", value='scout'),
        app_commands.Choice(name="Engineer", value='engineer'),
        app_commands.Choice(name="Gunner", value='gunner'),
        ])
async def rand_build(interaction : discord.Interaction, character : str):
    klass = character if character != 'rand' else random.choice(['driller', 'scout', 'engineer', 'gunner'])
    if is_valid_class(klass):
        build = Build(klass)
        await interaction.response.send_message(str(build))
    
client.run(os.environ['TOKEN'])