from fastapi import FastAPI
from confluent_kafka import Producer, Consumer

app = FastAPI()

# Set up Kafka producer and consumer
producer = Producer({'bootstrap.servers': 'kafka-broker-a:9092,kafka-broker-b:9092'})
consumer = Consumer({
    'bootstrap.servers': 'kafka-broker-a:9092,kafka-broker-b:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['response-topic'])

@app.post('/send-request')
async def send_request(request: dict):
    # Send the request as a message to the Kafka topic
    producer.produce('request-topic', value=request)

