from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from app_ballon.dto import DTOInput
from app_ballon.usecase import baloon_calculate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view  # <-- добавить импорт

# Параметры запроса (GET) – остаются без изменений
volume_param = openapi.Parameter('volume_liters', openapi.IN_QUERY, description="Объём в литрах",
                                 type=openapi.TYPE_INTEGER, required=True)
pressure_param = openapi.Parameter('pressure_bar', openapi.IN_QUERY, description="Давление в барах",
                                   type=openapi.TYPE_INTEGER, required=True)
temperature_param = openapi.Parameter('temperature_Celsius', openapi.IN_QUERY, description="Температура в °C",
                                      type=openapi.TYPE_INTEGER, required=True)


@swagger_auto_schema(
    method='get',
    manual_parameters=[volume_param, pressure_param, temperature_param],
    responses={
        200: openapi.Response(
            description="Успешный ответ",
            examples={
                "application/json": {
                    "result": "Работы разрешены"
                }
            }
        ),
        400: openapi.Response(
            description="Ошибка в данных",
            examples={
                "application/json": {
                    "data_type": "Error"
                }
            }
        )
    }
)
@api_view(['GET'])
def app_ballon(request):
    volume_liters = request.GET.get('volume_liters')
    pressure_bar = request.GET.get('pressure_bar')
    temperature_Celsius = request.GET.get('temperature_Celsius')
    try:
        volume_liters_d = int(volume_liters)
        pressure_bar_d = int(pressure_bar)
        temperature_Celsius_d = int(temperature_Celsius)
    except:
        return JsonResponse({"data_type": "Error"})
    dto = DTOInput(volume_liters=volume_liters_d, pressure_bar=pressure_bar_d,
                   temperature_Celsius=temperature_Celsius_d)
    result = baloon_calculate(dto)
    return JsonResponse({"result": result})


# landing остаётся без изменений
def landing(request):
    return render(request, 'index.html')
