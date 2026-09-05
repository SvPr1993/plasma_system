from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from app_vacuum.usecase import CheckVacuumUseCase
from app_vacuum.repo import DjangoSettingsRepository


@shared_task
def check_vacuum_async(vacuum_value: float):
    """
    Асинхронная проверка вакуума. Возвращает результат, аналогичный api.
    """
    repo = DjangoSettingsRepository()
    usecase = CheckVacuumUseCase(repo)
    result = usecase.execute(vacuum_value)
    return result


@shared_task
def send_vacuum_alert_email(vacuum_value: float, result: str, threshold: float):
    """
    Отправка уведомления по электронной почте при изменении статуса (пример).
    """
    subject = f'Результат проверки вакуума: {result}'
    message = f'Значение: {vacuum_value}\nПорог: {threshold}\nСтатус: {result}'
    # Замените на реальный адрес получателя
    recipient_list = ['admin@example.com']
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)


@shared_task
def periodic_vacuum_check():
    """
    Периодическая задача: получает текущее значение вакуума из некоего источника
    (например, из модели или внешнего датчика) и проверяет его.
    Здесь для примера берём случайное число.
    """
    import random
    value = random.uniform(0, 1)  # в реальности — чтение из БД или API
    result = check_vacuum_async(value)
    # Если статус изменился или превышен порог, можно отправить уведомление
    # Для простоты отправляем письмо всегда, когда результат 'danger'
    if result['status'] == 'danger':
        send_vacuum_alert_email.delay(value, result['result'], result['threshold'])
    return result
