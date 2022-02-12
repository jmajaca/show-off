from dataclasses import dataclass


@dataclass
class Point:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    axis_x: int
    axis_y: int


@dataclass
class TextBox:

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'points':
                setattr(self, key, [Point(**element) for element in value])
            else:
                setattr(self, key, value)

    ord_num: int
    points: list[Point]
    probability: float
