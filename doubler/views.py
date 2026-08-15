from django.http import JsonResponse
from django.shortcuts import render
from doubler.usecase import double_number


def doubler(request, number):
    result = double_number(number)
    return JsonResponse({"result": result})

# Cделать свое приложение по бэкэнду
# Добавить простую формулу по принципу этого приложения



from django.shortcuts import render
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.decorators import api_view


@swagger_auto_schema(method='get',
                     manual_parameters=[
                         openapi.Parameter('param1', openapi.IN_QUERY, type=openapi.TYPE_STRING,
                                           description='Первый параметр'),
                     ],
                     responses={200: 'OK'}
                     )
@api_view(['GET'])
def check_vacuum(request):
    result = None
    value = None

    if request.method == 'POST':
        # Получаем введённое значение
        raw_value = request.POST.get('vacuum_value')
        try:
            value = float(raw_value)
            threshold = getattr(settings, 'VACUUM_THRESHOLD', 0.5)
            if value > threshold:
                result = 'Работы РАЗРЕШЕНЫ'
                status = 'success'
            else:
                result = 'Работы ЗАПРЕЩЕНЫ'
                status = 'danger'
        except (TypeError, ValueError):
            result = 'Ошибка: введите корректное число'
            status = 'warning'

    context = {
        'result': result,
        'value': value,
        'threshold': getattr(settings, 'VACUUM_THRESHOLD', 0.5),
        'status': status if result else '',
    }
    return render(request, 'vacuum.html', context)