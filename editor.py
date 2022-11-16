import json
import requests
import pprint

url = "https://100058.pythonanywhere.com/dowelleditor/editor/"
    #searchstring="ObjectId"+"("+"'"+"6139bd4969b0c91866e40551"+"'"+")"
payload = {
    "database" : "social-media-auto",
    'collection': "step2_data",
    "fields": "title",
    "document_id": "62fd1ed5cee6d0752b849cc6"
    }
headers = {
    'Content-Type': 'application/json'
    }

response = requests.post(url,data=payload)
print(response.text)

