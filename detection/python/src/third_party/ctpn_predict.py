import os

import numpy as np

import torch
import torch.nn.functional as F

from third_party import ctpn_config
from third_party.ctpn_utils import gen_anchor, bbox_transfor_inv, clip_box, filter_bbox, nms, TextProposalConnectorOriented

from third_party.ctpn_model import CTPN

prob_thresh = 0.5
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
weights = os.path.join(ctpn_config.WEIGHTS_FILE)

model = CTPN()
model.load_state_dict(torch.load(weights, map_location=device)['model_state_dict'])
model.to(device)
model.eval()


def get_det_boxes(image: np.ndarray) -> np.ndarray:
    h, w = image.shape[:2]
    image = image.astype(np.float32) - ctpn_config.IMAGE_MEAN
    image = torch.from_numpy(image.transpose(2, 0, 1)).unsqueeze(0).float()

    with torch.no_grad():
        image = image.to(device)
        cls, regr = model(image)
        cls_prob = F.softmax(cls, dim=-1).cpu().numpy()
        regr = regr.cpu().numpy()
        anchor = gen_anchor((int(h / 16), int(w / 16)), 16)
        bbox = bbox_transfor_inv(anchor, regr)
        bbox = clip_box(bbox, [h, w])

        fg = np.where(cls_prob[0, :, 1] > prob_thresh)[0]
        select_anchor = bbox[fg, :]
        select_score = cls_prob[0, fg, 1]
        select_anchor = select_anchor.astype(np.int32)
        keep_index = filter_bbox(select_anchor, 16)

        # nms
        select_anchor = select_anchor[keep_index]
        select_score = select_score[keep_index]
        select_score = np.reshape(select_score, (select_score.shape[0], 1))
        nmsbox = np.hstack((select_anchor, select_score))
        keep = nms(nmsbox, 0.3)
        select_anchor = select_anchor[keep]
        select_score = select_score[keep]

        # text line
        text_conn = TextProposalConnectorOriented()
        text = text_conn.get_text_lines(select_anchor, select_score, [h, w])

        return text
