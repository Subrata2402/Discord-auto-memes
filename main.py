import discord
import aiohttp
import asyncio
import asyncpraw

webhook_url = "" # Put discord channel Webhook url

async def main():
    reddit = asyncpraw.Reddit(
        client_id = "", # Put your reddit client id
        client_secret = "", # Put your reddit client secret
        username = "", # Put username here
        password = "", # Put password here
        user_agent = "" # Put anything in user agent
        )
    subreddit = await reddit.subreddit("memes") # You can change subreddit here
    
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(webhook_url, adapter=discord.AsyncWebhookAdapter(session))
        async for submission in subreddit.top(limit=None): # You can set limit how many memes do you want to retrieve
            name = submission.title
            image = submission.url
            score = submission.score
            permalink = submission.permalink
            link = "https://www.reddit.com" + permalink
            num_comments = submission.num_comments
            embed=discord.Embed(description=f"**[{name}]({link})**")
            embed.set_image(url=image)
            embed.set_footer(text=f"👍 {score} | 💬 {num_comments}")
            if not submission.over_18 and not submission.is_video:
                await webhook.send(embed=embed, username="Camelia")
                print(name)
                await asyncio.sleep(60) # You can change loop timing here in seconds

    await main()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
