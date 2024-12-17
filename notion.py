import requests
import json
import pandas as pd

NOTION_API_KEY = "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"
NOTION_URL = "https://api.notion.com/v1/pages"
PAGE_ID = "15b2ec8473e98007885fe7ec343ff6df"

headers = {
    "Authorization": "Bearer " + NOTION_API_KEY,
    "Content-Type": "application/json", 
    "Notion-Version": "2022-06-28", 
}

#create
def data_conversion_4_adding_row(data: dict):
    response = {}
    for x in data:
        if data[x]["type"] == "title":
            tmp_data = {"title" : [{"text": {"content": data[x]["value"]}}]}
        elif data[x]["type"] == "number":
            tmp_data = {"number": data[x]["value"]}
        elif data[x]["type"] == "rich_text":
            tmp_data = {"rich_text": [{"text": {"content": data[x]["value"]}}]}
        elif data[x]["type"] == "date":
            tmp_data = {"date": {"start": data[x]["value"], "end": None}}
        elif data[x]["type"] == "url":
            tmp_data = {"url": data[x]["value"]}
        response.update({x: tmp_data})

    return {"properties": response}

def data_conversion_4_create(data: dict):
    response = {}
    has_title = False
    for x in data:
        if data[x]["type"] == "title":
            tmp_data = {"title" : {}}
            has_title = True

        elif data[x]["type"] == "number":
            tmp_data = {"number": {}}

        elif data[x]["type"] == "rich_text":
            tmp_data = {"rich_text": {}}

        elif data[x]["type"] == "date":
            tmp_data = {"date": {}}

        elif data[x]["type"] == "url":
            tmp_data = {"url": {}}         

        response.update({x: tmp_data})
    
    if not has_title:
        response.update({"Title": {"title": {}}})
    return {"properties": response}

def add_data(id:str, data: dict):
    payload = {
        "parent" : {"database_id" : id} 
    }
    payload.update(data_conversion_4_adding_row(data))
    response = requests.post("https://api.notion.com/v1/pages", headers=headers, json=payload)

    if response.status_code == 400:
        print("Failed to add row")
        return response.json()
    
    print("Row added successfully")
    return response.json()

def create_customer(id:str, data: dict):
    payload = {
        "parent" : {"type": "page_id", "page_id": PAGE_ID},
        "title": [{
            "type": "text",
            "text": {"content": id}
        }]
    }
    payload.update(data_conversion_4_create(data))
    response = requests.post("https://api.notion.com/v1/databases", headers=headers, json=payload)

    if response.status_code == 400:
        print("Failed to create customer")
        return response.json()
    
    print("Customer created successfully")

    add_data(response.json()["id"], data)

    return response.json()

#read
def read_db():
    url = f"https://api.notion.com/v1/blocks/{PAGE_ID}/children"
    response = requests.get(url, headers=headers)

    data = response.json()
    result = data["results"]

    while data["has_more"]:
        next_url = url + f"?start_cursor={data['next_cursor']}"
        response = requests.get(next_url, headers=headers)
        data = response.json()  
        result += data["results"]

    if result == []: 
        return None
    return result

def display_db():
    res = read_db()
    if res == None:
        return None

    for i in range(len(res)):
        print(res[i]["child_database"]["title"])

def display_customer_data(dbID : str):
    url = f"https://api.notion.com/v1/databases/{dbID}/query"
    response = requests.post(url, headers=headers, json={"page_size": 100})

    data = response.json()

    with open("output.json", "w") as f:
        json.dump(data, f, indent=4)

    result = data["results"]

    if result == []: 
        return None

    while data["has_more"]:
        next_url = url + f"?start_cursor={data['next_cursor']}"
        response = requests.post(next_url, headers=headers)
        data = response.json()  
        result += data["results"]

    for x in result:
        for y in x["properties"]:
            if x["properties"][y]["type"] == "title":
                print(x["properties"][y]["title"][0]["text"]["content"], end=", ")
            elif x["properties"][y]["type"] == "number":
                print(x["properties"][y]["number"], end=", ")
            elif x["properties"][y]["type"] == "rich_text":
                print(x["properties"][y]["rich_text"][0]["text"]["content"], end=", ")
            elif x["properties"][y]["type"] == "date":
                print(x["properties"][y]["date"]["start"], end=", ")
            elif x["properties"][y]["type"] == "url":
                print(x["properties"][y]["url"], end=", ")
        print()

    

def get_customer_data(customer_ID : str):
    res = read_db()
    if res == None:
        return None
    
    for i in range(len(res)):
        if res[i]["child_database"]["title"] == customer_ID:
            return display_customer_data(res[i]["id"])
    
    return None

#update


#delete

