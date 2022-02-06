import os

from PIL import Image
from torch.utils.data import Dataset
from torch.utils.data.dataset import T_co
from torchvision.transforms import transforms

from dataset.SynthDatasetInstance import SynthDatasetInstance


class SynthDataset(Dataset):

    def __init__(self, dir_path: str):
        super().__init__()
        images = os.listdir(dir_path)
        self.length = len(images)
        self.image_paths = [os.path.join(dir_path, image) for image in images]
        self.image_labels = [image.split('_')[0] for image in images]
        self.transform = transforms.Compose([
            transforms.Grayscale(num_output_channels=1),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])

    def __len__(self) -> int:
        return self.length

    def __getitem__(self, index) -> T_co:
        if index >= self.__len__():
            raise IndexError()
        image = Image.open(self.image_paths[index])
        image = self.transform(image)
        label = self.image_labels[index]
        return SynthDatasetInstance(value=image, label=label)
