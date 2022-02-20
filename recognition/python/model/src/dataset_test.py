from torch.utils.data import DataLoader

from dataset.SynthPadCollator import SynthPadCollator
from dataset.SynthDataset import SynthDataset

import numpy as np
import matplotlib.pyplot as plt


def main():
    train_dataset = SynthDataset(dir_path='../data/train')
    train_dataloader = DataLoader(dataset=train_dataset, collate_fn=SynthPadCollator(), batch_size=5, shuffle=True)
    for instance, label in train_dataloader:
        to_show = np.squeeze(instance[0])
        plt.title(label[0])
        plt.imshow(to_show)
        plt.axis('off')
        plt.show()
        break


if __name__ == '__main__':
    main()
