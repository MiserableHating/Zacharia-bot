import discord, asyncio, logging, sys, datetime, os, json
from discord.ext import commands

class help:
    def __init__(self, client):
        self.client = client

    print("Cog")

def setup(client):
    client.add_cog(help(client))
