from fastapi import FastAPI
import uvicorn
import cv2

app = FastAPI()
cap = cv2.VideoCapture(0)

@app.post("/start")
async def start_inference():
    print('Start model inference')
 
    pass

