from dotenv import load_dotenv
import os
from client.bot import *

load_dotenv()
discord_token = os.getenv('DISCORD_TOKEN')

client.run(discord_token)
