from tqdm import tqdm

from dataset.OCRLabelConverter import OCRLabelConverter
from model.CRNN import CRNN

import torch
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader


class OCRTrainer:

    def __init__(self, model: CRNN, optimizer: torch.optim.Optimizer, converter: OCRLabelConverter):
        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = model
        self.optimizer = optimizer
        self.criterion = torch.nn.CTCLoss(reduction='mean', zero_infinity=True).to(self.device)
        self.converter = converter

    def train(self, train_dataloader: DataLoader, validate_dataloader: DataLoader, epoch_num: int, verbose=True,
              early_stop=None):
        self.model.train()
        validation_loss = []
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
                print(f'epoch: {epoch + 1}, train loss: {cumulative_loss / count}')

            current_validation_loss = self.validate(validate_dataloader, epoch, verbose=verbose)

            if early_stop is not None:
                if len(validation_loss) == 0:
                    activate_early_stop = False
                else:
                    activate_early_stop = True
                for former_validation_loss in validation_loss[-early_stop:]:
                    if current_validation_loss < former_validation_loss:
                        activate_early_stop = False
                        break
                if activate_early_stop:
                    print('Early stop activated, stopping model training')
                    OCRTrainer.__draw_validation_graph(validation_loss)
                    return
                else:
                    validation_loss.append(current_validation_loss)

        if verbose:
            OCRTrainer.__draw_validation_graph(validation_loss)

    def validate(self, validate_dataloader: DataLoader, epoch, verbose=True):
        cumulative_loss, count = 0, 0
        with torch.no_grad():
            for batch, labels in tqdm(validate_dataloader):
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

        validation_loss = cumulative_loss / count

        if verbose:
            print(f'epoch: {epoch + 1}, validation loss: {validation_loss}')

        return validation_loss

    @staticmethod
    def __draw_validation_graph(validation_loss: list) -> None:
        plt.plot([_ + 1 for _ in range(len(validation_loss))], validation_loss)
        plt.xlabel('Epochs')
        plt.ylabel('Validation loss')
        plt.show()

