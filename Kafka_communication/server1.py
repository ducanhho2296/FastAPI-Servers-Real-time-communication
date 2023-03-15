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

@app.post('/send-request')
async def send_request(request: dict):
    # Send the request as a message to the Kafka topic
    producer.produce('request-topic', value=request)

    # Wait for a response from Server B
    msg = consumer.poll(10.0)

    if msg is None:
        return {'error': 'Request timed out'}

    if msg.error():
        return {'error': str(msg.error())}

    # Return the response to the client
    return {'response': msg.value().decode('utf-8')}
