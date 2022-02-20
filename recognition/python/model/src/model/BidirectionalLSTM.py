import torch.nn as nn


class BidirectionalLSTM(nn.Module):

    def __init__(self, input_size: int, hidden_size: int, out_size: int, batch_first=True):
        super().__init__()
        self.model = nn.LSTM(input_size=input_size, hidden_size=hidden_size, bidirectional=True, batch_first=batch_first)
        self.linear = nn.Linear(in_features=hidden_size * 2, out_features=out_size)

    def forward(self, x):
        x, _ = self.model(x)  # out: bxTxh
        b, T, h = x.size()
        x = x.reshape(T * b, h)  # out: (b*T)xh
        x = self.linear(x)  # out: (b*T)x(out_size)
        x = x.reshape(b, T, -1)  # out: bxTx(out_size)
        return x
