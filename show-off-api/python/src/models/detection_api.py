from dataclasses import dataclass


@dataclass
class Point:

    axis_x: int
    axis_y: int


@dataclass
class TextBox:

    ord_num: int
    points: list[Point]
    probability: float
