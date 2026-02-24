import json
import pika

def send_label(queue_name: str, message: dict):
    """
    Send a JSON message to RabbitMQ
    """
    credentials = pika.PlainCredentials("guest", "guest")
    parameters = pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    channel.basic_publish(
        exchange="",
        routing_key=queue_name,
        body=json.dumps(message).encode("utf-8"),
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    connection.close()
    print(f"Sent message to {queue_name}: {message}")
