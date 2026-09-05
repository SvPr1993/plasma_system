import logging
import redis
from django.conf import settings
from django.http import JsonResponse
from django.utils.timezone import now
from django.core.exceptions import MiddlewareNotUsed

logger = logging.getLogger(__name__)


class ThrottleMiddleware:
    """
    Глобальный middleware для ограничения количества запросов в секунду (RPS).
    Использует Redis для хранения счётчиков.
    Включается/выключается переменной окружения THROTTLE_ENABLED.
    Лимит задаётся через THROTTLE_RATE (запросов в секунду).
    Можно исключить пути через THROTTLE_EXEMPT_PATHS (список префиксов).
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.enabled = getattr(settings, 'THROTTLE_ENABLED', False)
        self.rate = getattr(settings, 'THROTTLE_RATE', 10)
        self.exempt_paths = getattr(settings, 'THROTTLE_EXEMPT_PATHS', [])
        self.redis_url = (
            getattr(settings, 'THROTTLE_REDIS_URL', None) or
            getattr(settings, 'CELERY_BROKER_URL', None)
        )

        if not self.enabled or not self.redis_url:
            raise MiddlewareNotUsed

        try:
            self.redis_client = redis.from_url(self.redis_url, decode_responses=True)
            self.redis_client.ping()
        except Exception as e:
            logger.error(f"Redis connection failed for throttle: {e}. Middleware disabled.")
            raise MiddlewareNotUsed

    def __call__(self, request):
        if self._should_skip(request):
            return self.get_response(request)

        client_ip = self._get_client_ip(request)
        current_second = int(now().timestamp())
        key = f"throttle:global:{client_ip}:{current_second}"

        try:
            count = self.redis_client.incr(key)
            self.redis_client.expire(key, 2)  # TTL чуть больше 1 секунды

            if count > self.rate:
                return JsonResponse(
                    {'error': 'Too many requests. Please slow down.'},
                    status=429
                )
        except Exception as e:
            logger.warning(f"Throttle redis error: {e}")
            # Fail-open – при ошибке Redis запрос пропускается

        return self.get_response(request)

    def _should_skip(self, request):
        """Проверяет, нужно ли пропустить throttling для данного запроса."""
        if not self.enabled:
            return True

        # Пропускаем методы, не требующие ограничения
        if request.method in ('OPTIONS',):
            return True

        path = request.path_info
        for exempt in self.exempt_paths:
            if path.startswith(exempt):
                return True

        return False

    def _get_client_ip(self, request):
        """Определяет реальный IP клиента с учётом прокси."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip