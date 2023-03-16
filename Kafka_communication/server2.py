import json
from kafka import KafkaConsumer
from fastapi import FastAPI

app = FastAPI()

consumer = KafkaConsumer(
    'fastapi_topic',
    bootstrap_servers=["your_server"],
    sasl_plain_username='username',
    sasl_plain_password='password',
    sasl_mechanism='mechanism',
    security_protocol='SASL_PLAINTEXT',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def process_message(message):
    print(f"Received message: {message}")

# def kafka_consumer():
#     for message in consumer:
#         process_message(message.value)
#         messages.append(message.value)



# @app.get("/")
# async def kafka_consumer():
#     for message in consumer:
#         process_message(message.value)
#         return {"message:": message.value}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
for message in consumer:
    process_message(message.value)

