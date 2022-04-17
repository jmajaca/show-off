from dataclasses import dataclass


@dataclass
class ImageBoxData:

    start_x: int
    start_y: int
    width: int
    height: int
    text: str


@dataclass
class TextCorrection:

    id: str
    text: str
