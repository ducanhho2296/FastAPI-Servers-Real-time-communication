from fastapi import FastAPI
import uvicorn
import requests
app = FastAPI()

@app.get('/')
async def root():
    return {"message": "This is server 2"}

@app.get('/call_server2')
async def call_server2():
    response = requests.get("http://localhost:8000/")
    return {"message":response.json()["message"]}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)