from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from app_vacuum.usecase import CheckVacuumUseCase
from app_vacuum.repo import DjangoSettingsRepository
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from celery.result import AsyncResult
from .tasks import check_vacuum_async

# Создаём экземпляр usecase с репозиторием (можно вынести в DI-контейнер)
settings_repo = DjangoSettingsRepository()
check_vacuum_usecase = CheckVacuumUseCase(settings_repo)


# Веб-интерфейс (рендеринг HTML)
@swagger_auto_schema(method='get',
                     manual_parameters=[
                         openapi.Parameter('vacuum_value', openapi.IN_QUERY,
                                           type=openapi.TYPE_NUMBER,
                                           description='Значение вакуума',
                                           required=True),
                     ],
                     responses={200: 'OK'})
@api_view(['GET'])
def check_vacuum_web(request):
    result_data = None
    error = None
    raw_value = request.GET.get('vacuum_value')
    if raw_value is not None:
        try:
            value = float(raw_value)
            result_data = check_vacuum_usecase.execute(value)
        except (TypeError, ValueError):
            error = 'Ошибка: введите корректное число'

    context = {
        'result': result_data['result'] if result_data else None,
        'value': result_data['value'] if result_data else None,
        'threshold': result_data['threshold'] if result_data else settings_repo.get_threshold(),
        'status': result_data['status'] if result_data else '',
        'error': error,
    }
    return render(request, 'vacuum.html', context)


# API (JSON)
@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter(
            'vacuum_value',
            openapi.IN_QUERY,
            type=openapi.TYPE_NUMBER,
            description='Значение вакуума (число с плавающей точкой)',
            required=True
        ),
    ],
    responses={
        200: openapi.Response(
            description='Результат проверки',
            examples={
                'application/json': {
                    'value': 0.8,
                    'threshold': 0.5,
                    'result': 'Работы РАЗРЕШЕНЫ',
                    'status': 'success'
                }
            }
        ),
        400: 'Ошибка: неверный параметр'
    }
)
@api_view(['GET'])
@throttle_classes([AnonRateThrottle])
def api_check_vacuum(request):
    raw_value = request.GET.get('vacuum_value')
    if raw_value is None:
        return Response(
            {'error': 'Параметр "vacuum_value" обязателен'},
            status=400
        )
    try:
        value = float(raw_value)
    except (TypeError, ValueError):
        return Response(
            {'error': 'Значение должно быть числом с плавающей точкой'},
            status=400
        )
    result = check_vacuum_usecase.execute(value)
    return Response(result)


@swagger_auto_schema(method='post', manual_parameters=[
    openapi.Parameter('vacuum_value', openapi.IN_QUERY,
                      type=openapi.TYPE_NUMBER,
                      description='Значение вакуума',
                      required=True),
],
                     responses={200: 'OK'})
@api_view(['POST'])
def api_check_vacuum_async(request):
    raw_value = request.data.get('vacuum_value')
    if raw_value is None:
        return Response({'error': 'Параметр "vacuum_value" обязателен'}, status=400)
    try:
        value = float(raw_value)
    except (TypeError, ValueError):
        return Response({'error': 'Значение должно быть числом'}, status=400)

    task = check_vacuum_async.delay(value)
    return Response({'task_id': task.id}, status=202)


@api_view(['GET'])
def get_task_result(request, task_id):
    task = AsyncResult(task_id)
    if task.ready():
        return Response({
            'status': 'success' if task.successful() else 'failed',
            'result': task.result if task.successful() else str(task.info)
        })
    else:
        return Response({'status': 'pending'}, status=202)
