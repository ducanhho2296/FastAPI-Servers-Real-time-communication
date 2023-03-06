from fastapi import FastAPI
import uvicorn
import requests
app = FastAPI()

@app.get('/')
async def root():
    return {"message": "This is server 1"}

@app.get('/call_server2')
async def call_server2():
    response = requests.get("http://localhost:8001/")
    return {"message":response.json()["message"]}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
