from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from app_ballon.dto import DTOInput
from app_ballon.usecase import baloon_calculate


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
    print(dto)
    result = baloon_calculate(dto)

    print("##########", dto, result)
    return JsonResponse({"result": result})
