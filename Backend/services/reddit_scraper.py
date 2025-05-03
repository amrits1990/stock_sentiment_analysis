import asyncpraw
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

async def fetch_reddit_sentiment(company, since, num_items):
    # Create Reddit instance INSIDE the async function (don't globalize it!)
    reddit = asyncpraw.Reddit(
        client_id=os.getenv("REDDIT_CLIENT_ID"),
        client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        user_agent="SentimentAnalysisApp/0.1 by u/yourusername"
    )

    query = company
    texts = []
    since_date = datetime.strptime(since, "%Y-%m-%d")
    try:
        subreddit = await reddit.subreddit('all')

        async for post in subreddit.search(query, limit=num_items, sort='relevance', time_filter='month'):
            title = post.title if post.title else ""
            selftext = post.selftext if post.selftext else ""
            texts.append(f"{title} {selftext}")

            await asyncio.sleep(1)  # Rate-limit

    except Exception as e:
        print(f"Error fetching Reddit posts for {company}: {e}")

    await reddit.close()  # Properly close session

    return texts