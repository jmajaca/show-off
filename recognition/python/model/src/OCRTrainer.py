from tqdm import tqdm

from dataset.OCRLabelConverter import OCRLabelConverter
from model.CRNN import CRNN

import torch
from torch.utils.data import DataLoader


class OCRTrainer:

    def __init__(self, model: CRNN, optimizer: torch.optim.Optimizer, converter: OCRLabelConverter):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = model
        self.optimizer = optimizer
        self.criterion = torch.nn.CTCLoss(reduction='mean', zero_infinity=True).to(self.device)
        self.converter = converter

    def train(self, train_dataloader: DataLoader, validate_dataloader: DataLoader, epoch_num: int, verbose=True):
        self.model.train()
        for epoch in range(epoch_num):
            cumulative_loss, count = 0, 0
            for batch, labels in tqdm(train_dataloader):
                prediction = self.model(batch)
                encoded_labels, labels_length = self.converter.encode(labels)

                batch_size, seq_size, class_size = prediction.size()
                pred_sizes = torch.LongTensor([seq_size for _ in range(batch_size)]).to(self.device)

                log_probs = prediction.log_softmax(2)
                log_probs = log_probs.permute(1, 0, 2)

                with torch.backends.cudnn.flags(enabled=False):
                    loss = self.criterion(log_probs, encoded_labels, pred_sizes, labels_length)
                    cumulative_loss += loss.item()
                    count += 1
                    loss.backward()

                self.optimizer.step()
                self.optimizer.zero_grad()
            if verbose:
                print(f'epoch: {epoch + 1}, loss: {cumulative_loss/count}')

    def validate(self, validate_dataloader: DataLoader, verbose=True):
        pass
