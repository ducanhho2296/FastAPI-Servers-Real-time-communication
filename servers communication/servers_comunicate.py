from fastapi import FastAPI
import uvicorn
import requests


app = FastAPI()

@app.get('/call_server2')
async def call_server2():
    response = requests.get("http://localhost:8001/")
    return {"message":response.json()["message"]}

