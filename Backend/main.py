# FastAPI app entry point
from fastapi import FastAPI
from api import routes
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import sys

app = FastAPI()
app.include_router(routes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

@app.get('/')
def root():
    return {'message': 'Stock Sentiment Backend Ready'}

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=9321, reload ='True')