from typing import Dict, Any
from app_vacuum.repo import VacuumSettingsRepository


class CheckVacuumUseCase:
    def __init__(self, settings_repo: VacuumSettingsRepository):
        self.settings_repo = settings_repo

    def execute(self, value: float) -> Dict[str, Any]:
        threshold = self.settings_repo.get_threshold()
        if value > threshold:
            result = 'Работы РАЗРЕШЕНЫ'
            status = 'success'
        else:
            result = 'Работы ЗАПРЕЩЕНЫ'
            status = 'danger'
        return {
            'value': value,
            'threshold': threshold,
            'result': result,
            'status': status
        }
