import cv2

from detection import Detection

if __name__ == '__main__':
    img_path = 'images/ocr4.jpg'
    image = cv2.imread(img_path)
    result = Detection.get_text_boxes(image)
    print(result)
