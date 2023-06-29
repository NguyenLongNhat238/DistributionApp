class HideResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response.content = b"Success"  # Thông báo tổng quát hoặc giá trị rỗng
        return response
