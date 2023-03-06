from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "This is server 1"}

app2 = FastAPI()
@app2.get('/')
async def root():
    return {"message": "This is server 2"}

if __name__ == '__main__':
    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app2, host="0.0.0.0", port=8000)