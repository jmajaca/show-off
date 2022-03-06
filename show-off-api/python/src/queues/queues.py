import dataclasses
import json
import logging
from abc import ABC, abstractmethod

import pika

import env
from models.image_api import ImageData, TextCorrection


class Queue(ABC):

    def __init__(self, queue: str, exchange: str = ''):
        self.__connection_params = pika.ConnectionParameters(
            host=env.QUEUE_HOST,
            port=env.QUEUE_PORT,
            virtual_host=env.QUEUE_VIRTUAL_HOST,
            credentials=pika.credentials.PlainCredentials(
                username=env.QUEUE_USERNAME,
                password=env.QUEUE_PASSWORD
            )
        )
        self.queue = queue
        self.exchange = exchange

    def _send_json(self, payload: dict, headers: dict):
        connection = pika.BlockingConnection(self.__connection_params)
        channel = connection.channel()
        channel.basic_publish(exchange=self.exchange, routing_key=self.queue, body=json.dumps(payload),
                              properties=pika.BasicProperties(content_type='application/json', headers=headers))
        connection.close()

    def _send_bytes(self, payload: bytes, headers: dict):
        connection = pika.BlockingConnection(self.__connection_params)
        channel = connection.channel()
        channel.basic_publish(exchange=self.exchange, routing_key=self.queue, body=payload,
                              properties=pika.BasicProperties(content_type='application/octet-stream', headers=headers))
        connection.close()

    @abstractmethod
    def send(self, payload, headers: dict):
        pass


class ImageQueue(Queue):

    def __init__(self):
        super().__init__(env.IMAGE_QUEUE_NAME)

    def send(self, payload: bytes, headers: dict):
        try:
            self._send_bytes(payload, headers)
        except Exception as e:
            logging.error(f"Error has occurred while sending request with headers {headers} on queue {self.queue}",
                          exc_info=True)


class ImageDataQueue(Queue):

    def __init__(self):
        super().__init__(env.IMAGE_DATA_QUEUE_NAME)

    def send(self, payload: ImageData, headers: dict):
        try:
            self._send_json(dataclasses.asdict(payload), headers)
        except Exception as e:
            logging.error(f"Error has occurred while sending request with headers {headers} on queue {self.queue}",
                          exc_info=True)


class TextCorrectionQueue(Queue):

    def __init__(self):
        super().__init__(env.TEXT_CORRECTION_QUEUE_NAME)

    def send(self, payload: TextCorrection, headers: dict):
        try:
            self._send_json(dataclasses.asdict(payload), headers)
        except Exception as e:
            logging.error(f"Error has occurred while sending request with headers {headers} on queue {self.queue}",
                          exc_info=True)
