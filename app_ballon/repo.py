from typing import Optional
from app_ballon.dto import BallonMassDTO
from app_ballon.models import BallonMass


class BallonMassRepository:
    @staticmethod
    def get_last_ballon_mass() -> Optional[BallonMassDTO]:
        """
        Возвращает последнюю запись BallonMass в виде DTO.
        Если записей нет, возвращает None.
        """
        ballon_mass = BallonMass.objects.last()
        if ballon_mass is None:
            return None
        return BallonMassDTO(
            oxygen=ballon_mass.oxygen,
            argon=ballon_mass.argon,
            nitrogen=ballon_mass.nitrogen,
        )

