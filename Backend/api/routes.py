# FastAPI routes (handles /analyze_list and /analyze_index)
from fastapi import APIRouter, UploadFile, File
from services.reddit_scraper import fetch_reddit_sentiment
from services.google_news_scraper import fetch_google_news_sentiment
from services.sentiment_analyzer import aggregate_sentiment
from utils.nse_utils import get_index_constituents

router = APIRouter()

@router.post('/analyze_list')
async def analyze_list(file: UploadFile = File(...), since: str = '2025-01-01', num_items: int = 20):
    companies = (await file.read()).decode().splitlines()
    results = {}
    for company in companies:
        news_score = fetch_google_news_sentiment(company, since, num_items)
        reddit_score = await fetch_reddit_sentiment(company, since, num_items)
        results[company] = aggregate_sentiment([reddit_score, news_score])
    return results

@router.get('/analyze_index/{index_name}')
async def analyze_index(index_name: str, since: str = '2025-01-01', num_items: int = 20):
    companies = get_index_constituents(index_name)
    results = {}
    for company in companies:
        news_score = fetch_google_news_sentiment(company, since, num_items)
        reddit_score = await fetch_reddit_sentiment(company, since, num_items)
        results[company] = aggregate_sentiment([reddit_score, news_score])
    return results
