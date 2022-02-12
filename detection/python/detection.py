from third_party.ctpn_predict import get_det_boxes


class Detection:

    @staticmethod
    def get_text_boxes(image):
        text_boxes = get_det_boxes(image)
        return sorted(text_boxes, key=lambda box: (min(box[1:-1:2]), min(box[::2])))
