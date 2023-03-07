from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from tortoise import fields
import tortoise
app = FastAPI()

# Define the database connection settings
DATABASE_URL = "postgres://user:password@localhost:5432/mydatabase"

# Define the database models

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)

