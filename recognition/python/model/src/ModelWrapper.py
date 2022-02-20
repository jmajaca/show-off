import torch
from PIL import Image
from torchvision.transforms import transforms

import model_env
from dataset.OCRLabelConverter import OCRLabelConverter
from model.CRNN import CRNN
from model_utils import prepare_prediction_for_conversion


class ModelWrapper:

    def __init__(self, weights_path: str):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = CRNN(len(model_env.alphabet))
        self.model.load_state_dict(torch.load(weights_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
        self.converter = OCRLabelConverter(model_env.alphabet)
        self.transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=1),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])

    def get_text(self, images: list[Image]) -> str:
        transformed_images: list[torch.Tensor] = []
        for image in images:
            if image.height != 32:
                new_width = 32 * image.width / image.height
                image = image.resize((new_width, 32), Image.ANTIALIAS)
            image = self.transform(image)
            transformed_images.append(image)
        tensor = transformed_images[0].unsqueeze(0).to(self.device)
        if len(transformed_images) != 1:
            pass
        prediction = self.model(tensor)
        return self.converter.decode(*prepare_prediction_for_conversion(prediction))
