from dataclasses import dataclass


# Прочитать про подсчет дробных чисел в программировании.
@dataclass
class DTOInput:
    pressure_oxygen: int
    pressure_argon: int
    pressure_nirtogen: int


class DTOOutput:
    accept_work: bool

