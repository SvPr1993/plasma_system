from django.http import JsonResponse
from django.shortcuts import render
from doubler.usecase import double_number


def doubler(request, number):
    result = double_number(number)
    return JsonResponse({"result": result})

# Cделать свое приложение по бэкэнду
# Добавить простую формулу по принципу этого приложения
