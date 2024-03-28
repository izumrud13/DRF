from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users import views
from users.apps import UsersConfig
from users.views import UserListAPIView, UserCreateAPIView, UserDetailAPIView, UserUpdateAPIView, UserDestroyAPIView, \
    PaymentListAPIView, PaymentCreateApiView

app_name = UsersConfig.name

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', UserListAPIView.as_view(), name='user-list'),
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('<int:pk>/', UserDetailAPIView.as_view(), name='user-get'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update'),
    path('delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user-delete'),
    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
    path('payment/create/', PaymentCreateApiView.as_view(), name='course-payment'),

]
