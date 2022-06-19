# Environment Variables

Function requres two variables defined in .env file:

```
CLICKUP_KEY=
DISCORD_WEBHOOK=
```

Clickup key can be found in https://app.clickup.com/6624359/settings/apps
Discord webhook can be found in https://discord.com/channels/985949569852506172/985949570381017232 in Integrations / Webhooks

For SAM testing, define same variables in env.json file in following format:

```
{
    "ClickupDailyFunction": {
        "CLICKUP_KEY": "",
        "DISCORD_WEBHOOK": ""
    }
}
```
