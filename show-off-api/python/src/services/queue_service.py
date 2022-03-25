import logging

from werkzeug.datastructures import FileStorage

from models.detection_api import MinimalTextBox
from models.image_api import ImageBoxData, TextCorrection
from queues.queues import ImageQueue, ImageDataQueue, TextCorrectionQueue


log = logging.getLogger(__name__)


class QueueService:

    def __init__(self):
        self.image_queue = ImageQueue()
        self.image_data_queue = ImageDataQueue()
        self.text_correction_queue = TextCorrectionQueue()

    def send_image(self, request_id: str, file: FileStorage):
        log.info(f'Sending request with id {request_id} to queue {self.image_queue.queue}')
        self.image_queue.send(QueueService.__read_bytes_from_file(file), QueueService.__create_request_header(request_id))

    def send_image_data(self, request_id: str, boxes: list[MinimalTextBox], texts: list[str]):
        if len(boxes) != len(texts):
            log.warning(f'For request {request_id} there is missmatch in length of boxes and texts')
            return
        request = list(map(lambda box, text: ImageBoxData(box.start_x, box.start_y, box.width, box.height, text.text),
                           boxes, texts))
        log.info(f'Sending request with id {request_id} to queue {self.image_data_queue.queue}')
        self.image_data_queue.send(request, QueueService.__create_request_header(request_id))

    def send_text_correction(self, request_id: str, text_correction: str):
        log.info(f'Sending request with id {request_id} to queue {self.text_correction_queue.queue}')
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
