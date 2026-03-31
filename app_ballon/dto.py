from dataclasses import dataclass


# Прочитать про подсчет дробных чисел в программировании.
@dataclass
class DTOInput:
    volume_liters: int
    pressure_bar: int
    temperature_Celsius: int


class DTOOutput:
    accept_work: bool

