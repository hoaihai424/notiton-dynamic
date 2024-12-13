import requests
import json
from fastapi import FastAPI, Depends, HTTPException
import pandas as pd

NOTION_API_KEY = "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"
NOTION_URL = "https://api.notion.com/v1/databases"
DATABASE_ID = "1532ec8473e9803ba028c913c45aa06b"

headers = {
    "Authorization": "Bearer " + NOTION_API_KEY,
    "Content-Type": "application/json", 
    "Notion-Version": "2022-06-28", 
}

app = FastAPI()

@app.get("/customers/{customer_id}")
async def get_customer(customer_id: str, num_pages: int = None):
    url = f"{NOTION_URL}/{DATABASE_ID}/query"

    page_size = 100 if num_pages is None else num_pages
    payload = {"page_size": page_size}

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    data = response.json()
    results = data["results"]
