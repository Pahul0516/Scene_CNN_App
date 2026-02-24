import json
import base64
from app.config.rabbitmq_config import create_connection
from app.messiging.producer import send_label
from app.model.inference import SceneClassifier

EXCHANGE = "photo_exchange"
SERVICE_QUEUE = "scene_service_queue"

classifier = SceneClassifier()

def callback(ch, method, properties, body):
    try:
        message = json.loads(body.decode())
        file_name = message["fileName"]
        image_bytes = base64.b64decode(message["data"])

        label = classifier.predict_from_bytes(image_bytes)
        print(f"{file_name} → {label}")

        response_queue = "scene_response_queue"
        send_label(response_queue, {"fileName": file_name, "label": label})

        ch.basic_ack(delivery_tag=method.delivery_tag)

    except Exception as e:
        print("Error:", e)
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def start_consumer():
    connection = create_connection()
    channel = connection.channel()

    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type="fanout",
        durable=True
    )

    channel.queue_declare(queue=SERVICE_QUEUE, durable=True)

    channel.queue_bind(
        exchange=EXCHANGE,
        queue=SERVICE_QUEUE
    )

    channel.basic_consume(
        queue=SERVICE_QUEUE,
        on_message_callback=callback
    )

    print("Waiting for messages...")
    channel.start_consuming()