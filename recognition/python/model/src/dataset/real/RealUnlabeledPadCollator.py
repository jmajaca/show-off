import torch.nn.utils.rnn


class RealPadCollator:

    def __init__(self):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

    def __call__(self, batch: list[torch.Tensor]):
        images = torch.nn.utils.rnn.pad_sequence([instance.T for instance in batch], batch_first=True)
        images = images.permute(0, 3, 2, 1)
        images = images.to(self.device)
        return images
