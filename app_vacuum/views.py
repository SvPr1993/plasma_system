from django.shortcuts import render
from django.conf import settings


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
