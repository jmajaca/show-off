from PIL import Image
from torch.utils.data import Dataset
from torch.utils.data.dataset import T_co
from torchvision.transforms import transforms


class RealDataset(Dataset):

    def __init__(self, images: list[Image]):
        super().__init__()
        self.images = images
        self.length = len(images)
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
        image = self.images[index]
        image = self.transform(image)
        return image
