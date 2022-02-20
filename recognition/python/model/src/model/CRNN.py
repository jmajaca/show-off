import torch.nn as nn

from python.model.src.model.BidirectionalLSTM import BidirectionalLSTM


class CRNN(nn.Module):

    def __init__(self, class_num: int):
        super().__init__()
        self.height = 32
        # input is Bx1xHxW, H=32, Bx1x32xW
        self.cnn = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=64, kernel_size=(3, 3), stride=(1, 1), padding=1),  # Bx64x16xW
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2, 2), stride=2),  # Bx64x16xW/2
            nn.Conv2d(in_channels=64, out_channels=128, kernel_size=(3, 3), stride=(1, 1), padding=1),  # Bx128x16xW/2
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2, 2), stride=2),  # Bx128x8xW/4
            nn.Conv2d(in_channels=128, out_channels=256, kernel_size=(3, 3), stride=(1, 1), padding=1),  # Bx256x8xW/4
            nn.BatchNorm2d(num_features=256),
            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=(3, 3), stride=(1, 1), padding=1),  # Bx256x8xW/4
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 1), padding=(0, 1)),
            nn.Conv2d(in_channels=256, out_channels=512, kernel_size=(3, 3), stride=(1, 1), padding=1),
            nn.BatchNorm2d(num_features=512),
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=(3, 3), stride=(1, 1), padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(2, 2), stride=(2, 1), padding=(0, 1)),
            nn.Conv2d(in_channels=512, out_channels=512, kernel_size=(2, 2), stride=(1, 1), padding=0),
            nn.BatchNorm2d(num_features=512),
        )
        self.rnn = nn.Sequential(
            BidirectionalLSTM(input_size=512, hidden_size=256, out_size=256),
            BidirectionalLSTM(input_size=256, hidden_size=256, out_size=class_num),
        )

    def forward(self, x):
        x = self.cnn(x)  # out: Bx512x1xW/4
        x = x.squeeze(2)  # out: Bx512xW/4
        x = x.permute(0, 2, 1)  # out: BxW/4x512
        x = self.rnn(x)  # out: BxW/4x(class_num)
        return x
