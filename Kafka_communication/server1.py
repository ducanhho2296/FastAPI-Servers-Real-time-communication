import json
from kafka import KafkaProducer
from fastapi import FastAPI

app = FastAPI()

producer = KafkaProducer(
    bootstrap_servers=["your_server"],
    sasl_plain_username='username',
    sasl_plain_password='password',
    sasl_mechanism='mechanism',
    security_protocol='SASL_PLAINTEXT',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

@app.post("/send_message")
async def send_message(message: str):
    producer.send('fastapi_topic', {'message': message})
    return {"status": "Message sent"}


@app.get("/repeatly_request")
def repeat_request():
    count = 0
    while count <= 10:
        producer.send("fastapi_topic", {'message':count})
        print("The count message {} was sent".format(count))
        count += 1

    if msg.error():
        return {'error': str(msg.error())}

    # Return the response to the client
    return {'response': msg.value().decode('utf-8')}
