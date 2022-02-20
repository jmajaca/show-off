import collections

import torch


class OCRLabelConverter:

    def __init__(self, alphabet: str):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.__alphabet = alphabet
        self.__mapping = {}
        for i, char in enumerate(alphabet):
            self.__mapping[char] = i + 1

    def encode(self, text) -> tuple[torch.IntTensor, torch.IntTensor]:
        if isinstance(text, str):
            text = [self.__mapping[char] for char in text]
            length = [len(text)]
        elif isinstance(text, collections.Iterable):
            length = [len(s) for s in text]
            text = ''.join(text)
            text = [self.__mapping[char] for char in text]
        else:
            raise Exception('Invalid text type')
        text_tensor = torch.IntTensor(text).to(self.device)
        length_tensor = torch.IntTensor(length).to(self.device)
        return text_tensor, length_tensor

    def decode(self, t, length):
        if length.numel() == 1:
            length = length[0]
            assert t.numel() == length, "text with length: {} does not match declared length: {}".format(t.numel(),
                                                                                                         length)
            char_list = []
            for i in range(length):
                if t[i] != 0 and (not (i > 0 and t[i - 1] == t[i])):
                    char_list.append(self.__alphabet[t[i] - 1])
            return ''.join(char_list)
        else:
            # batch mode
            assert t.numel() == length.sum(), "texts with length: {} does not match declared length: {}".format(
                t.numel(), length.sum())
            texts = []
            index = 0
            for i in range(length.numel()):
                l = length[i]
                texts.append(
                    self.decode(t[index:index + l], torch.IntTensor([l])))
                index += l
            return texts
