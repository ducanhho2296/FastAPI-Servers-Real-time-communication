from fastapi import FastAPI
from confluent_kafka import Producer, Consumer

app = FastAPI()

# Set up Kafka producer and consumer
producer = Producer({'bootstrap.servers': 'kafka-broker-a:9092,kafka-broker-b:9092'})
consumer = Consumer({
