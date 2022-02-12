import torch.nn as nn
import torchvision.models as models


class BasicConv(nn.Module):
    def __init__(self, in_planes: int, out_planes: int, kernel_size: tuple, stride: tuple = (1, 1),
                 padding: int = 0, dilation: tuple = (1, 1), groups: int = 1, relu: bool = True,
                 bn: bool = True, bias: bool = True):
        super(BasicConv, self).__init__()
        self.out_channels = out_planes
        self.conv = nn.Conv2d(in_planes, out_planes, kernel_size=kernel_size, stride=stride, padding=padding,
                              dilation=dilation, groups=groups, bias=bias)
        self.bn = nn.BatchNorm2d(out_planes, eps=1e-5, momentum=0.01, affine=True) if bn else None
        self.relu = nn.ReLU(inplace=True) if relu else None

    def forward(self, x):
        x = self.conv(x)
        if self.bn is not None:
            x = self.bn(x)
        if self.relu is not None:
            x = self.relu(x)
        return x


class CTPN(nn.Module):
    def __init__(self):
        super().__init__()
        base_model = models.vgg16(pretrained=False)
        self.base_layers: nn.Sequential = base_model.features[:-1]  # block5_conv3 output
        self.rpn = BasicConv(512, 512, (3, 3), (1, 1), 1, bn=False)
        self.brnn = nn.GRU(512, 128, bidirectional=True, batch_first=True)
        self.lstm_fc = BasicConv(256, 512, (1, 1), (1, 1), relu=True, bn=False)
        self.rpn_class = BasicConv(512, 10 * 2, (1, 1), (1, 1), relu=False, bn=False)
        self.rpn_regress = BasicConv(512, 10 * 2, (1, 1), (1, 1), relu=False, bn=False)

    def forward(self, x):
        x = self.base_layers(x)
        # rpn
        x = self.rpn(x)  # [b, c, h, w]

        x1 = x.permute(0, 2, 3, 1).contiguous()  # channels last   [b, h, w, c]
        b = x1.size()  # b, h, w, c
        x1 = x1.view(b[0] * b[1], b[2], b[3])

        x2, _ = self.brnn(x1)

        xsz = x.size()
        x3 = x2.view(xsz[0], xsz[2], xsz[3], 256)  # torch.Size([4, 20, 20, 256])

        x3 = x3.permute(0, 3, 1, 2).contiguous()  # channels first [b, c, h, w]
        x3 = self.lstm_fc(x3)
        x = x3

        cls = self.rpn_class(x)
        regress = self.rpn_regress(x)

        cls = cls.permute(0, 2, 3, 1).contiguous()
        regress = regress.permute(0, 2, 3, 1).contiguous()

        cls = cls.view(cls.size(0), cls.size(1) * cls.size(2) * 10, 2)
        regress = regress.view(regress.size(0), regress.size(1) * regress.size(2) * 10, 2)

        return cls, regress
