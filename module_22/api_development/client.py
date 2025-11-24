import requests
from pydantic import BaseModel
import uvicorn


api_url ="http://127.0.0.1:8000/create_person"

person_data = {
    "Name": "John Doe",
    "age": 30,
}

response = requests.post(api_url, json=person_data)
print("Response code:", response.status_code )
print("Response JSON",response.json())