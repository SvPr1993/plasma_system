from django.conf import settings
from abc import ABC, abstractmethod


# Абстрактный интерфейс (для тестируемости)
class VacuumSettingsRepository(ABC):
    @abstractmethod
    def get_threshold(self) -> float:
        pass


# Реализация для Django
class DjangoSettingsRepository(VacuumSettingsRepository):
    def get_threshold(self) -> float:
        return getattr(settings, 'VACUUM_THRESHOLD', 0.5)
