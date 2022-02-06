import torch.nn.utils.rnn

from dataset.SynthDatasetInstance import SynthDatasetInstance


class SynthPadCollator:

    def __init__(self):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    def __call__(self, batch: list[SynthDatasetInstance]):
        """
        Arguments:
          batch:
            list of Instances returned by `Dataset.__getitem__`.
        Returns:
          A tensor representing the input batch.
        """
        images = torch.nn.utils.rnn.pad_sequence([instance.value.T for instance in batch], batch_first=True)
        images = images.permute(0, 3, 2, 1)
        images = images.to(self.device)
        labels = [instance.label for instance in batch]
        return images, labels
