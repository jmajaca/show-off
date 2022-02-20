from dataclasses import dataclass


@dataclass
class RecognitionResponse:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    tokens: list[str]
