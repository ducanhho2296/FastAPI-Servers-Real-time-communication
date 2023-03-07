from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import fields
import tortoise
app = FastAPI()

# Define the database connection settings
DATABASE_URL = "postgres://user:password@localhost:5432/mydatabase"

@app.get('/call_server2')
async def call_server2():
    response = requests.get("http://localhost:8001/")
    return {"message":response.json()["message"]}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)

