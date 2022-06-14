import os
import time
from dotenv import load_dotenv
from discord_webhook import DiscordWebhook, DiscordEmbed
from loguru import logger

load_dotenv()
DISCORD_WEBHOOK=os.environ.get('DISCORD_WEBHOOK')


def send(message: str):
    try:
        webhook = DiscordWebhook(url=DISCORD_WEBHOOK, content=message, rate_limit_retry=True)
        response = webhook.execute()
        response.raise_for_status()
        return webhook, response
    except:
        logger.exception("Discord webhook exception")


if __name__ == '__main__':
    webhook, response = send("Hello World!")
    time.sleep(5)
    webhook.delete(response)
