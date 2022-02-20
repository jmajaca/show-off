import torch


# TODO refactor into OCRLabelConverter
def prepare_prediction_for_conversion(prediction: torch.Tensor) -> tuple:
    batch_size, seq_size, class_size = prediction.size()
    pred_sizes = torch.LongTensor([seq_size for _ in range(batch_size)])
    prediction = prediction.permute(1, 0, 2)
    probs, pos = prediction.max(2)
    pos = pos.transpose(1, 0).contiguous().view(-1)
    return pos.data, pred_sizes.data
