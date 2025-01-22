import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
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

#retrieve
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

    with open("data.json", "w") as f:
        json.dump(result, f, indent=4)

    if result == []: 
        return None
    return result

def display_db():
    res = read_db()
    if res == None:
        return None
    
    list_of_data = []

    for i in range(len(res)):
        try:
            list_of_data.append(res[i]["child_database"]["title"])
        except KeyError:
            continue

    return list_of_data

def get_data(dbID : str):
    url = f"https://api.notion.com/v1/databases/{dbID}/query"
    response = requests.post(url, headers=headers, json={"page_size": 100})

    data = response.json()
    result = data["results"]

    if result == []: 
        return None

    while data["has_more"]:
        next_url = url + f"?start_cursor={data['next_cursor']}"
        response = requests.post(next_url, headers=headers)
        data = response.json()  
        result += data["results"]
    
    return result

def display_customer_data(dbID : str):
    result = get_data(dbID)
    list_of_data = {}
    idx = 0

    for x in result:
        list_of_data.update({idx: {}})
        for y in x["properties"]:
            try: 
                if x["properties"][y]["type"] == "title":
                    list_of_data[idx].update({y: x["properties"][y]["title"][0]["text"]["content"]})
                elif x["properties"][y]["type"] == "number":
                    list_of_data[idx].update({y: x["properties"][y]["number"]})
                elif x["properties"][y]["type"] == "rich_text":
                    list_of_data[idx].update({y: x["properties"][y]["rich_text"][0]["text"]["content"]})
                elif x["properties"][y]["type"] == "date":
                    list_of_data[idx].update({y: x["properties"][y]["date"]["start"]})
                elif x["properties"][y]["type"] == "url":
                    list_of_data[idx].update({y: x["properties"][y]["url"]})
            except IndexError:
                list_of_data[idx].update({y: None})
        idx += 1

    return list_of_data

def get_customer_data(customer_ID : str):
    res = read_db()
    for i in range(len(res)):
        if res[i]["child_database"]["title"] == customer_ID:
            return display_customer_data(res[i]["id"])
    
    return "No such customer"

#update
def changeID(new_name: str, dbID: str):
    payload = {
        "title": [
            {
                "type": "text",
                "text": {
                    "content": new_name
                }
            }
        ]
    }

    url = f"https://api.notion.com/v1/databases/{dbID}"
    response = requests.patch(url, headers=headers, json=payload)

    return response.json()

def get_key_field(data: dict):
    for x in data.keys():
        if data[x]["type"] == "title":
            return x
        
    return None

def update_customer_db(id : str, data: dict, data_id : str):
    key_field = get_key_field(data)
    res = get_data(id)

    try:
        for x in res:
            if x["properties"][key_field]["title"][0]["text"]["content"] == data_id:
                payload = data_conversion_4_adding_row(data)
                pageid = x["id"]
                url = f"https://api.notion.com/v1/pages/{pageid}"
                response = requests.patch(url, headers=headers, json=payload)

                return response.json()
    except KeyError:
        return {"message": "Data not found"}

#delete
def delete_customer_db(id : str):
    url = f"https://api.notion.com/v1/databases/{id}"
    response = requests.patch(url, headers=headers, json={"archived": True})

    return response.json()

def delete_data(customer_id: str, row_id: str):
    tmp = get_data(customer_id)

    if not tmp:
        return {"message": "No data found"}

    key_field = ""

    for x in tmp[0]["properties"]:
        if tmp[0]["properties"][x]["type"] == "title":
            key_field = x
            break

    pageID = None
    for x in tmp:
        if x["properties"][key_field]["title"][0]["text"]["content"] == row_id:
            pageID = x["id"]
            break

    if not pageID:
        return {"message": "Row ID not found"}

    url = f"https://api.notion.com/v1/pages/{pageID}"
    response = requests.patch(url, headers=headers, json={"archived": True})

    if response.status_code == 200:
        return {"message": "Data deleted successfully"}
    else:
        return {"message": "Failed to delete data", "details": response.json()}