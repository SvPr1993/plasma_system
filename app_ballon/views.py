from django.http import JsonResponse
from django.shortcuts import render
from app_ballon.dto import DTOInput
from app_ballon.usecase import baloon_calculate

#Это объем баллонов для начала работ(залать в setting)
SIZE_BALLON = 6


def app_ballon(request):
    p_ox = request.GET.get('p_ox')
    p_ar = request.GET.get('p_ar')
    p_ni = request.GET.get('p_ni')
    try:
        p_ox_d = int(p_ox)
        p_ar_d = int(p_ar)
        p_ni_d = int(p_ni)
    except:
        return JsonResponse({"data_type": "Error"})
    dto = DTOInput(pressure_oxygen=p_ox_d, pressure_argon=p_ar_d, pressure_nirtogen=p_ni_d)
    result = baloon_calculate(dto, SIZE_BALLON)

    print("##########", dto, result)
    return JsonResponse({"result": result})
