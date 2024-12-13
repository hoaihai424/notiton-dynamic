import requests
import json
import pandas as pd

NOTION_API_KEY = "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"
NOTION_URL = "https://api.notion.com/v1/databases"

headers = {
    "Authorization": "Bearer " + NOTION_API_KEY,
    "Content-Type": "application/json", # the request and response content type is JSON
    "Notion-Version": "2022-06-28", 
}

