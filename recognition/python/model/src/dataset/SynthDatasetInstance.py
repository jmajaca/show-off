from dataclasses import dataclass

from torch import Tensor


@dataclass
class SynthDatasetInstance:
    """
    This is a representation of one instance of SynthDataset.

    Attributes
        value (Image): An image.
        label (str): A image label.
    """
    value: Tensor
    label: str

    def __iter__(self):
        return iter([self.value, self.label])
