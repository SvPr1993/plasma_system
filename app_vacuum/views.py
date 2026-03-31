from django.http import JsonResponse


def app_vacuum(request):
    return JsonResponse({"result": 1})
