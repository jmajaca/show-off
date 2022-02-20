import torch
from PIL import Image
from torch.utils.data import DataLoader

import env_model
from dataset.OCRLabelConverter import OCRLabelConverter
from dataset.real.RealUnlabeledDataset import RealDataset
from dataset.real.RealUnlabeledPadCollator import RealPadCollator
from model.CRNN import CRNN
from model_utils import prepare_prediction_for_conversion


class ModelWrapper:

    def __init__(self, weights_path: str):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = CRNN(len(env_model.alphabet))
        self.model.load_state_dict(torch.load(weights_path, map_location=self.device))
        self.model.to(self.device)
        self.model.eval()
        self.converter = OCRLabelConverter(env_model.alphabet)
        self.collate_fn = RealPadCollator()

    def get_text(self, images: list[Image]) -> list[str]:
        for i, image in enumerate(images):
            if image.height != 32:
                new_width = 32 * image.width / image.height
                images[i] = image.resize((new_width, 32), Image.ANTIALIAS)
        dataset = RealDataset(images=images)
        dataloader = DataLoader(dataset=dataset, collate_fn=self.collate_fn, batch_size=len(images))
        for data in dataloader:
            prediction = self.model(data)
            return self.converter.decode(*prepare_prediction_for_conversion(prediction))
