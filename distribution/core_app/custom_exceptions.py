from rest_framework import exceptions


class NoActionPermissionError(exceptions.APIException):
    status_code = 403
    default_detail = {
        "error": {
            "message": "You don't have action permission in this resource!",
            "vi": "Bạn không có quyền thực hiện hành động này!",
            "en": "You don't have action permission in this resource!",
        }
    }
    default_code = "forbidden"
