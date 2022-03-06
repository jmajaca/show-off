import logging

from werkzeug.datastructures import FileStorage

from models.detection_api import MinimalTextBox
from models.image_api import ImageBoxData, ImageData, TextCorrection
from queues.queues import ImageQueue, ImageDataQueue, TextCorrectionQueue


class QueueService:

    def __init__(self):
        self.image_queue = ImageQueue()
        self.image_data_queue = ImageDataQueue()
        self.text_correction_queue = TextCorrectionQueue()

    def send_image(self, request_id: str, file: FileStorage):
        logging.info(f'Sending request with id {request_id} to queue {self.image_queue.queue}')
        self.image_queue.send(QueueService.__read_bytes_from_file(file), QueueService.__create_request_header(request_id))

    def send_image_data(self, request_id: str, boxes: list[MinimalTextBox], text: str):
        send_boxes = list(map(lambda box: ImageBoxData(box.start_x, box.start_y, box.width, box.height), boxes))
        request = ImageData(request_id, send_boxes, text)
        logging.info(f'Sending request with id {request_id} to queue {self.image_data_queue.queue}')
        self.image_data_queue.send(request, QueueService.__create_request_header(request_id))

    def send_text_correction(self, request_id: str, text_correction: str):
        logging.info(f'Sending request with id {request_id} to queue {self.text_correction_queue.queue}')
        self.text_correction_queue.send(TextCorrection(request_id, text_correction),
                                        QueueService.__create_request_header(request_id))

    @staticmethod
    def __read_bytes_from_file(file: FileStorage):
        file.stream.seek(0)
        file_bytes = file.read()
        file.stream.seek(0)
        return file_bytes

    @staticmethod
    def __create_request_header(request_id: str):
        return {'request_id': request_id}
