import torch
from torch.utils.data import DataLoader
from torch.optim.adam import Adam

import env_model
from OCREvaluator import OCREvaluator
from OCRTrainer import OCRTrainer
from dataset.OCRLabelConverter import OCRLabelConverter
from dataset.synth.SynthDataset import SynthDataset
from dataset.synth.SynthPadCollator import SynthPadCollator
from model.CRNN import CRNN


def load_data(train_validation_ratio=0.7) -> tuple[DataLoader, DataLoader, DataLoader]:
    train_dataset = SynthDataset(dir_path='../data/train')
    test_dataset = SynthDataset(dir_path='../data/test')
    pad_collator = SynthPadCollator()
    train_dataloader = DataLoader(dataset=train_dataset, collate_fn=pad_collator, batch_size=32, shuffle=True)
    test_dataloader = DataLoader(dataset=test_dataset, collate_fn=pad_collator, batch_size=1, shuffle=True)
    return train_dataloader, train_dataloader, test_dataloader


def main():
    alphabet = model_env.alphabet
    train_dataloader, validation_dataloader, test_dataloader = load_data()
    converter = OCRLabelConverter(alphabet)
    model = CRNN(class_num=len(alphabet))
    model.to(torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'))
    optimizer = Adam(params=model.parameters(), lr=1e-3)
    trainer = OCRTrainer(model, optimizer, converter=converter)
    trainer.train(train_dataloader, train_dataloader, epoch_num=6)

    truths, predictions = [], []
    for element, label in test_dataloader:
        prediction = model(element)
        batch_size, seq_size, class_size = prediction.size()
        pred_sizes = torch.LongTensor([seq_size for _ in range(batch_size)])
        prediction = prediction.permute(1, 0, 2)

        # refactor this chunk
        probs, pos = prediction.max(2)
        pos = pos.transpose(1, 0).contiguous().view(-1)

        pred_label = converter.decode(pos.data, pred_sizes.data)
        print(f'label={label[0]}, predicted_label={pred_label}')
        truths.append(label[0])
        predictions.append(pred_label)
    print(f'Word accuracy: {OCREvaluator.word_accuracy(truths, predictions)}')
    print(f'Word similarity: {OCREvaluator.word_sim(truths, predictions)}')
    torch.save(model.state_dict(), '../data/result/CRNN.pth')


if __name__ == '__main__':
    main()
