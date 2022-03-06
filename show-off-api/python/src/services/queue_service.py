import base64
import dataclasses
import json
import logging

import pika
from werkzeug.datastructures import FileStorage

import env
from models.detection_api import MinimalTextBox
from models.image_api import ImageBoxData, ImageData


class QueueService:

    def __init__(self):
        self.__connection_params = pika.ConnectionParameters(
            host=env.QUEUE_HOST,
            port=env.QUEUE_PORT,
            virtual_host=env.QUEUE_VIRTUAL_HOST,
            credentials=pika.credentials.PlainCredentials(
                username=env.QUEUE_USERNAME,
                password=env.QUEUE_PASSWORD
            )
        )

    def __send(self, payload, queue: str, exchange: str = ''):
        connection = pika.BlockingConnection(self.__connection_params)
        channel = connection.channel()
        channel.basic_publish(exchange=exchange, routing_key=queue, body=json.dumps(dataclasses.asdict(payload)),
                              properties=pika.BasicProperties(content_type='application/json'))
        connection.close()

    def send_image_data(self, request_id: str, image: FileStorage, boxes: list[MinimalTextBox], text: str, queue: str):
        send_boxes = list(map(lambda box: ImageBoxData(box.start_x, box.start_y, box.width, box.height), boxes))
        # TODO send file bytes on another queue
        image.stream.seek(0)
        file_bytes = image.stream.read()
        image_string = base64.b64encode(file_bytes).decode('utf-8')
        request = ImageData(request_id, image_string, send_boxes, text)
        image.stream.seek(0)
        logging.info(f'Sending request with id {request_id} to queue {queue}')
        try:
            self.__send(request, queue)
        except Exception as e:
            logging.error(f'Error has occurred while sending request with id {request_id} to queue {queue}',
                          exc_info=True)
