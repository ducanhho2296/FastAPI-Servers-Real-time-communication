from confluent_kafka import Producer, Consumer
import json


# Set up Kafka producer and consumer
producer = Producer({'bootstrap.servers': 'kafka-broker-a:9092,kafka-broker-b:9092'})
consumer = Consumer({
    'bootstrap.servers': 'kafka-broker-a:9092,kafka-broker-b:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
})
consumer.subscribe(['request-topic'])

def process_request(request):
    # Parse the request message
    data = json.loads(request)

    # Process the request
    # ...
    # Perform the necessary processing here, and generate a response message

    response = {'message': 'Hello from Server B'}

    # Return the response message
    return json.dumps(response)

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        print(f'Error: {msg.error()}')
        continue

    # Process the request
    request = msg.value().decode('utf-8')
    response = process_request(request)

    # Send the response as a message to the Kafka topic
    producer.produce('response-topic', value=response.encode('utf-8'))
