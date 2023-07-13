from django.utils import timezone
import zoneinfo


class HideResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.content = b"Success"  # Thông báo tổng quát hoặc giá trị rỗng
        return response


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timez = request.META.get("HTTP_TIMEZONE")
        if timez:
            timezone.activate(zoneinfo.ZoneInfo(timez))
        else:
            timezone.activate(zoneinfo.ZoneInfo("Asia/Ho_Chi_Minh"))
        return self.get_response(request)
