from .models import UserAgent


class UserAgentMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """Remember user agent header for each logged-in user"""
        if request.user.is_authenticated:
            user = request.user
            entity, created = UserAgent.objects.get_or_create(user=user)
            entity.user = user
            entity.agent = request.headers.get('User-Agent', '')
            entity.save()

        return self.get_response(request)
