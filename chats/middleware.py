from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

@database_sync_to_async
def get_user(token_key):
    try:
        access_token = AccessToken(token_key)
        return User.objects.filter(id=access_token['user_id']).first()
    except:
        return AnonymousUser()


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)
        self.inner = inner

    async def __call__(self, scope, receive, send):
        try:
            token_key = scope["query_string"].decode().split('=')[1]
            scope['user'] = await get_user(token_key)
        except:
            pass
        return await super().__call__(scope, receive, send)


TokenAuthMiddlewareStack = (
    lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))
)