from datetime import datetime
from user.models import UserLog


class UserLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def request_log(self, method, url, user):
        try:
            create_log = UserLog.objects.get(method=method, url=url, user=user)
            create_log.count += 1
            create_log.updated_at = datetime.now()
            create_log.save()
        except:
            created = UserLog.objects.create(method=method, url=url, user=user)

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            self.request_log(request.method, request.path, request.user)
            # response = self.get_response(request)
        return response
