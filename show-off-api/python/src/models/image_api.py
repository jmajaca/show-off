from dataclasses import dataclass


@dataclass
class ImageBoxData:

    start_x: int
    start_y: int
    width: int
    height: int


@dataclass
class ImageData:

    id: str
    file: str
    box: list[ImageBoxData]
    text: str
