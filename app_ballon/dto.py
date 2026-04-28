from dataclasses import dataclass


@dataclass
class DTOInput:
    volume_liters: int
    pressure_bar: int
    temperature_Celsius: int


class DTOOutput:
    accept_work: bool


@dataclass
class BallonMassDTO:
    oxygen: int
    argon: int
    nitrogen: int
