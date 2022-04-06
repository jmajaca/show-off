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
from model_utils import prepare_prediction_for_conversion


def load_data(train_validation_ratio=0.7) -> tuple[DataLoader, DataLoader, DataLoader]:
    test_dataset = SynthDataset(dir_path='../data/test')
    train_dataset = SynthDataset(dir_path='../data/train')
    validation_dataset_size = int((1 - train_validation_ratio) * len(train_dataset))
    train_dataset, validation_dataset = torch.utils.data.random_split(train_dataset, [len(train_dataset) - validation_dataset_size, validation_dataset_size])
    pad_collator = SynthPadCollator()
    test_dataloader = DataLoader(dataset=test_dataset, collate_fn=pad_collator, batch_size=1, shuffle=True)
    train_dataloader = DataLoader(dataset=train_dataset, collate_fn=pad_collator, batch_size=32, shuffle=True)
    validation_dataloader = DataLoader(dataset=validation_dataset, collate_fn=pad_collator, batch_size=32, shuffle=True)
    return train_dataloader, validation_dataloader, test_dataloader


def main():
    alphabet = env_model.alphabet
    train_dataloader, validation_dataloader, test_dataloader = load_data()
    converter = OCRLabelConverter(alphabet)
    model = CRNN(class_num=len(alphabet))
    model.to(torch.device('cuda:0' if torch.cuda.is_available() else 'cpu'))
    optimizer = Adam(params=model.parameters(), lr=1e-3)
    trainer = OCRTrainer(model, optimizer, converter=converter)
    trainer.train(train_dataloader, validation_dataloader, epoch_num=100, early_stop=10)

    truths, predictions = [], []
    for element, label in test_dataloader:
        prediction = model(element)

        pos, pred_sizes = prepare_prediction_for_conversion(prediction)

        pred_label = converter.decode(pos.data, pred_sizes.data)

        truths.append(label[0])
        predictions.append(pred_label)

    print(f'Word accuracy: {OCREvaluator.word_accuracy(truths, predictions)}')
    print(f'Word similarity: {OCREvaluator.word_sim(truths, predictions)}')
    torch.save(model.state_dict(), '../data/result/CRNN.pth')


if __name__ == '__main__':
    main()
