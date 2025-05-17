import feedparser
import discord
import os
import asyncio

# RSS-Feed URL
RSS_URL = "https://rss.app/feeds/6ylmybWwgG1OqovY.xml"

# Discord Bot Token und Channel ID aus Umgebungsvariablen
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # Die Discord Channel ID als Zahl

intents = discord.Intents.default()
client = discord.Client(intents=intents)

posted_entries = set()

async def check_feed():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print(f"Channel mit ID {CHANNEL_ID} wurde nicht gefunden.")
        return
    while not client.is_closed():
        feed = feedparser.parse(RSS_URL)
        for entry in reversed(feed.entries):
            if entry.id not in posted_entries:
                message = f"**{entry.title}**\n{entry.link}"
                await channel.send(message)
                posted_entries.add(entry.id)
        await asyncio.sleep(600)  # alle 10 Minuten prüfen

@client.event
async def on_ready():
    print(f"Bot ist eingeloggt als {client.user}")
    client.loop.create_task(check_feed())

client.run(DISCORD_TOKEN)
