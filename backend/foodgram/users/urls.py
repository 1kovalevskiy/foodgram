from django.urls import include, path

from rest_framework.routers import SimpleRouter

from users.views import UserViewSet, me_view, set_password,\
    SubscriptionsViewSet

app_name = 'authentication'


router_v1 = SimpleRouter()
router_v1.register(
    r'users/subscriptions', SubscriptionsViewSet, basename='subscriptions'
)
router_v1.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path(r'users/set_password/', set_password, name='set_password'),
    path(r'users/me/', me_view, name='my_profile'),
    path(r'auth/', include('djoser.urls.authtoken')),
    path(r'', include(router_v1.urls)),
]
